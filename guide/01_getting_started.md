# 01. 설치와 첫 pipeline

## 1. 설치

Repository root에서 backend·frontend·desktop dependency를 한 번에 설치합니다.

```bash
npm run install:all
```

이 command는 frontend와 Electron package를 설치하고 `backend/`에서 `uv sync --group dev`를 실행합니다.

## 2. 실행 방법

### Desktop 통합 실행

```bash
npm run desktop
```

Electron이 backend process를 시작하고 editor를 엽니다.

### 개발 server 분리 실행

Terminal 1:

```bash
npm run dev:backend
```

Terminal 2:

```bash
npm run dev:frontend
```

분리 실행은 browser network panel, backend log와 hot reload를 따로 관찰할 때 편리합니다.

## 3. 첫 pipeline

다음 node를 순서대로 연결합니다.

```text
Load Images → Grayscale → Gaussian Blur → Canny → Preview
```

1. `Load Images`에서 한 장의 image를 선택합니다.
2. `Gaussian Blur`의 kernel size를 3, 5, 9로 바꾸며 edge noise 변화를 관찰합니다.
3. `Canny`의 두 threshold를 바꾸고 약한 edge와 강한 edge가 어떻게 남는지 비교합니다.
4. 각 node의 실행 시간과 preview를 기록합니다.
5. Python code를 export하고 `cv2.cvtColor`, `cv2.GaussianBlur`, `cv2.Canny` 순서가 graph와 같은지 확인합니다.

## 4. Template 사용

`frontend/public/examples/`와 `backend/examples/`에는 blur+Canny, contour detection, morphology cleanup, histogram equalization, K-Means palette와 Albumentations 예제가 있습니다. UI에서 template을 불러온 뒤 parameter 하나씩 바꾸는 방식으로 시작하세요.

## 5. 자주 발생하는 문제

### Backend가 시작되지 않음

- Python version과 `uv --version`을 확인합니다.
- `cd backend && uv sync --group dev`를 다시 실행합니다.
- port를 이미 사용하는 process가 있는지 확인합니다.

### Frontend가 backend에 연결되지 않음

- backend health endpoint와 browser console을 확인합니다.
- desktop과 standalone frontend를 동시에 띄웠다면 서로 다른 backend를 바라보지 않는지 확인합니다.
- WebSocket proxy 설정은 `frontend/vite.config.ts`에서 확인합니다.

### Image가 예상과 다른 색으로 보임

OpenCV 기본 channel order는 BGR이고 browser·Pillow에서 흔히 쓰는 순서는 RGB입니다. Color conversion node와 exported code의 channel order를 함께 확인하세요.

### Workflow가 실행되지 않음

- cycle이 없는 DAG인지 확인합니다.
- required input port가 모두 연결됐는지 확인합니다.
- image, mask, bbox와 keypoint port type이 호환되는지 확인합니다.
