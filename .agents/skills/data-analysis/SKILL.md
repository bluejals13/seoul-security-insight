---
name: data-analysis
description: 데이터 수집, Data Loader 계층, 표준 Schema 변환, 데이터 전처리, 서울 25개 자치구 분석, API 연동, Mock Data 및 Fallback 처리를 수행할 때 사용한다.
---

# Data & Analysis Guidelines

## 1. 프로젝트 핵심 데이터 종류 (6가지)
1. **서울시 지구대/파출소**: 시설명, 주소, 위도/경도, 운영시간(확보 시), 자치구
2. **서울시 CCTV**: 위치, 자치구, 설치 수량, 설치 연도(확보 시)
3. **서울시 여성안심귀갓길**: 구간/위치, 자치구, 좌표 또는 공간정보, 구간명
4. **자치구별 인구 및 면적**: 자치구, 인구, 면적, 인구밀도
5. **서울 지역별 범죄 데이터**: 자치구/지역, 범죄 유형, 발생 건수, 연도, 장소 유형(확보 시)
6. **안전 관련 공공시설**: 가로등, 비상벨, 안심벨, 기타 안전시설 (위치, 수량, 자치구)

## 2. 표준 데이터 계약 (Schema)
모든 시설 데이터는 Data Loader 계층을 거치며 다음 내부 표준 Schema로 변환 및 통합된다:
- `facility_id`: 시설 식별자
- `district`: 자치구명 (서울특별시 25개 자치구)
- `facility_type`: 시설 유형 (CCTV, 파출소/지구대, 여성안심귀갓길, 가로등, 비상벨 등)
- `facility_name`: 시설명
- `latitude`: 위도
- `longitude`: 경도
- `address`: 주소
- `installed_year`: 설치 연도
- `count`: 수량

## 3. 데이터 로딩 및 Fallback 원칙
- **우선순위**: `data/raw/security_infrastructure.csv` (또는 개별 공공데이터 CSV) 존재 시 실제 CSV 우선 로드, 미존재 시 Mock Data fallback 동작.
- **Schema 검증 주의사항**: 실제 데이터 파일이 존재하지만 schema가 잘못된 경우 조용히 Mock Data로 fallback하지 않고 오류를 알린다.
- **좌표 및 수치 처리 규칙**:
  - 좌표가 없는 데이터를 임의 좌표로 생성하지 않는다.
  - 서울시 범위를 벗어나는 외곽/외곽지역 좌표는 지도 및 분석 데이터에서 제외한다.
  - 실제 데이터 없이 통계 수치를 임의로 만들어내지 않는다.

## 4. API / 공공데이터 연동 원칙
- API 호출 모듈은 `utils/data_sources/` 또는 별도 Data Ingestion 계층으로 분리한다.
- API 장애 발생 시 앱 전체가 다운되지 않도록 예외 처리를 철저히 한다.
- 외부 API/데이터는 내부 표준 Schema로 변환한다.
- UI 표기를 위해 데이터 출처(Source)와 수집일(Updated Date) metadata 구조를 유지한다.
- 로컬 캐싱을 적용하여 동일 API의 반복 호출을 방지한다.
- 실제 데이터가 추가되면 기존 Mock Data 기반 분석/시각화 로직을 그대로 재사용한다.

## 5. 데이터 파일 구조 및 확장 순서
### 디렉터리 구조
```text
data/
  raw/
    security_infrastructure.csv
    police_stations.csv
    cctv.csv
    safe_roads.csv
    population.csv
    crime.csv
    safety_facilities.csv
  processed/
```

### 실제 공공데이터 추가 순서
1. 원본 데이터를 `data/raw/`에 저장
2. Data Loader (`utils/data_loader.py`)에서 로드 구현
3. 내부 표준 schema로 변환/표준화
4. `analysis/preprocessing.py` 전처리 적용
5. `analysis/` 통계 분석 모듈 연결
6. `visualization/` 시각화 모듈 연결
7. `pages/` 및 `components/` UI 연동
