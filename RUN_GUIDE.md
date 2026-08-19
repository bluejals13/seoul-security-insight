# SEOUL SECURITY INFRASTRUCTURE INSIGHT - 실행 가이드

서울지역 보안 인프라 데이터 분석 Streamlit 대시보드 실행 구동 가이드입니다.

---

## 1. 실행 환경 요구사항

- **Python**: `>=3.11, <3.13`
- **Package Manager**: `uv`
- **주요 가상환경**: 프로젝트 루트 `.venv`

---

## 2. 앱 실행 방법

프로젝트 루트 디렉토리(`C:\Users\user\Desktop\seoul-security-insight`)에서 아래 명령어를 실행합니다.

```bash
.venv/Scripts/python.exe -m streamlit run app.py
```

실행 성공 시 다음과 같은 터미널 메시지와 함께 브라우저에서 서비스가 자동으로 론칭됩니다.

```text
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://...:8501
```

---

## 3. 주요 페이지 구성

1. **메인 인덱스 (`app.py`)**: 서비스 개요, 헤더, DEMO DATA 안내 및 주요 KPI 요약
2. **Page 1 Overview (`pages/1_📊_Overview.py`)**:
   - **Header & DEMO DATA**: 서비스 소개 및 Mock Data 경고 표시
   - **KPI Cards**: 전체 시설 수량, 자치구 수, 시설 유형 수, 구별 평균 수량
   - **자치구별 보안 인프라 수**: Horizontal Bar Chart (시설 수 기준 내림차순 정렬)
   - **시설 유형별 설치 비중**: Donut Chart
   - **자치구 × 시설 유형 분포**: Heatmap (SEOUL_DISTRICTS 25개 구 순서)
   - **연도별 설치 추이**: Line Chart
   - **자치구별 요약 표**: Summary Data Table

---

## 4. 모듈 단독 검증 명령어

### Python Import 테스트
```bash
.venv/Scripts/python.exe -c "import app; print('APP IMPORT OK')"
.venv/Scripts/python.exe -c "import runpy; runpy.run_path('pages/1_📊_Overview.py'); print('OVERVIEW IMPORT OK')"
```

### 전처리기 및 모듈 통합 테스트
```bash
.venv/Scripts/python.exe -c "from utils.mock_data import get_mock_data; from analysis.preprocessing import preprocess_data; df = preprocess_data(get_mock_data()); print('Cleaned Data Shape:', df.shape)"
```

---

## 5. 실제 공공데이터 연결 방법

실제 공공데이터 CSV가 준비되면 아래 절차로 연결할 수 있습니다.

### 1. 데이터 준비

서울시 또는 공공데이터포털 등에서 보안 인프라 관련 데이터를 CSV 형태로 준비합니다.

### 2. CSV 저장

파일명을 다음과 같이 지정합니다.

`security_infrastructure.csv`

그리고 다음 위치에 저장합니다.

`data/raw/security_infrastructure.csv`

### 3. 데이터 형식 확인

Data Loader는 내부적으로 다음 9개 표준 컬럼을 사용합니다.

- `facility_id`
- `district`
- `facility_type`
- `facility_name`
- `latitude`
- `longitude`
- `address`
- `installed_year`
- `count`

실제 CSV의 컬럼명은 현재 `utils/data_loader.py`에 정의된 지원 매핑 규칙에 따라
위 표준 컬럼으로 변환됩니다.

실제 데이터의 컬럼명이 지원되는 매핑 규칙과 일치하지 않는 경우
자동으로 추측하거나 Mock Data로 대체하지 않고 데이터 검증 오류를 발생시킵니다.

### 4. 대시보드 실행

프로젝트 루트에서 실행합니다.

```bash
.venv/Scripts/python.exe -m streamlit run app.py

