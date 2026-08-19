# 서울쉴더스 (Seoul Shielders) - AI Agent Guidelines

이 프로젝트는 **서울지역 보안 인프라 분석 및 지도 기반 치안 정보 서비스** 구축 프로젝트입니다.
모든 작업 수행 시 본 문서와 `.agents/` 디렉터리의 규칙, 스킬, 워크플로우를 준수해야 합니다.

---

## 1. 상시 적용 규칙 (Always-On Rules)

다음 규칙은 프로젝트의 모든 작업에서 항시 적용됩니다.

- 🛡️ [core.md](file:///.agents/rules/core.md): 최상위 아키텍처 원칙, 기존 코드 보호, Mock Data 계층 분리, 민감정보 보호
- 🧪 [testing.md](file:///.agents/rules/testing.md): 코드 수정 후 필수 7단계 검증 라이프사이클 및 실행 명령

---

## 2. 동적 온디맨드 스킬 (On-Demand Skills)

특정 도메인 작업을 수행할 때는 해당 Skill의 명세(`SKILL.md`)를 확인하고 적용합니다.

- 🐍 [python](file:///.agents/skills/python/SKILL.md): Python 3.12 스펙, `uv` 패키지 관리, 타입 힌트, 모듈화 작성 스타일
- 📊 [data-analysis](file:///.agents/skills/data-analysis/SKILL.md): 데이터 수집, Schema, 전처리, 통계 분석, API 연동, Mock/Fallback
- 🎨 [streamlit-ui](file:///.agents/skills/streamlit-ui/SKILL.md): Streamlit UI, `app.py`, `pages/`, `components/`, UI와 로직 분리
- 🗺️ [visualization](file:///.agents/skills/visualization/SKILL.md): Plotly 차트, Folium 지도, 기존 시각화 보호, 서울 25개 자치구 범위
- 🔒 [security](file:///.agents/skills/security/SKILL.md): API Key, `.env`, `st.secrets`, 개인정보 보호, Git 노출 방지
- 🐙 [git](file:///.agents/skills/git/SKILL.md): Git 브랜치, 커밋, PR, 배포 저장소 설정 수칙

---

## 3. 작업 절차 (Workflows)

특정 작업 진행 시 아래 절차 문서(`file:///.agents/workflows/...`)에 따라 단계별로 작업을 진행합니다.

- 🚀 [feature.md](file:///.agents/workflows/feature.md): 새로운 기능 개발 절차
- 🐞 [bugfix.md](file:///.agents/workflows/bugfix.md): 버그 수정 절차
- 📈 [data-analysis.md](file:///.agents/workflows/data-analysis.md): 데이터 분석 및 데이터 소스 연동 개발 절차
- 🖥️ [ui-change.md](file:///.agents/workflows/ui-change.md): UI/레이아웃 변경 절차

---

## 4. 필수 실행 명령
- **앱 실행 명령**: `uv run streamlit run app.py`
