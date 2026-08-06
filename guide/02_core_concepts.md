# 02. Graph, node와 실행 흐름

## 1. Node contract

모든 backend node는 `BaseNode`를 상속하고 다음 contract를 제공합니다.

- `type`: workflow JSON에 저장되는 안정적인 식별자
- `label`, `category`, `description`: UI 표시 metadata
- `ports`: input/output 방향, data type, optional·multiple 여부
- `params`: 기본값, 범위, 선택지와 UI 설명
- `execute()`: runtime 처리
- `emit_python()`: 같은 동작을 standalone code로 생성
- `stochastic`, `cacheable`: 실행과 cache 정책

`type`은 저장된 workflow와 API contract이므로 이름을 바꾸면 migration이 필요합니다.

## 2. Metadata-driven UI

Backend registry의 metadata가 frontend palette와 inspector form을 구성합니다. 표준 parameter type이라면 Python node를 구현하고 `register_builtin_nodes()`에 등록하는 것만으로 UI에 나타납니다. File chooser나 annotation editor처럼 특수한 widget이 필요한 경우에만 frontend component를 추가합니다.

## 3. DAG execution

Executor는 graph를 topological order로 정렬합니다. Node를 실행하기 전에 upstream output을 port별 input으로 모으고 parameter를 validation합니다. Cycle, unknown node type, required port 누락과 type mismatch는 실행 전에 차단해야 합니다.

## 4. Cache

Architecture 문서 기준 cache key는 다음 요소에서 content-addressed 방식으로 만들어집니다.

```text
(node_type, params, input hashes, seed)
```

입력이나 parameter가 같으면 이전 output을 재사용할 수 있습니다. 파일 저장처럼 side effect가 있는 node는 `cacheable = False`여야 합니다. Random augmentation은 seed와 sample index를 포함해 재현성을 유지해야 합니다.

## 5. Batch와 annotation

Image port는 단일 `np.ndarray` 또는 image list를 전달할 수 있습니다. Bounding box, mask와 keypoint를 변화시키는 augmentation은 image와 annotation에 동일한 geometric transform을 적용해야 합니다. 좌표 format, image size와 clipping policy를 test로 고정하세요.

## 6. Code generation

`emit_python()`은 editor runtime 없이 같은 결과를 얻는 source line을 반환합니다. 새 node는 다음을 함께 검증해야 합니다.

1. `execute()` output shape·dtype
2. parameter가 실제 pixel 결과에 영향을 주는지
3. `emit_python()` code가 import와 variable을 올바르게 사용하는지
4. runtime과 generated code 결과가 같은지

## 7. Custom node 실습

[`examples/custom_gamma_node.py`](examples/custom_gamma_node.py)는 gamma correction node를 구현합니다. 학습용으로 격리되어 있어 application registry를 자동 변경하지 않습니다.

```bash
cd backend
uv run python ../guide/examples/test_custom_gamma_node.py
```

실제 application에 추가하려면 파일을 `backend/app/nodes/`로 옮기고 `backend/app/nodes/__init__.py`의 `register_builtin_nodes()`에서 instance를 등록한 뒤 backend test를 실행합니다.
