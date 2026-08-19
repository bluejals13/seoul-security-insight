# Feature Development Workflow

> **적용 시점 (Trigger)**: 새로운 기능(새 대시보드 페이지, 새로운 시각화 요소, 새로운 데이터 소스 등)을 개발할 때  
> **적용 대상 (Scope)**: 전체 신규 기능 개발 과정

---

## 단계별 개발 절차

### 1단계: 영향 범위 및 계층 확인
- 요구사항을 분석하고 어느 계층(`utils/`, `analysis/`, `visualization/`, `components/`, `pages/`)에 수정을 가할지 사전에 파악한다.
- 기존 구현 코드와 인터페이스 계약(Data Schema 등)을 사전에 확인한다.

### 2단계: Data Loader 및 데이터 처리 구현
- 필요한 경우 `utils/data_loader.py`에 데이터 로딩/fallback 로직을 작성한다.
- 데이터 스키마 규칙 (`.agents/rules/data.md`) 준수 여부를 확인한다.

### 3단계: Analysis 및 Visualization 구현
- `analysis/`에 데이터 분석 및 전처리 로직을 추가한다.
- `visualization/`에 Plotly 차트 또는 Folium 지도 구현 함수를 추가한다.

### 4단계: Streamlit UI 연동
- `components/` 모듈 및 `pages/` 파일에 UI 레이아웃과 데이터 시각화를 연동한다.
- UI 코드와 데이터 로딩 코드가 직접 결합되지 않도록 계층 분리를 유지한다.

### 5단계: 검증 및 회귀 테스트
- `.agents/rules/testing.md`의 7단계 검증 라이프사이클을 수행한다.
- `uv run streamlit run app.py`를 실행하여 정상 작동 및 화면 렌더링을 확인한다.
