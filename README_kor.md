<div align="center">

# 🎨 Image Pipes

### 스크립트 작성을 멈추고, 결과를 직접 보세요.

**컴퓨터 비전 pipeline을 시각적으로 구성하고 모든 pixel 변환을 실시간으로 확인한 뒤, 원하는 결과가 나오면 production-ready Python code로 내보냅니다.**

**⚡ 구성 · 미리보기 · 실험 · 내보내기**

[English](README.md) ·
[다운로드](https://github.com/mrajaeim/image-pipes/releases) ·
[기능](#-주요-기능) ·
[Architecture](#-architecture) ·
[빠른-시작](#-빠른-시작) ·
[한국어 학습 가이드](guide/README.md)

</div>

## 🚀 작업 방식

### Visual Editor

- node를 drag-and-drop하여 pipeline 구성
- 즉시 실행과 중간 결과 확인
- OpenCV와 Albumentations 처리
- 완성된 graph를 Python code로 내보내기

Dataset augmentation을 시각적으로 대량 생성할 수 있고, 반복 가능한 computer vision pipeline을 template으로 관리할 수 있습니다.

## 💭 해결하는 문제

기존 computer vision pipeline 개발에서는 다음 반복이 자주 발생합니다.

```text
parameter 수정 → script 실행 → image 저장 → image 열기 → 비교 → 반복
```

Blur kernel, threshold와 augmentation 값을 조정할 때마다 작업 context가 끊깁니다. Image Pipes는 pipeline을 graph로 조립하고 각 node 출력을 바로 보여 주며, 최종 결과를 standalone Python으로 내보내 이 반복 비용을 줄입니다.

```text
Load Image
    ↓
Resize
    ↓
Grayscale
    ↓
Gaussian Blur
    ↓
Threshold
    ↓
Find Contours
    ↓
Standalone Python
```

## ✨ 주요 기능

### 🎨 Console 대신 canvas

React Flow 기반 무한 canvas에 node를 배치하고 연결합니다. Backend node metadata에서 property panel과 validation을 자동 생성합니다.

- type을 인식하는 연결
- zoom과 pan을 지원하는 무한 canvas
- metadata 기반 동적 property panel
- graph 구성 중 실시간 validation

### ⚡ 단계별 실시간 preview

각 node는 독립적으로 실행되므로 연속된 `cv2` 호출의 결과를 머릿속으로 추측할 필요가 없습니다.

- 중간 image 출력
- bounding box, segmentation mask와 keypoint
- node별 실행 시간
- runtime log

### 🧠 DAG execution engine

Pipeline을 DAG (Directed Acyclic Graph, 방향성 비순환 그래프)로 검증하고 topological order로 실행합니다.

- incremental execution과 부분 재계산
- 선택한 node까지만 실행하는 targeted debugging
- in-memory cache
- 실행 전 전체 DAG validation

### 📦 Metadata-driven architecture

새 backend node의 type, port, parameter와 실행·codegen 동작을 구현하고 registry에 등록하면 frontend가 metadata를 읽어 palette, form과 validation을 구성합니다. 일반적인 node 추가에는 React code 변경이 필요하지 않습니다.

### 🧪 Computer vision toolbox

OpenCV를 통해 다음 기능을 제공합니다.

- color 변환, blur, filter와 edge detection
- histogram, morphology와 geometric transform
- contour, threshold, K-Means 등

Albumentations를 통해 flip, rotation, color jitter, noise, cutout과 elastic transform을 graph에 연결할 수 있습니다. Image와 함께 bounding box, mask와 keypoint도 전달합니다. Seed를 지정하면 동료와 실험 사이에 결과를 재현할 수 있습니다.

### 🐍 Runtime lock-in 없는 Python export

시각적으로 설계한 pipeline은 OpenCV와 Albumentations 기반의 읽을 수 있는 standalone Python으로 export됩니다.

```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)
```

Export된 code는 training pipeline, ETL job 또는 notebook에 바로 통합할 수 있습니다.

## 🚀 활용 사례

- ML training용 dataset preprocessing
- Albumentations augmentation 설계와 tuning
- computer vision 개념 교육
- OpenCV prototype과 parameter 탐색
- deterministic·versionable research pipeline
- box, mask와 keypoint annotation pipeline debugging
- 일반 image 분석

## 🏗 Architecture

```text
                     React Flow Editor
                             │
                    REST + WebSockets
                             │
                             ▼
                  DAG Execution Engine
               ┌─────────────┴─────────────┐
               │                           │
               ▼                           ▼
        OpenCV Processing          Albumentations
               │                           │
               └─────────────┬─────────────┘
                             ▼
                  Live Preview & Export
                             │
                             ▼
                    Standalone Python
```

### 기술 stack

| 영역 | 기술 |
|---|---|
| Frontend | React 19, TypeScript, Vite, React Flow, Zustand, TanStack Query, Material UI, Monaco Editor, React Hook Form, Zod |
| Backend | FastAPI, OpenCV, Albumentations, NumPy, Pillow, WebSocket, Pydantic v2 |
| Desktop | Electron |

## 🚀 빠른 시작

### Desktop installer

[Releases](https://github.com/mrajaeim/image-pipes/releases)에서 Windows, macOS 또는 Linux installer를 받으면 Python이나 Node.js 없이 실행할 수 있습니다.

### Source에서 실행

```bash
git clone https://github.com/mrajaeim/image-pipes.git
cd image-pipes
npm run install:all
npm run desktop
```

Electron application이 backend를 시작하고 editor를 엽니다.

개발 server를 분리해서 실행하려면 다음 command를 사용합니다.

```bash
npm run dev:backend
npm run dev:frontend
```

## 🧪 검증

```bash
cd backend
uv run pytest
uv run ruff check .

cd ../frontend
npm run typecheck
npm run lint
npm run build
```

## 🎯 주요 장점

| 장점 | 설명 |
|---|---|
| Visual workflow | script 수정 없이 node 연결과 parameter 변경을 반복 |
| 단계별 preview | 모든 변환의 중간 출력과 실행 시간 확인 |
| Metadata-driven | custom backend node가 UI와 codegen에 자동 연결 |
| 재현 가능한 augmentation | seed와 versionable workflow JSON 활용 |
| Python export | 전용 runtime에 묶이지 않는 source code 생성 |

## 🛣 Roadmap

- video pipeline과 camera streaming
- ONNX Runtime·PyTorch inference node
- CUDA acceleration
- batch processing
- plugin SDK
- cloud workspace
- pipeline template
- AI-assisted pipeline generation

## 🤝 기여

Bug fix, 성능 개선, 새 processing node와 기능 기여를 환영합니다. 큰 변경은 먼저 issue를 열어 설계를 논의하는 것이 좋습니다.

새 node 작성 실습과 내부 구조는 [한국어 학습 가이드](guide/README.md)를 참고하세요.

## 📄 License

MIT License로 배포됩니다. 자세한 내용은 [LICENSE](LICENSE)를 확인하세요.

## 번역 정보

이 문서는 원본 [`README.md`](README.md)의 한국어 번역본입니다. 원문의 section, link, code와 기술적 의미를 유지하면서 자연스러운 한국어로 옮겼으며 2026-08-06의 `main`을 기준으로 작성했습니다.
