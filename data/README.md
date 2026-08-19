# Data Architecture & Directory Structure Guide

서울쉴더스 (Seoul Shielders) 보안 인프라 데이터 계층 구조 안내 문서입니다.

---

## 디렉터리 구조 및 역할

```text
data/
├── sample/      # 개발, UI 및 데이터 분석 로직 검증용 샘플 CSV 데이터 (개발 모드)
├── raw/         # 외부 서울시 Open API 또는 공공데이터포털에서 수집한 원본 데이터 (Raw CSV/JSON)
├── processed/   # 전처리 및 내부 9개 표준 Schema로 변환 완료된 정제 데이터
└── metadata/    # 데이터 출처, 수집일, 데이터 스키마 버전 및 가동 상태 메타데이터
```

### 1. `data/sample/`
- **역할**: 개발 환경 및 UI/분석 로직 테스트용 샘플 데이터 저장
- **특징**: 실제 공공데이터 API 연결 전 또는 오프라인 테스트 시 사용됩니다.
- **파일명 예시**: `sample_security_infrastructure.csv`

### 2. `data/raw/`
- **역할**: 외부 API 또는 공공데이터포털에서 다운로드한 수집 원본 데이터 저장
- **특징**: 수집된 형태 그대로 보존하며 직접 분석/UI에 연결하지 않습니다.
- **파일명 예시**: `security_infrastructure.csv`, `cctv.csv`, `police_stations.csv`

### 3. `data/processed/`
- **역할**: Data Loader / Data Ingestion 파이프라인을 거쳐 전처리 및 내부 표준 Schema로 변환된 최종 데이터 저장
- **특징**: 분석 계층(`analysis/`) 및 시각화/UI 계층(`visualization/`, `pages/`)이 읽어오는 표준화된 데이터입니다.
- **파일명 예시**: `security_infrastructure.csv`

### 4. `data/metadata/`
- **역할**: 데이터셋의 메타데이터(출처, 갱신 상태, 스키마 버전 등) 관리
- **특징**: UI에서 데이터 수집일 및 데이터 공급원 상태를 표시할 때 참조합니다.
- **파일명 예시**: `security_infrastructure_metadata.json`

---

## 데이터 흐름 (Data Flow)

### 1. 개발 및 테스트 단계 (현재)
```text
data/sample/ (또는 In-memory Mock Data)
    └── Data Loader (utils/data_loader.py)
            └── Preprocessing (analysis/preprocessing.py)
                    └── Analysis & Visualization (analysis/, visualization/)
                            └── Streamlit UI (pages/, components/)
```

### 2. 실제 서울시 Open API 연동 단계 (향후)
```text
서울시 Open API / 공공데이터포털
    └── Raw Data Ingestion (data/raw/)
            └── Processing & Standardization Layer
                    └── Processed Data (data/processed/)
                            └── Data Loader (utils/data_loader.py)
                                    └── Preprocessing & Analysis
                                            └── Streamlit UI
```
*※ Data Loader 계층 분리를 통해, 실제 데이터 연동 시 분석 및 UI 코드 수정 없이 데이터 파일 배치/갱신만으로 전환이 가능합니다.*
