



# AGENTS.md

# SEOUL SECURITY INFRASTRUCTURE INSIGHT

서울지역 보안 인프라 데이터를 분석하고 시각화하여
서울의 지역별 보안 인프라 현황을 탐색할 수 있는
Streamlit 기반 데이터 분석 프로젝트이다.

---

# 1. PROJECT PURPOSE

이 프로젝트의 목적은 서울지역의 보안 인프라 데이터를 기반으로 다음 질문에
답할 수 있는 데이터 분석 서비스를 만드는 것이다.

- 서울 어느 지역에 보안 인프라가 많이 분포하는가?
- 자치구별 보안 인프라 분포에는 어떤 차이가 있는가?
- CCTV, 방범시설, 안전시설 등의 분포는 어떻게 다른가?
- 지역별 인구 또는 면적을 고려하면 어떤 지역의 인프라 밀도가 높은가?
- 특정 지역의 보안 인프라 현황은 어떠한가?
- 지도상에서 보안 인프라의 공간적 분포를 어떻게 확인할 수 있는가?

최종적으로 Streamlit Dashboard를 통해 사용자가 서울의 보안 인프라 현황을
쉽게 탐색할 수 있도록 한다.

---

# 2. CURRENT DEVELOPMENT PHASE

현재 프로젝트는 초기 개발 단계이다.

현재 가장 중요한 목표는 다음과 같다.

1. 프로젝트 실행 환경 구축
2. Streamlit 공통 UI 구축
3. Mock Data 구축
4. 데이터 분석 함수 구축
5. 차트 컴포넌트 구축
6. 지도 시각화 구조 구축
7. 페이지 구조 구축
8. 실제 데이터 연결 준비

현재 단계에서는 외부 API 및 실제 데이터 수집보다
UI / 분석 / 시각화 구조를 먼저 완성한다.

---

# 3. IMPORTANT DEVELOPMENT PRIORITY

개발 우선순위는 다음과 같다.

1. UI / 공통 컴포넌트
2. Mock Data
3. 분석 로직
4. 시각화
5. Streamlit 페이지
6. 실제 데이터 연결
7. 외부 API
8. 크롤링 / 자동 수집
9. 고급 기능

현재 단계에서 API나 크롤러를 먼저 구현하지 않는다.

---

# 4. MVP SCOPE

## 반드시 구현

- Streamlit 실행
- 공통 Header
- Sidebar Filter
- KPI 카드
- DataFrame Table
- Bar Chart
- Pie / Donut Chart
- 지역별 비교
- 지도 시각화 구조
- Mock Data
- 지역 필터
- 시설 유형 필터
- 자치구별 분석
- 시설 유형별 분석
- 기본 통계 분석
- 분석 결과 페이지

## 시간이 남으면

- 지도 기반 상세 탐색
- 지역별 시설 밀도
- 인구 대비 시설 수
- 면적 대비 시설 수
- 여러 시설 유형 비교
- 기간별 변화

## 현재 구현하지 않는 기능

- 로그인
- 회원가입
- 사용자 DB
- 결제
- 관리자 페이지
- 채팅
- 복잡한 AI
- LLM 추천
- 실시간 알림
- 외부 API 자동 수집
- Selenium 자동 수집
- 대규모 크롤러
- 불필요한 외부 서비스

---

# 5. TECHNOLOGY STACK

## Language

Python 3.11+

## Package Manager

uv

## Environment

프로젝트 루트의 `.venv`를 사용한다.

실행은 가능한 한 다음 방식을 사용한다.

```bash
uv run streamlit run app.py


Python 실행:

uv run python


패키지 확인:

uv pip list


패키지 추가가 필요한 경우 먼저 기존 환경을 확인한다.

uv pip list


이미 설치된 라이브러리를 우선 사용한다.

새로운 패키지를 추가하기 전에 반드시 사용자에게 확인한다.

6. MAIN LIBRARIES

현재 프로젝트에서 우선 사용하는 라이브러리:

pandas
numpy
plotly
streamlit
matplotlib
seaborn
folium
streamlit-folium
python-dotenv

필요 이상의 라이브러리를 추가하지 않는다.

7. PROJECT STRUCTURE

기본 구조:

job-insight/
│
├── app.py
├── AGENTS.md
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .env
├── .env.example
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── analysis/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── statistics.py
│   └── regional_analysis.py
│
├── visualization/
│   ├── __init__.py
│   ├── charts.py
│   └── maps.py
│
├── components/
│   ├── __init__.py
│   ├── header.py
│   ├── sidebar.py
│   ├── metrics.py
│   ├── tables.py
│   └── cards.py
│
├── utils/
│   ├── __init__.py
│   ├── common.py
│   └── mock_data.py
│
├── pages/
│   ├── 1_📊_Overview.py
│   ├── 2_🗺️_Regional_Analysis.py
│   ├── 3_🔐_Security_Infra.py
│   └── 4_📈_Statistics.py
│
└── notebooks/
    └── 01_EDA.ipynb

8. ARCHITECTURE

데이터 흐름은 다음 구조를 유지한다.

Data Source
    ↓
Raw Data
    ↓
Preprocessing
    ↓
Analysis
    ↓
Visualization
    ↓
Streamlit


현재 실제 데이터가 없을 경우:

Mock Data
    ↓
Preprocessing
    ↓
Analysis
    ↓
Visualization
    ↓
Streamlit


실제 데이터 연결 후에도 가능한 한 동일한 데이터 인터페이스를 유지한다.

9. MOCK DATA FIRST

현재 개발 단계에서는 Mock Data를 적극적으로 사용한다.

Mock Data는 실제 데이터와 가능한 한 동일한 컬럼 구조를 사용해야 한다.

예:

district
facility_type
facility_name
latitude
longitude
address
installed_year
count


예시:

강남구
CCTV
방범 CCTV
37.4979
127.0276
서울특별시 강남구 ...
2024
1


Mock Data는 실제 데이터를 흉내 내기 위한 것이며
실제 통계값으로 오해될 수 있는 문구를 사용하지 않는다.

Dashboard에 Mock Data를 사용하는 경우 다음과 같이 표시할 수 있다.

DEMO DATA
현재 화면은 서비스 UI 및 분석 로직 검증을 위한 Mock Data입니다.

10. DATA SCHEMA

기본 데이터 스키마는 다음을 사용한다.

Security Infrastructure
facility_id
district
facility_type
facility_name
latitude
longitude
address
installed_year
count


필요한 경우 다음 컬럼을 추가할 수 있다.

dong
management_org
status
source


단, 기존 분석 코드에 영향을 주는 컬럼 변경은
임의로 수행하지 않는다.

11. FACILITY TYPES

MVP에서 사용할 기본 시설 유형:

FACILITY_TYPES = [
    "CCTV",
    "보안등",
    "비상벨",
    "방범시설",
    "안전시설",
]


실제 데이터의 시설 분류가 달라질 경우
분석 코드에서 직접 문자열을 하드코딩하지 말고
설정 파일 또는 상수로 관리한다.

12. SEOUL DISTRICTS

서울 25개 자치구를 기본 분석 단위로 사용한다.

SEOUL_DISTRICTS = [
    "강남구",
    "강동구",
    "강북구",
    "강서구",
    "관악구",
    "광진구",
    "구로구",
    "금천구",
    "노원구",
    "도봉구",
    "동대문구",
    "동작구",
    "마포구",
    "서대문구",
    "서초구",
    "성동구",
    "성북구",
    "송파구",
    "양천구",
    "영등포구",
    "용산구",
    "은평구",
    "종로구",
    "중구",
    "중랑구",
]

13. ANALYSIS RULES

분석 로직과 UI 코드를 분리한다.

잘못된 구조:

# Streamlit page

df.groupby(...)
st.bar_chart(...)


가능하면 다음과 같이 분리한다.

analysis/
    ↓
DataFrame / 결과 객체
    ↓
visualization/
    ↓
Plotly Figure
    ↓
Streamlit page


분석 함수는 Streamlit UI를 직접 호출하지 않는다.

14. CORE ANALYSIS

MVP 핵심 분석은 다음과 같다.

14.1 지역별 시설 수
강남구     1,240
송파구     1,180
관악구     1,050
...

14.2 시설 유형별 수
CCTV       5,200
보안등     3,800
비상벨     1,200
...

14.3 자치구 × 시설 유형

Cross Tab:

        CCTV  보안등  비상벨
강남구    500    300     80
송파구    480    290     70
관악구    520    350     90

14.4 지역별 시설 밀도

가능한 경우:

시설 수 / 면적


또는

시설 수 / 인구


를 계산한다.

단, 인구나 면적 데이터가 없는 경우
임의의 수치를 만들어 사용하지 않는다.

15. ANALYSIS OUTPUT CONTRACT

분석 함수는 가능한 한 다음 형태로 결과를 반환한다.

pd.DataFrame


예:

def get_facility_count_by_district(df):
    return (
        df.groupby("district")
        .size()
        .reset_index(name="facility_count")
    )


UI에서 사용할 데이터를 분석 함수가 반환하도록 한다.

분석 함수 내부에서:

st.write()
st.metric()
st.plotly_chart()


등을 호출하지 않는다.

16. VISUALIZATION RULES

시각화 코드는:

visualization/


에 둔다.

예:

def create_district_bar_chart(df):
    ...
    return fig


Streamlit page에서는:

fig = create_district_bar_chart(df)
st.plotly_chart(fig, use_container_width=True)


형태를 사용한다.

17. CORE CHARTS

MVP에서 다음 차트를 우선 구현한다.

Chart 1

자치구별 보안 인프라 수

→ Horizontal Bar Chart

Chart 2

시설 유형별 분포

→ Donut Chart

Chart 3

자치구 × 시설 유형

→ Heatmap

Chart 4

지역별 시설 수 비교

→ Bar Chart

Chart 5

연도별 설치 추이

→ Line Chart

단, 실제 데이터에 날짜/연도 정보가 충분하지 않으면
연도별 추이를 구현하지 않는다.

18. MAP VISUALIZATION

지도는 MVP의 핵심 시각화 요소 중 하나이다.

가능한 경우:

서울 지도
    ↓
시설 위치 표시
    ↓
시설 유형별 색상
    ↓
필터 적용


지도 구현 시 좌표가 없는 데이터는 지도에 표시하지 않는다.

잘못된 좌표를 임의로 생성하지 않는다.

19. STREAMLIT PAGE STRUCTURE
Main

서비스 소개 및 핵심 KPI.

SEOUL SECURITY INFRASTRUCTURE INSIGHT

서울지역 보안 인프라 데이터 분석

[전체 시설]
[자치구 수]
[시설 유형]
[데이터 수]

Page 1 — Overview

전체 서울지역 현황.

기능:

전체 시설 수
자치구별 시설 수
시설 유형별 분포
주요 차트
Page 2 — Regional Analysis

지역 중심 분석.

Sidebar:

자치구
[전체]

시설 유형
[전체]


출력:

선택 지역 KPI
지역별 비교
시설 유형별 비교
지도
Page 3 — Security Infrastructure

시설 중심 분석.

예:

시설 유형
[CCTV ▼]


출력:

시설 수
자치구별 분포
지도
설치 연도
상세 데이터
Page 4 — Statistics

분석 결과를 표 중심으로 제공한다.

예:

자치구 | 전체시설 | CCTV | 보안등 | 비상벨
-------------------------------------------
강남구 | ...
송파구 | ...
관악구 | ...

20. COMMON UI COMPONENTS

공통 UI는 여러 페이지에서 재사용할 수 있도록 만든다.

필수 컴포넌트:

Header
Sidebar
KPI Cards
Section Title
Info Card
Data Table
Empty State
Loading State


예:

render_header()

render_kpi_cards()

render_section_title("자치구별 시설 현황")

render_result_table(df)


각 페이지에서 동일한 UI 코드를 복사하지 않는다.

21. SIDEBAR RULE

Sidebar 필터는 가능한 한 공통 컴포넌트로 만든다.

예:

지역
[전체 ▼]

시설 유형
[전체 ▼]

설치년도
[전체 ▼]


필터 결과는 DataFrame으로 반환한다.

filtered_df = render_sidebar_filters(df)

22. KPI RULE

KPI는 다음 원칙을 따른다.

전체 시설
1,234

자치구
25

시설 유형
5

평균 시설 수
49.3


KPI 숫자는 분석 결과에서 계산한다.

임의의 숫자를 하드코딩하지 않는다.

Mock Data 단계에서는 Mock Data임을 명시한다.

23. TABLE RULE

표는 분석 결과를 확인할 수 있도록 제공한다.

가능하면:

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


를 사용한다.

불필요하게 모든 원본 데이터를 화면에 출력하지 않는다.

필요한 컬럼만 선택한다.

24. DATA VALIDATION

데이터를 사용하기 전에 최소한 다음을 확인한다.

필수 컬럼 존재
결측값
중복값
좌표 이상값
시설 유형
자치구


예:

required_columns = [
    "facility_id",
    "district",
    "facility_type",
    "latitude",
    "longitude",
]


필수 컬럼이 없으면 조용히 실패하지 말고
명확한 오류 메시지를 제공한다.

25. MISSING DATA

결측값을 무조건 0으로 변경하지 않는다.

예:

인구 데이터 없음


을:

인구 = 0


으로 처리하면 안 된다.

분석 의미가 달라질 수 있다.

가능한 경우:

Unknown
N/A
결측


등으로 구분한다.

26. API / EXTERNAL DATA RULE

현재 단계에서는 외부 API를 구현하지 않는다.

다음 기능은 후순위다.

공공데이터 API
서울시 API
외부 REST API
웹 크롤링
Requests
BeautifulSoup
Selenium
Playwright


현재 UI와 분석 구조는 Mock Data로 개발한다.

실제 API가 연결되더라도
분석 및 UI 코드를 최대한 변경하지 않는 것을 목표로 한다.

27. FUTURE DATA SOURCE

향후 실제 데이터 연결 시:

공공데이터
    ↓
API / CSV
    ↓
Raw Data
    ↓
Preprocessing
    ↓
Analysis
    ↓
Dashboard


구조를 사용한다.

API 구현은 별도의 모듈로 분리한다.

예:

data_sources/
├── public_api.py
├── csv_loader.py
└── crawler.py


현재는 생성하지 않아도 된다.

28. NO FAKE DATA RULE

실제 데이터가 없는 경우 Mock Data를 사용할 수 있다.

하지만 Mock Data를 실제 통계처럼 표현하지 않는다.

금지:

서울 강남구의 실제 CCTV 수는 1,234개이다.


허용:

※ 현재 화면은 개발용 Mock Data입니다.

29. SECURITY

다음 정보는 절대 코드에 작성하지 않는다.

API Key
Token
Password
Secret
개인 식별 정보

환경 변수:

.env


사용.

예:

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")


.env는 Git에 올리지 않는다.

30. .GITIGNORE

최소 다음을 포함한다.

.env
.env.*
!.env.example

.venv/
__pycache__/
*.pyc

.pytest_cache/
.ruff_cache/

.ipynb_checkpoints/

.DS_Store
Thumbs.db

*.log

31. CODING STYLE

Python:

PEP 8 준수
함수명은 snake_case
클래스명은 PascalCase
상수는 UPPER_SNAKE_CASE
의미가 명확한 변수명 사용

예:

district_facility_count


좋음.

x


가능하면 피한다.

32. FUNCTION RULE

하나의 함수가 너무 많은 역할을 수행하지 않도록 한다.

나쁜 예:

def process_everything():
    # 데이터 로딩
    # 전처리
    # 분석
    # 차트
    # Streamlit 출력


좋은 예:

load_data()
preprocess_data()
analyze_data()
create_chart()
render_page()

33. IMPORT RULE

가능하면 모듈 역할에 맞는 import 구조를 유지한다.

예:

from analysis.regional_analysis import (
    get_district_facility_count,
)

from visualization.charts import (
    create_district_bar_chart,
)

from components.metrics import (
    render_kpi_cards,
)


분석 모듈이 Streamlit UI 모듈을 import하지 않도록 한다.

34. STREAMLIT CACHE

비용이 큰 데이터 로딩 또는 계산에는 Streamlit cache를 사용할 수 있다.

예:

@st.cache_data
def load_data():
    ...


단순한 계산까지 무조건 cache 처리하지 않는다.

35. ERROR HANDLING

에러를 무조건 숨기지 않는다.

잘못된 예:

try:
    ...
except:
    pass


금지.

가능하면 구체적인 예외를 처리한다.

try:
    ...
except FileNotFoundError:
    ...


사용자가 이해할 수 있는 오류 메시지를 제공한다.

36. TESTING

코드를 수정한 후 최소한 다음을 확인한다.

Python Import
uv run python -c "import app"

Streamlit
uv run streamlit run app.py

분석 모듈
uv run python -c "from analysis.regional_analysis import *; print('OK')"

Mock Data

Mock Data로 페이지가 정상 실행되는지 확인한다.

37. STREAMLIT TEST

페이지에서 다음을 확인한다.

[ ] 앱 실행
[ ] 페이지 이동
[ ] Sidebar 표시
[ ] 지역 필터
[ ] 시설 유형 필터
[ ] KPI 변경
[ ] Chart 출력
[ ] Table 출력
[ ] 지도 출력
[ ] 데이터 없음 상태

38. UI TEST

가능하면 Playwright를 이용해 다음을 확인한다.

페이지 접속
↓
Sidebar 확인
↓
필터 선택
↓
화면 변경 확인
↓
Chart 확인
↓
Table 확인


UI 테스트를 하지 않은 경우
"UI 테스트 완료"라고 보고하지 않는다.

39. DEVELOPMENT WORKFLOW

Agent는 코드를 수정하기 전에 반드시:

1. AGENTS.md 확인
2. 현재 디렉토리 확인
3. 관련 파일 확인
4. 기존 코드 확인
5. 변경 범위 결정
6. 구현
7. 테스트
8. 결과 보고


순서를 따른다.

40. BEFORE CODING

사용자가 특정 기능을 요청하면
먼저 다음을 확인한다.

현재 파일 존재 여부
현재 함수 존재 여부
현재 import 구조
현재 데이터 구조
현재 Streamlit 구조


이미 구현된 기능을 새로 만들지 않는다.

41. MINIMAL CHANGE RULE

요청받은 기능에 필요한 최소 범위만 수정한다.

예:

사용자가:

Sidebar 필터 수정


을 요청한 경우

다음은 임의로 변경하지 않는다.

데이터 구조
API
크롤러
분석 알고리즘
다른 페이지
Git 설정
42. API / CRAWLER PROTECTION

다음 디렉토리는 현재 단계에서 보호한다.

crawler/
data_sources/


사용자가 명시적으로 요청하지 않는 이상
수정하지 않는다.

API 연결이 필요한 경우에도 먼저 사용자에게 확인한다.

43. DEPENDENCY RULE

새로운 패키지가 필요하다고 판단되면
바로 설치하지 않는다.

먼저:

uv pip list


를 확인한다.

기존 라이브러리로 해결 가능한지 판단한다.

새 패키지가 반드시 필요하다면:

왜 필요한지
어떤 대체 방법이 있는지
어떤 패키지를 추가하는지


를 먼저 사용자에게 설명한다.

44. DATA STRUCTURE PROTECTION

다음 데이터 계약을 임의로 변경하지 않는다.

facility_id
district
facility_type
facility_name
latitude
longitude
address
installed_year
count


컬럼을 변경해야 한다면
관련된 분석 / 시각화 / 페이지 전체 영향을 확인한다.

45. NO UNREQUESTED REFACTORING

사용자가 요청하지 않은 대규모 리팩터링을 하지 않는다.

특히 다음 작업을 임의로 하지 않는다.

디렉토리 구조 변경
파일 대량 이동
함수 전체 재작성
라이브러리 변경
패키지 교체
데이터 구조 변경
46. DESTRUCTIVE ACTIONS

다음 작업은 반드시 사용자 승인을 받는다.

git reset --hard
git clean
git push --force
Git history 변경
파일 대량 삭제
data/raw 전체 삭제
data/processed 전체 삭제
패키지 대량 제거
.venv 삭제

47. GIT WORKFLOW

기본 branch:

main
develop


기능 개발:

feature/기능명


예:

feature/common-ui
feature/regional-analysis
feature/security-map
feature/mock-data


가능하면 main에 직접 push하지 않는다.

48. COMMIT MESSAGE

Conventional Commit 사용.

예:

feat: 서울 보안 인프라 Mock Data 추가
feat: 지역별 시설 분석 함수 구현
feat: 공통 KPI 컴포넌트 추가
feat: 자치구별 보안 인프라 차트 추가
feat: Streamlit 지역 분석 페이지 추가

fix: 지역 필터 오류 수정
refactor: 차트 함수 분리
docs: 프로젝트 문서 수정
chore: uv dependency 업데이트

49. TASK EXECUTION RULE

큰 작업은 작은 작업으로 나눈다.

예:

Task: Regional Analysis

Subtask 1
Mock Data 확인

Subtask 2
지역별 집계 함수

Subtask 3
차트 생성

Subtask 4
Streamlit 연결

Subtask 5
필터 테스트


한 번에 모든 파일을 수정하지 않는다.

50. PAGE DEVELOPMENT RULE

새로운 Streamlit 페이지를 만들 때:

1. 기존 공통 컴포넌트 확인
2. 필요한 분석 함수 확인
3. 필요한 차트 확인
4. Page 구현
5. Mock Data 실행
6. UI 검증


순서를 따른다.

페이지 안에서 공통 UI를 새로 복사하지 않는다.

51. MOCK DATA DEVELOPMENT RULE

실제 데이터가 없더라도 모든 페이지가 실행되어야 한다.

따라서:

실제 데이터 존재
    ↓
실제 데이터 사용

실제 데이터 없음
    ↓
Mock Data 사용


구조를 사용할 수 있다.

단, 이 fallback 구조가 실제 데이터 오류를 숨기지 않도록
명확한 상태 표시를 제공한다.

52. UI DESIGN

전체 서비스의 UI는 일관성을 유지한다.

기본 스타일:

Primary Color
Dark Navy / Blue

Accent
Security Blue

Background
Light Gray

Card
White

Warning
Orange

Danger
Red


보안 인프라 서비스라는 성격에 맞게
과도하게 화려한 디자인은 피한다.

53. PAGE LAYOUT

가능하면 다음 구조를 사용한다.

Header
↓
Description
↓
Filters
↓
KPI
↓
Main Visualization
↓
Secondary Visualization
↓
Data Table


중요한 정보가 위에 오도록 한다.

54. CHART RULE

차트에는 최소한 다음을 고려한다.

제목
축 이름
단위
범례
데이터 정렬
적절한 색상

숫자만 표시하고 의미가 없는 차트를 만들지 않는다.

55. DATA INTERPRETATION

분석 결과를 사실 이상으로 해석하지 않는다.

예를 들어:

A지역에 CCTV가 많다.


와

A지역이 다른 지역보다 안전하다.


는 동일하지 않다.

보안 인프라 데이터만으로 범죄율이나 안전도를 단정하지 않는다.

56. IMPORTANT ANALYTICAL LIMITATIONS

다음 사항을 항상 고려한다.

보안 인프라가 많다고 해서
해당 지역이 반드시 안전한 것은 아니다.

시설 수가 적다고 해서
해당 지역이 반드시 위험한 것도 아니다.

인구, 면적, 유동인구, 범죄 발생 데이터 등이 없으면
밀도나 안전도에 대한 해석을 제한한다.

데이터가 측정하지 않은 것을 추측하지 않는다.

57. AI / LLM RULE

LLM은 현재 MVP의 필수 기능이 아니다.

사용자가 명시적으로 요청하지 않는 한
LLM 기능을 추가하지 않는다.

현재 우선순위:

데이터
↓
분석
↓
시각화
↓
Streamlit


LLM은 이후 확장 기능으로 고려한다.

58. API FUTURE PHASE

향후 실제 데이터 연결 단계에서는:

Phase 1
Mock Data

Phase 2
CSV / 정적 데이터

Phase 3
공공데이터

Phase 4
API

Phase 5
자동 수집


순서로 확장하는 것을 권장한다.

현재 단계에서는 Phase 1~2에 집중한다.

59. COMPLETION CRITERIA

기능을 "완료"라고 보고하기 전에 확인한다.

[ ] 코드 작성
[ ] import 오류 없음
[ ] Mock Data 실행
[ ] Streamlit 실행
[ ] UI 확인
[ ] 필터 확인
[ ] Chart 확인
[ ] Table 확인
[ ] 오류 상태 확인


검증하지 않은 기능은 완료라고 보고하지 않는다.

60. FINAL REPORT FORMAT

작업 완료 후 Agent는 다음 형식으로 보고한다.

## 작업 완료

### 변경 파일
- components/...
- analysis/...
- visualization/...
- pages/...

### 구현 내용
- ...
- ...
- ...

### 테스트
- uv run python ...
- uv run streamlit run app.py
- ...

### 확인 결과
- 정상 / 실패

### 미구현
- API
- 실제 데이터 연결
- ...

### 주의사항
- Mock Data 사용
- ...

61. ABSOLUTE RULES

다음 규칙은 항상 우선한다.

기존 코드를 먼저 확인한다.
AGENTS.md를 먼저 읽는다.
사용자 요구 범위를 벗어나지 않는다.
API와 크롤러를 임의로 수정하지 않는다.
실제 데이터가 없으면 Mock Data를 사용한다.
Mock Data를 실제 데이터처럼 표현하지 않는다.
분석과 UI를 분리한다.
공통 UI는 재사용한다.
중복 코드를 만들지 않는다.
새 패키지를 임의로 설치하지 않는다.
.env를 Git에 포함하지 않는다.
API Key를 코드에 작성하지 않는다.
테스트하지 않은 기능을 완료라고 하지 않는다.
대규모 리팩터링을 임의로 하지 않는다.
파괴적 작업은 반드시 승인받는다.
불확실한 사항은 추측하지 말고 먼저 확인한다.
데이터가 말하지 않는 내용을 임의로 해석하지 않는다.
현재 MVP를 먼저 완성하고 확장 기능은 나중에 구현한다.
