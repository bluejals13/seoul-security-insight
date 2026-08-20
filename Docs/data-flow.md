# 서울시 생활안전 데이터 흐름 및 데이터 관계 구조도 (Data Flow & ERD)

**문서 작성일자**: 2026년 8월 20일  
**대상 시스템**: 서울시 보안 인프라 분석 및 지도 기반 치안 정보 서비스

---

## 1. 시스템 데이터 파이프라인 구조도 (Data Processing Pipeline)

```mermaid
flowchart TD
    subgraph RAW_LAYER ["1. Raw Data Layer (data/raw/)"]
        R1["5대_범죄_발생현황_2024.csv"]
        R2["등록인구_2024.csv"]
        R3["서울시_가로등_위치_2023.csv"]
    end

    subgraph CLEANING_LAYER ["2. Data Audit & Preprocessing (analysis/)"]
        P1["01_data_audit.py<br/>(인코딩 검단, 결측치/이상치 감사)"]
        P2["02_cleaning.py<br/>(자치구 PK 기준 Inner Join & 1만명당 지표 생성)"]
    end

    subgraph PROCESSED_LAYER ["3. Processed Data Layer (data/processed/)"]
        D1["5대_범죄_자치구별_2024.csv"]
        D2["서울시_가로등_자치구별_2023.csv"]
        D3["seoul_security_consolidated_2024.csv<br/>(통합 데이터셋)"]
    end

    subgraph ANALYSIS_LAYER ["4. Statistical Analysis (analysis/)"]
        A1["03_analysis.py<br/>(절대건수 vs 인구대비 순위, 상관분석, Key Insights)"]
        A2["04_visualization.py<br/>(Plotly/Chart 시각화 자원 생성)"]
    end

    subgraph DELIVERY_LAYER ["5. Delivery & User Experience Layer"]
        V1["dashboard/index.html<br/>(인터랙티브 대시보드)"]
        V2["presentation/index.html<br/>(발표용 HTML 슬라이드)"]
        V3["presentation/seoul-security-insight.pptx<br/>(발표용 PPTX)"]
        V4["docs/<br/>(데이터 감사 및 방법론 문서)"]
    end

    R1 --> P1
    R2 --> P1
    R3 --> P1
    P1 --> P2
    P2 --> D1
    P2 --> D2
    P2 --> D3
    D3 --> A1
    A1 --> A2
    A2 --> V1
    A2 --> V2
    A2 --> V3
    A1 --> V4
```

---

## 2. 데이터 관계 및 스키마 구조도 (Data Entity Relationship Diagram)

```mermaid
erDiagram
    CRIME_2024 {
        string district PK "자치구명 (예: 강남구, 중구)"
        int crime_count_2024 "5대 범죄 총 발생건수"
        int murder_2024 "살인 발생건수"
        int robbery_2024 "강도 발생건수"
        int sexual_violence_2024 "성범죄 발생건수"
        int theft_2024 "절도 발생건수"
        int violence_2024 "폭력 발생건수"
    }

    STREETLIGHT_2023 {
        string district PK "자치구명 (예: 강남구, 중구)"
        int streetlights_2023 "가로등 총 설치 수"
    }

    POPULATION_2024 {
        string district PK "자치구명 (예: 강남구, 중구)"
        int population_2024 "주민등록 총 인구 수"
    }

    CONSOLIDATED_SECURITY_2024 {
        string district PK "자치구명"
        int crime_count_2024 "5대 범죄 총 발생건수"
        int population_2024 "주민등록 인구 수"
        int streetlights_2023 "가로등 총 설치 수"
        float crime_per_10k "인구 1만명당 범죄건수"
        float streetlights_per_10k "인구 1만명당 가로등수"
        float crime_per_streetlight "가로등 1개당 범죄건수"
        float violence_pct "폭력 비중 (%)"
        float theft_pct "절도 비중 (%)"
    }

    CRIME_2024 ||--|| CONSOLIDATED_SECURITY_2024 : "Inner Join on district"
    STREETLIGHT_2023 ||--|| CONSOLIDATED_SECURITY_2024 : "Inner Join on district"
    POPULATION_2024 ||--|| CONSOLIDATED_SECURITY_2024 : "Inner Join on district"
```

---

## 3. 리포지토리 구성과 데이터 흐름 매핑 Table

| 파이프라인 단계 | 실행 파일 / 소스 파일 | 주요 역할 및 출력물 |
|---|---|---|
| **1. 감사 (Audit)** | `analysis/01_data_audit.py` | CSV 데이터의 인코딩, 결측치, 이상치, 행/열 구조 점검 |
| **2. 정제 (Clean)** | `analysis/02_cleaning.py` | 자치구 PK 기준 Inner Join -> `seoul_security_consolidated_2024.csv` 생성 |
| **3. 분석 (Analysis)** | `analysis/03_analysis.py` | 절대/상대 순위, 피어슨 상관계수, 5대 범죄 비율 계산 -> `key_analysis_results.json` |
| **4. 시각화 (Visualization)** | `analysis/04_visualization.py` | 대시보드 및 발표용 차트 자원 및 HTML/PPTX 자원 통합 생성 |
| **5. 대시보드 (Dashboard)** | `dashboard/index.html` | 자치구/범죄유형 필터링, Hover Tooltip, 순위 정렬 인터랙티브 웹 UI |
| **6. 프레젠테이션 (Presentation)**| `presentation/index.html`, `.pptx` | 16:9 슬라이드, 스피커 노트를 지원하는 발표용 산출물 |
