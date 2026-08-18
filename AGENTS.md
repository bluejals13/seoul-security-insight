

# 1. 프로젝트 개요

## 1.1 프로젝트명

**JOB INSIGHT**

## 1.2 프로젝트 목적

IT 채용공고와 GitHub 개발 생태계 데이터를 수집·분석하여

- 현재 IT 채용시장에서 어떤 기술이 많이 요구되는지
- 직무별로 어떤 기술이 필요한지
- 신입과 경력의 기술 요구사항이 어떻게 다른지
- 채용시장과 GitHub의 기술 관심도가 어떻게 다른지
- 취업 준비생이 어떤 기술을 우선적으로 학습해야 하는지

를 데이터 기반으로 보여주는 서비스입니다.

---

# 2. 핵심 분석 질문

프로젝트는 아래 질문에 답하는 것을 목표로 합니다.

### Q1.
현재 IT 채용시장에서 가장 많이 요구되는 기술은 무엇인가?

### Q2.
Backend / Frontend / Data / AI·ML / DevOps 직무별 요구 기술은 어떻게 다른가?

### Q3.
신입과 경력 채용의 기술 요구사항은 어떻게 다른가?

### Q4.
채용시장에서 요구되는 기술과 GitHub에서 나타나는 개발 생태계의 관심도는 어떻게 다른가?

### Q5.
특정 직무를 희망하는 사용자에게 어떤 기술을 우선적으로 학습하도록 추천할 수 있는가?

---

# 3. 개발 원칙

## 원칙 1 — 완료 기준을 먼저 정의한다

개발 전에 해당 작업의 완료 조건을 확인합니다.

MVP 범위를 벗어나는 기능을 임의로 추가하지 않습니다.

### 요청 없이 추가하지 않는 기능

- 로그인
- 회원가입
- 사용자 DB
- 결제
- 관리자 페이지
- 복잡한 AI 추천
- 채팅 기능
- 불필요한 외부 서비스

필요한 경우 반드시 먼저 요구사항을 확정합니다.

---

## 원칙 2 — 조사 먼저, 구현 나중

외부 라이브러리/API/크롤링을 구현하기 전에 관련 공식 문서를 확인합니다.

특히 다음을 확인합니다.

1. 공식 API 존재 여부
2. 현재 사용 가능한 API 방식
3. 인증 방법
4. Rate Limit
5. 이용약관
6. robots.txt
7. 자동화 허용 여부
8. 현재 라이브러리 사용법

가능하면 공식 API를 우선 사용합니다.

---

## 원칙 3 — 버그는 원인 분석 후 수정한다

에러 발생 시 무작정 코드를 수정하지 않습니다.

다음 순서를 지킵니다.

```text
에러 확인
  ↓
발생 위치 확인
  ↓
재현
  ↓
원인 분석
  ↓
수정 방법 결정
  ↓
최소 범위 수정
  ↓
테스트


땜빵식 수정이나 원인 없는 코드 변경을 금지합니다.

4. 기술 스택
영역	기술
Language	Python 3.11+
Package Manager	uv
Data Collection	Requests
HTML Parser	BeautifulSoup4
Browser Automation	Selenium / Playwright
API	GitHub REST API
Data Processing	Pandas
Numerical	NumPy
Visualization	Plotly
Dashboard	Streamlit
Environment	python-dotenv
Version Control	Git / GitHub
AI Agent	Antigravity
MCP	Context7 / GitHub / Playwright / Task Master / Chrome DevTools
5. 프로젝트 디렉토리
job-insight/
│
├── app.py
├── AGENTS.md
├── README.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .env
├── .env.example
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── crawler/
│   ├── __init__.py
│   ├── job_crawler.py
│   └── github_api.py
│
├── data/
│   ├── raw/
│   │   ├── jobs_raw.csv
│   │   └── github_raw.csv
│   │
│   └── processed/
│       ├── jobs_clean.csv
│       └── tech_analysis.csv
│
├── analysis/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── eda.py
│   ├── tech_analysis.py
│   └── recommendation.py
│
├── visualization/
│   ├── __init__.py
│   └── charts.py
│
├── pages/
│   ├── 1_📊_Job_Market.py
│   ├── 2_💻_Tech_Trend.py
│   └── 3_🎯_Job_Recommendation.py
│
├── utils/
│   ├── __init__.py
│   └── common.py
│
└── notebooks/
    ├── 01_EDA.ipynb
    └── 02_Tech_Analysis.ipynb

6. 디렉토리 역할
app.py

Streamlit 서비스의 메인 진입점입니다.

실행:

streamlit run app.py

crawler/

외부 데이터 수집만 담당합니다.

job_crawler.py
→ 채용공고 수집

github_api.py
→ GitHub API 데이터 수집


Crawler에서 분석 로직을 수행하지 않습니다.

data/raw/

외부에서 수집한 원본 데이터를 저장합니다.

jobs_raw.csv
github_raw.csv


Raw 데이터는 가능한 한 그대로 보존합니다.

data/processed/

정제된 데이터를 저장합니다.

jobs_clean.csv
tech_analysis.csv

analysis/

분석 로직을 담당합니다.

preprocessing.py
→ 데이터 정제

eda.py
→ 탐색적 데이터 분석

tech_analysis.py
→ 기술 스택 분석

recommendation.py
→ 기술 추천

visualization/

Plotly 차트를 생성합니다.

분석 로직과 UI 코드를 분리합니다.

pages/

Streamlit 멀티페이지입니다.

Job Market
Tech Trend
Job Recommendation

7. 데이터 흐름

프로젝트의 기본 데이터 흐름은 절대 임의로 변경하지 않습니다.

채용 사이트
    ↓
Crawler
    ↓
data/raw/jobs_raw.csv
    ↓
Preprocessing
    ↓
data/processed/jobs_clean.csv
    ↓
Analysis
    ↓
Visualization
    ↓
Streamlit


GitHub 데이터:

GitHub API
    ↓
data/raw/github_raw.csv
    ↓
Analysis
    ↓
채용시장 데이터와 비교

8. 채용 데이터 표준

팀 전체가 동일한 데이터 스키마를 사용합니다.

필수 컬럼
job_id
company
title
job_category
experience
employment_type
location
description
required_skills
preferred_skills
posted_date
deadline
url
source


예:

job_id: 001
company: A회사
title: 백엔드 개발자
job_category: Backend
experience: 신입
location: 서울

9. GitHub 데이터 표준

기본 컬럼:

language
repository
stars
forks
open_issues
updated_at


필요한 경우 분석 목적에 맞는 컬럼을 추가할 수 있습니다.

10. 직무 분류

MVP에서는 아래 5개 직무를 사용합니다.

JOB_CATEGORIES = [
    "Backend",
    "Frontend",
    "Data",
    "AI/ML",
    "DevOps",
]


새로운 직무 추가 시 기존 필터와 분석 코드에 미치는 영향을 확인합니다.

11. 기술 스택

초기 분석 대상:

TECH_STACK = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "SQL",
    "C++",
    "Go",
    "Rust",

    "Spring",
    "Django",
    "FastAPI",
    "React",
    "Vue",
    "Next.js",

    "AWS",
    "Azure",
    "GCP",

    "Docker",
    "Kubernetes",

    "MySQL",
    "PostgreSQL",
    "Redis",

    "Git",
    "Linux",
]

12. 기술명 정규화

동일 기술의 표현 차이를 하나의 기술명으로 통일합니다.

TECH_ALIASES = {
    "Python": [
        "python",
        "python3",
    ],

    "JavaScript": [
        "javascript",
        "js",
    ],

    "TypeScript": [
        "typescript",
        "ts",
    ],

    "PostgreSQL": [
        "postgresql",
        "postgres",
    ],
}


예:

Python
python
Python3


→

Python


으로 통일합니다.

13. 채용공고 수집 원칙
정적 페이지
Requests
    ↓
HTML
    ↓
BeautifulSoup
    ↓
데이터 추출

동적 페이지
Selenium / Playwright
    ↓
페이지 로딩
    ↓
HTML
    ↓
BeautifulSoup
    ↓
데이터 추출

공식 API

가능한 경우:

API
 ↓
JSON
 ↓
DataFrame


방식을 우선합니다.

14. 크롤링 안전 규칙

크롤링 전 반드시 확인합니다.

이용약관
robots.txt
API 정책
자동화 허용 여부
Rate Limit
개인정보 포함 여부


과도한 요청을 보내지 않습니다.

HTTP 요청에는 timeout을 사용합니다.

requests.get(
    url,
    timeout=10,
)


브라우저 자동화 후에는 반드시 브라우저를 종료합니다.

15. Raw 데이터 보존 원칙

Raw 데이터는 분석 전에 수정하지 않습니다.

잘못된 구조:

Crawler
 ↓
바로 데이터 수정
 ↓
분석


올바른 구조:

Crawler
 ↓
Raw
 ↓
Preprocessing
 ↓
Processed
 ↓
Analysis


Raw 데이터는 문제가 발생했을 때 재처리할 수 있는 원본으로 사용합니다.

16. 전처리

analysis/preprocessing.py에서 담당합니다.

기본 처리:

컬럼명 정규화
중복 제거
결측치 처리
문자열 정리
날짜 정규화
기술명 정규화


예:

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

17. 기술 추출

채용공고의 description을 기반으로 기술을 추출합니다.

예:

Python과 FastAPI를 사용하며
AWS 및 Docker 경험자를 우대합니다.


↓

Python
FastAPI
AWS
Docker


기술 추출은 분석 단계에서 수행합니다.

Crawler는 원문 description을 최대한 보존합니다.

18. 핵심 분석
분석 1 — 전체 기술 수요

예:

Python      72%
SQL         68%
Java        61%
AWS         59%
Docker      51%


실제 수치는 수집한 데이터로 계산합니다.

분석 2 — 직무별 기술 수요

예:

Backend
Python
SQL
AWS
Docker

Frontend
JavaScript
TypeScript
React
Next.js

분석 3 — 신입 vs 경력

예:

             신입      경력

Python       72%      81%
SQL          68%      76%
AWS          45%      69%
Docker       31%      57%


실제 수치는 데이터로 계산합니다.

분석 4 — 채용시장 vs GitHub

두 데이터는 모집단과 수집 방법이 다릅니다.

따라서:

채용시장 비율 = 채용공고에서의 기술 등장 비율

GitHub 지표 = GitHub 데이터에서 측정한 기술 활동/관심 지표


로 정의합니다.

두 값을 동일한 의미의 비율로 표현하지 않습니다.

19. 시각화

핵심 그래프는 5개 이내로 제한합니다.

1. 전체 기술 순위

Bar Chart

2. 직무별 기술 비교

Grouped Bar Chart

3. 신입 vs 경력

Grouped Bar Chart

4. 채용시장 vs GitHub

Comparison Chart

5. 기간별 기술 추세

Line Chart

데이터가 충분할 경우에만 구현합니다.

20. Streamlit 화면
Main
💼 JOB INSIGHT

2026 IT 채용시장 기술 트렌드 분석

전체 공고
기업 수
직무 수
기술 수

Page 1 — Job Market

기능:

직무 필터
경력 필터
지역 필터
전체 공고 수
기업 수
직무별 채용 비중
Page 2 — Tech Trend

기능:

직무 선택
기술 수요 순위
직무별 기술 비교
신입/경력 비교
GitHub 비교
Page 3 — Recommendation

기능:

희망 직무
+
현재 보유 기술
↓
부족 기술 분석
↓
우선 학습 기술 추천

21. 추천 시스템

MVP에서는 규칙 기반으로 구현합니다.

예:

backend_skills = {
    "Python": 0.72,
    "SQL": 0.68,
    "AWS": 0.59,
    "Docker": 0.51,
    "FastAPI": 0.34,
}


사용자가:

Python


을 보유한 경우:

추천 학습 기술

1. SQL
2. AWS
3. Docker
4. FastAPI


추천 순서는 해당 직무에서의 기술 수요를 기준으로 합니다.

22. LLM 사용 원칙

LLM은 MVP 필수 기능이 아닙니다.

우선 다음 기능을 완성합니다.

수집
 ↓
전처리
 ↓
분석
 ↓
추천
 ↓
Streamlit


이후 시간이 남을 경우 LLM을 추가합니다.

가능한 확장:

채용공고
 ↓
LLM
 ↓
업무 요약
 ↓
필요 역량 분석
 ↓
학습 로드맵

23. 환경변수

API Key는 절대 코드에 직접 작성하지 않습니다.

.env

GITHUB_API_KEY=


.env.example

GITHUB_API_KEY=


Python:

from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")


API Key를 다음에 출력하지 않습니다.

console
log
Streamlit
Git
PR

24. Git Ignore

.gitignore에는 최소 다음을 포함합니다.

# Environment
.env
.env.*
!.env.example

# Python
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
*.egg-info/

# Node
node_modules/

# Build
dist/
build/

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS
.DS_Store
Thumbs.db

# IDE
.idea/

25. Git 협업
Branch 구조
main
  │
  └── develop
       │
       ├── feature/job-crawler
       ├── feature/job-crawler-selenium
       ├── feature/github-api
       ├── feature/preprocessing
       ├── feature/analysis
       ├── feature/streamlit
       └── feature/recommendation

작업 시작
git checkout develop
git pull origin develop
git checkout -b feature/기능명

Commit 규칙

Conventional Commit을 사용합니다.

feat: 채용공고 크롤러 구현
feat: GitHub API 수집 추가
fix: 기술 alias 추출 오류 수정
refactor: 전처리 함수 분리
docs: README 업데이트
chore: requirements 업데이트

Push
git add .
git commit -m "feat: 채용공고 크롤러 구현"
git push origin feature/job-crawler


이후 Pull Request를 생성합니다.

가능하면 main에 직접 push하지 않습니다.

26. 팀원 작업 분배

6~7명 기준:

담당	영역
A	채용 데이터 수집 1
B	채용 데이터 수집 2 / Selenium
C	GitHub API
D	전처리 / 기술 추출
E	통계 / 데이터 분석
F	시각화 / Streamlit
G	통합 / 추천 / 발표

단, 각 담당자는 자신의 코드가 다른 모듈과 연결될 수 있도록 공통 데이터 규격을 반드시 준수합니다.

27. MCP 사용 규칙

현재 프로젝트에서 사용하는 MCP:

Context7
GitHub
Playwright
Task Master AI
Chrome DevTools

Context7

라이브러리 사용법 및 최신 공식 문서 확인에 사용합니다.

라이브러리 API를 추측해서 구현하지 않습니다.

GitHub MCP

다음 작업에 사용합니다.

Repository 확인
파일 조회
Branch 확인
Issue 확인
Pull Request 확인
GitHub 작업
Playwright MCP

웹 페이지 및 Streamlit UI 테스트에 사용합니다.

검증 대상:

페이지 이동
필터
버튼
입력
차트 출력
추천 결과
Chrome DevTools MCP

브라우저 디버깅 및 렌더링 문제 분석에 사용합니다.

Task Master AI

개발 작업을 Task / Subtask 단위로 관리합니다.

예:

Task
├── 채용 크롤러
│   ├── URL 수집
│   ├── HTML 분석
│   └── CSV 저장
│
├── 전처리
│   ├── 결측치
│   ├── 중복
│   └── 기술명 정규화
│
└── Streamlit
    ├── Dashboard
    ├── Tech Trend
    └── Recommendation

28. AI Agent 작업 절차

AI Agent는 코드를 수정하기 전에 다음 순서를 따릅니다.

1. 사용자 요구사항 확인
        ↓
2. AGENTS.md 확인
        ↓
3. 현재 프로젝트 구조 확인
        ↓
4. 관련 파일 확인
        ↓
5. Context7 등 공식 문서 조사
        ↓
6. 영향 범위 분석
        ↓
7. 최소 범위 구현
        ↓
8. 테스트
        ↓
9. 변경 사항 요약


기존 파일을 확인하지 않고 새로운 파일을 임의로 생성하지 않습니다.

29. 파괴적 작업

다음 작업은 명시적인 승인 없이 수행하지 않습니다.

기존 코드 대규모 삭제
디렉토리 구조 대규모 변경
데이터 전체 삭제
Git history 변경
git push --force
API Key 변경/폐기
외부 서비스 삭제
패키지 대량 삭제

30. Notebook 규칙

Notebook은 분석 및 실험용입니다.

notebooks/
├── 01_EDA.ipynb
└── 02_Tech_Analysis.ipynb


Notebook에서 검증된 코드는 최종적으로 다음으로 이동합니다.

analysis/
visualization/


서비스 코드가 Notebook에만 존재해서는 안 됩니다.

31. 개발 일정
Day 1 — 설계 및 환경

목표:

GitHub Repository
       ↓
프로젝트 구조
       ↓
Python 환경
       ↓
데이터 규격 확정
       ↓
TECH_STACK 확정
       ↓
크롤링 테스트
       ↓
Streamlit 실행

완료 조건
Repository 생성
Branch 전략 확정
프로젝트 구조 생성
.gitignore 생성
.env.example 생성
jobs_raw.csv 컬럼 확정
TECH_STACK 확정
Streamlit 실행 성공
32. Day 2 — 데이터 수집

목표:

채용 사이트
    ↓
jobs_raw.csv

GitHub API
    ↓
github_raw.csv

완료 조건
실제 채용 데이터 확보
GitHub 데이터 확보
Raw CSV 생성
데이터 스키마 준수
33. Day 3 — 분석

목표:

Raw
 ↓
Preprocessing
 ↓
Technology Extraction
 ↓
Analysis
 ↓
Visualization Data

완료 조건
전체 기술 순위
직무별 기술 분석
신입 vs 경력 분석
GitHub 비교
핵심 그래프 생성
34. Day 4 — Streamlit

목표:

Analysis
 ↓
Plotly
 ↓
Streamlit

완료 조건
Dashboard
필터
Tech Trend
GitHub 비교
Recommendation
35. Day 5 — 통합

Day 5에는 새로운 기능을 최대한 추가하지 않습니다.

전체 시스템을 처음부터 끝까지 실행합니다.

Crawler
 ↓
Raw Data
 ↓
Preprocessing
 ↓
Analysis
 ↓
Visualization
 ↓
Recommendation
 ↓
Streamlit


발표 환경에서 한 번에 실행되는 것을 목표로 합니다.

36. MVP 범위
🔴 반드시 완성
채용 데이터 수집
        ↓
Requests / BeautifulSoup / Selenium
        ↓
Raw CSV
        ↓
Pandas 전처리
        ↓
기술 스택 추출
        ↓
직무별 분석
        ↓
신입/경력 분석
        ↓
GitHub API
        ↓
채용시장 vs GitHub 비교
        ↓
Plotly
        ↓
Streamlit
        ↓
기술 추천

🟡 시간이 남으면
지역별 분석
월별 트렌드
공고 검색
공고 상세 페이지

🟢 최종 확장
LLM
 ↓
채용공고 요약
 ↓
역량 분석
 ↓
개인 맞춤 학습 로드맵

37. Definition of Done

기능 완료를 선언하기 전에 반드시 검증합니다.

프로젝트 실행
streamlit run app.py


정상 실행되어야 합니다.

데이터

다음 파일이 정상적으로 생성되어야 합니다.

data/raw/jobs_raw.csv
data/raw/github_raw.csv
data/processed/jobs_clean.csv

데이터 품질

확인 항목:

[ ] 필수 컬럼 존재
[ ] 중복 데이터 처리
[ ] 결측치 처리
[ ] 기술명 정규화
[ ] 날짜 형식 통일
[ ] URL 정상 여부

분석

다음 분석이 정상적으로 실행되어야 합니다.

[ ] 전체 기술 수요
[ ] 직무별 기술 수요
[ ] 신입 vs 경력
[ ] 채용시장 vs GitHub

Streamlit
[ ] 메인 페이지 출력
[ ] 직무 필터
[ ] 경력 필터
[ ] 지역 필터
[ ] 기술 차트
[ ] 직무별 기술 분석
[ ] 신입/경력 비교
[ ] GitHub 비교
[ ] 기술 추천

보안
[ ] .env Git 제외
[ ] API Key 하드코딩 없음
[ ] API Key 로그 출력 없음
[ ] .env.example 존재

Git
[ ] feature branch 사용
[ ] 의미 있는 commit
[ ] PR 생성
[ ] develop 기준 충돌 확인
[ ] main 직접 push 없음

38. 최종 서비스 구조

전체 시스템은 다음 구조를 유지합니다.

                     ┌──────────────────┐
                     │   채용 사이트    │
                     └────────┬─────────┘
                              ↓
                    crawler/job_crawler.py
                              ↓
                         jobs_raw.csv
                              ↓
                  analysis/preprocessing.py
                              ↓
                        jobs_clean.csv
                              ↓
                   analysis/tech_analysis.py
                              ↓
               ┌──────────────┼──────────────┐
               ↓              ↓              ↓
            직무 분석       경력 분석       기술 분석
               │              │              │
               └──────────────┼──────────────┘
                              ↓
                   visualization/charts.py
                              ↓
                         Streamlit
                              ↑
                              │
                  analysis/recommendation.py
                              ↑
                              │
                       GitHub API

39. 최종 목표

JOB INSIGHT의 최종 목표는 단순히 채용공고를 보여주는 것이 아닙니다.

사용자가 다음 질문에 답을 얻도록 하는 것입니다.

"내가 원하는 IT 직무에 취업하려면 어떤 기술을 우선적으로 준비해야 하는가?"

이를 위해:

채용시장 데이터
       +
GitHub 데이터
       ↓
데이터 수집
       ↓
전처리
       ↓
기술 추출
       ↓
직무/경력별 분석
       ↓
시각화
       ↓
사용자 기술 비교
       ↓
🎯 학습 기술 추천


의 전체 파이프라인을 완성합니다.

40. Agent 최종 행동 규칙

AI Agent는 항상 다음을 우선합니다.

기존 코드와 구조를 먼저 확인한다.
AGENTS.md 규칙을 따른다.
데이터 규격을 임의로 변경하지 않는다.
공식 문서를 먼저 확인한다.
최소 범위만 수정한다.
API Key를 노출하지 않는다.
파괴적 작업은 승인받는다.
구현 후 반드시 테스트한다.
테스트하지 않은 기능을 "완료"라고 보고하지 않는다.
MVP 범위를 벗어나는 기능은 임의로 구현하지 않는다.


