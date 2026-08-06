# 03. 확장, 성능, 보안과 배포

## 1. 새 node를 production에 추가하는 절차

1. 입력·출력 port와 parameter contract를 먼저 정의합니다.
2. `execute()`를 pure function에 가깝게 작성하고 side effect를 격리합니다.
3. invalid dtype, empty image, 범위 밖 parameter를 명시적으로 처리합니다.
4. `emit_python()`에서 runtime과 같은 default·rounding·channel order를 사용합니다.
5. node를 registry에 등록합니다.
6. metadata, parameter validation, pixel output과 codegen test를 추가합니다.
7. frontend palette와 inspector를 확인하고 특수 widget이 필요할 때만 TypeScript를 수정합니다.

## 2. 성능 분석

- Node별 duration으로 병목을 찾습니다.
- Cache hit 여부와 input hash 비용을 함께 측정합니다.
- 큰 image list는 memory peak와 copy 횟수를 관찰합니다.
- OpenCV operation이 contiguous array를 요구하는지 확인합니다.
- WebSocket preview에는 원본 전체가 아닌 적절한 size·quality의 representation을 사용합니다.
- GPU node를 추가할 때 device transfer가 계산 절감보다 비싸지 않은지 측정합니다.

## 3. 재현성

Workflow JSON, application version, Python dependency lock, input asset hash와 seed를 함께 기록합니다. Albumentations나 OpenCV version이 달라지면 동일 seed라도 결과가 달라질 수 있으므로 `backend/uv.lock`을 보존합니다.

## 4. 보안

### File input과 output

- Client가 보낸 path를 그대로 신뢰하지 않습니다.
- 허용된 asset·workflow·output root 밖으로 나가는 path traversal을 차단합니다.
- Extension뿐 아니라 decode 성공과 실제 image format을 확인합니다.
- Zip output에는 absolute path나 `..` member가 들어가지 않도록 합니다.

### Generated code

Generated Python은 사용자가 검토한 뒤 신뢰된 환경에서 실행해야 합니다. Parameter를 source에 삽입할 때 string representation과 path quoting을 검증하고, 임의 expression을 그대로 code로 연결하지 않습니다.

### Desktop boundary

Electron renderer에는 최소 권한만 노출하고 preload API를 명시적으로 제한합니다. Remote content, shell command와 filesystem 접근을 renderer input에서 직접 실행하지 않습니다.

## 5. 배포

- Docker: `docker-compose.yml`과 `Dockerfile`을 사용해 web application을 구성합니다.
- Desktop: `npm run build:desktop`으로 frontend와 backend sidecar를 packaging합니다.
- CI: backend pytest·ruff, frontend typecheck·lint·build를 분리해 실패 원인을 명확히 합니다.
- Release: workflow schema 변경 시 migration과 backward compatibility를 확인합니다.

## 6. 고급 실습

1. Gamma node의 LUT를 parameter별로 cache해 반복 allocation을 줄입니다.
2. Runtime output과 generated Python output을 같은 synthetic gradient image로 비교합니다.
3. Gamma parameter가 cache key에 포함되는지 확인합니다.
4. `uint8`, grayscale, BGR과 BGRA 입력을 test합니다.
5. 잘못된 gamma 0 또는 음수가 validation에서 거부되는지 확인합니다.
