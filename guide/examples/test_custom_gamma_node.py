"""Custom Gamma node의 독립 실행 검증.

실행:
    cd backend
    uv run python ../guide/examples/test_custom_gamma_node.py
"""

from __future__ import annotations

import cv2
import numpy as np
from custom_gamma_node import GammaCorrectionNode


def gradient_image() -> np.ndarray:
    row = np.arange(256, dtype=np.uint8)
    return np.repeat(row[None, :], 16, axis=0)


def main() -> None:
    node = GammaCorrectionNode()
    image = gradient_image()

    identity = node.execute({"image": image}, {"gamma": 1.0})["image"]
    darker = node.execute({"image": image}, {"gamma": 2.0})["image"]
    brighter = node.execute({"image": image}, {"gamma": 0.5})["image"]

    assert np.array_equal(identity, image)
    assert darker.shape == image.shape and darker.dtype == np.uint8
    assert brighter.shape == image.shape and brighter.dtype == np.uint8
    assert int(darker[0, 128]) < int(image[0, 128])
    assert int(brighter[0, 128]) > int(image[0, 128])

    code = node.emit_python(
        "gamma-1",
        {"gamma": 2.0},
        {"image": "input_image"},
        {"image": "output_image"},
    )
    assert any("cv2.LUT" in line for line in code)
    namespace = {"cv2": cv2, "np": np, "input_image": image}
    exec("\n".join(code), namespace)
    assert np.array_equal(namespace["output_image"], darker)
    assert node.metadata().type == "gamma_correction_tutorial"
    print("custom gamma node checks passed")


if __name__ == "__main__":
    main()
