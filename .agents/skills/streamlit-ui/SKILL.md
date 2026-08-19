---
name: streamlit-ui
description: Streamlit 페이지, components, 레이아웃, UI 상태 관리 또는 사용자 인터페이스를 수정하거나 추가할 때 사용한다.
---

# Streamlit UI Guidelines

## 1. UI 구조 및 설계 원칙
- **엔트리포인트**: `app.py`는 애플리케이션의 실행 엔트리포인트 역할에 집중한다.
- **멀티페이지 구조**: 각 화면 기능은 `pages/` 디렉터리 내에 독립된 모듈 파일로 구성한다.
- **UI 컴포넌트 재사용**: 재사용 가능한 UI 카드, 메트릭 표시, 헤더, 테이블 등은 `components/` 모듈로 분리 관리한다.
- **UI-데이터 분리**: Streamlit UI 코드에서 직접 외부 API를 수집하거나 복잡한 데이터 분석 전처리를 수행하지 않는다. (분석/로딩 모듈 호출 방식으로 처리)

## 2. 대시보드 페이지 계획
### Page 1 - Overview (`pages/1_📊_Overview.py`)
- 서울 전체 보안 인프라 KPI
- 자치구별 시설 수, 시설 유형별 분포, 자치구 × 시설유형 Heatmap, 연도별 설치 추이, 자치구별 요약표

### Page 2 - Regional Analysis
- 서울 지도 및 자치구 선택
- 선택 자치구의 보안 인프라 현황 & 시설 유형별 분포
- 인구 대비 시설 수 및 면적 대비 시설 수
- 범죄 데이터와 보안 인프라 비교

### Page 3 - Security Infrastructure
- CCTV, 파출소/지구대, 여성안심귀갓길, 가로등, 비상벨, 기타 안전시설 필터링
- 지도 기반 시설 검색 및 상세 필터링

### Page 4 - Statistics
- 범죄 발생 추이 및 시설 설치 추이
- 인구 대비 시설 비율, 자치구 간 비교
- 범죄와 시설 간 비교 분석, 통계표 및 시각화

## 3. 배포 환경 설정 (Streamlit Community Cloud)
- **Repository**: `bluejals13/seoul-security-insight`
- **Branch**: `main`
- **Main file path**: `app.py`
