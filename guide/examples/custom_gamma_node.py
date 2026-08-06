"""학습용 gamma correction node.

이 파일은 application registry를 자동 변경하지 않습니다. 실제로 추가하려면
backend/app/nodes/ 아래로 옮기고 register_builtin_nodes()에서 등록하세요.
"""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np

from app.engine.registry import BaseNode
from app.nodes.common import image_in, image_out, number_param, require_image


class GammaCorrectionNode(BaseNode):
    """8-bit image에 lookup table 기반 gamma correction을 적용합니다."""

    type = "gamma_correction_tutorial"
    label = "Gamma Correction (Tutorial)"
    category = "color"
    description = "Apply gamma correction with a precomputed uint8 lookup table."
    ports = [image_in(), image_out()]
    params = [
        number_param(
            "gamma",
            "Gamma",
            1.0,
            minimum=0.1,
            maximum=5.0,
            step=0.1,
            description="Values below 1 brighten; values above 1 darken.",
        )
    ]

    @staticmethod
    def _lut(gamma: float) -> np.ndarray:
        """OpenCV LUT에 사용할 256-entry table을 만듭니다."""
        if gamma <= 0:
            raise ValueError("gamma must be greater than zero")
        values = np.arange(256, dtype=np.float32) / 255.0
        corrected = np.power(values, gamma) * 255.0
        return np.clip(np.rint(corrected), 0, 255).astype(np.uint8)

    def execute(
        self,
        inputs: dict[str, Any],
        params: dict[str, Any],
        seed: int = 0,
    ) -> dict[str, np.ndarray]:
        del seed  # deterministic node이므로 seed를 사용하지 않습니다.
        image = require_image(inputs)
        if image.dtype != np.uint8:
            raise ValueError("GammaCorrectionNode expects a uint8 image")
        gamma = float(params["gamma"])
        return {"image": cv2.LUT(image, self._lut(gamma))}

    def emit_python(
        self,
        node_id: str,
        params: dict[str, Any],
        input_vars: dict[str, str],
        output_vars: dict[str, str],
    ) -> list[str]:
        gamma = float(params["gamma"])
        src = input_vars["image"]
        dst = output_vars["image"]
        safe_id = "".join(ch if ch.isalnum() else "_" for ch in node_id)
        lut_var = f"_gamma_lut_{safe_id}"
        return [
            f"{lut_var} = np.clip(np.rint((np.arange(256, dtype=np.float32) / 255.0) "
            f"** {gamma!r} * 255.0), 0, 255).astype(np.uint8)",
            f"{dst} = cv2.LUT({src}, {lut_var})",
        ]
