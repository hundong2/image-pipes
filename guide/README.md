# Image Pipes 한국어 학습 가이드

작성일: 2026-08-06

Image Pipes를 설치하고 시각적 pipeline을 만든 뒤, DAG executor와 metadata-driven node architecture를 이해하고 custom node를 확장하는 순서로 학습합니다.

## 학습 순서

1. [설치와 첫 pipeline](01_getting_started.md)
2. [Graph, node와 실행 흐름](02_core_concepts.md)
3. [확장, 성능, 보안과 배포](03_advanced.md)
4. [Custom Gamma node 예제](examples/custom_gamma_node.py)
5. [예제 test](examples/test_custom_gamma_node.py)

## 프로젝트 목적

OpenCV·Albumentations pipeline을 React Flow canvas에서 설계하고 각 node 결과를 즉시 확인한 뒤, 동일 동작의 standalone Python code를 생성합니다. 실험 속도와 관찰 가능성을 높이되 production code export를 제공해 visual tool에 종속되지 않도록 합니다.

## 전체 흐름

```text
Workflow JSON
  → Pydantic graph validation
  → node metadata·port type 검사
  → topological sort
  → dependency output 수집
  → cache key 계산
  → BaseNode.execute()
  → WebSocket progress·preview

동일 graph
  → topological sort
  → BaseNode.emit_python()
  → standalone Python
```

## 핵심 디렉터리

| 경로 | 역할 |
|---|---|
| `backend/app/engine/` | registry, executor, cache와 실행 context |
| `backend/app/nodes/` | OpenCV·Albumentations node 구현 |
| `backend/app/services/codegen.py` | graph에서 Python source 생성 |
| `backend/app/api/` | REST API |
| `backend/app/websocket/` | 실행 progress와 결과 전달 |
| `frontend/src/store/graphStore.ts` | editor graph 상태 |
| `frontend/src/features/` | canvas, inspector, preview와 workflow UI |
| `frontend/src/workflow/` | template, import/export와 persistence |
| `desktop/` | Electron main·preload process |

## 준비물

- Python 3.11 이상 (`README` badge는 3.12+ 권장)
- Node.js와 npm
- [uv](https://docs.astral.sh/uv/)
- Desktop build 시 platform별 packaging dependency

## 빠른 검증

```bash
npm run install:all

cd backend
uv run pytest
uv run ruff check .

cd ../frontend
npm run typecheck
npm run build
```

## 문서 연결

- [한국어 README](../README_kor.md)
- [원문 README](../README.md)
- [Architecture 문서](../docs/architecture.md)
