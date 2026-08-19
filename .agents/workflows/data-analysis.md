# Data Analysis Workflow

> **적용 시점 (Trigger)**: 공공데이터 신규 추가, 데이터 전처리, 통계 분석 로직 작성/수정 시  
> **적용 대상 (Scope)**: `data/*`, `utils/data_loader.py`, `analysis/*.py`

---

## 단계별 데이터 처리 절차

### 1단계: 원본 데이터 수집 및 배치
- 신규 확보된 공공데이터 원본 파일(CSV 등)을 `data/raw/` 디렉터리에 저장한다.

### 2단계: Data Loader 표준화 구현
- `utils/data_loader.py`에 해당 원본 파일 수집/로드 함수를 추가한다.
- 데이터 항목들을 프로젝트 표준 Schema (`facility_id`, `district`, `facility_type`, `facility_name`, `latitude`, `longitude`, `address`, `installed_year`, `count`)로 변환한다.

### 3단계: 전처리 (Preprocessing) 적용
- `analysis/preprocessing.py`에 데이터 정제, 서울시 외 외곽 좌표 제외, 결측치 처리 로직을 적용한다.

### 4단계: 분석 (Analysis) 연동
- `analysis/regional_analysis.py` 또는 `analysis/statistics.py`에 통계 및 지역 분석 계산 알고리즘을 연동한다.
- 분석 결과는 임의 수치를 하드코딩하지 않고 데이터 기반 연산 결과로 반환한다.

### 5단계: Mock Data fallback 및 검증
- 실제 파일 미존재 시 Mock Data로 항상 정상 작동하는지 확인한다.
- `.agents/rules/testing.md` 절차에 맞춰 import 및 loader/analysis 단위 동작 테스트를 실행한다.
