---
name: python
description: Python 소스 코드를 작성, 수정, 리팩터링하거나 패키지 관리(uv), 타입 힌트, 함수/클래스 모듈화 작업을 수행할 때 사용한다.
---

# Python Development Guidelines

## 1. 런타임 및 패키지 관리
- **Python 버전**: Python 3.12.x
- **패키지 관리자**: `uv` 사용 (`uv run ...` 명령 패턴 적용)

## 2. 코드 구조 및 작성 규칙
- **관심사 분리 (SoC)**:
  - 데이터 로딩: `utils/`
  - 데이터 전처리 및 통계 분석: `analysis/`
  - 시각화(차트/지도): `visualization/`
  - UI 컴포넌트: `components/`
  - 엔트리포인트 및 페이지: `app.py`, `pages/`
- **단순성 유지**:
  - `app.py`나 단일 파일에 비즈니스/수집/분석 로직을 몰아넣지 않는다.
- **코드 스타일 및 타입 힌팅**:
  - 명확하고 직관적인 함수/클래스 네이밍을 준수한다.
  - 주요 함수의 파라미터 및 반환값에 Python 타입 힌트(Type Annotation)를 작성한다.
  - 불필요한 복잡성을 지양하고 예외 처리(try/except)를 명확히 작성한다.
