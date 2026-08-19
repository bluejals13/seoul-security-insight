# Testing & Verification Rules (Always-On)

> **적용 시점 (Trigger)**: 모든 코드 변경 후 또는 작업 완료 시 반드시 수행하는 공통 검증 규칙  
> **적용 대상 (Scope)**: 프로젝트 전체 (`*`)

---

## 1. 공통 검증 원칙
- 코드 작성 및 수정 후 단순 "완료" 보고를 금지하며, 반드시 검증 명령을 실행하고 결과를 확인한다.
- 코드 수정 후에는 기존 기능이 정상 동작하는지 회귀(Regression) 여부를 확인한다.

---

## 2. 코드 수정 후 7단계 순차 검증 라이프사이클
코드 수정 완료 시 반드시 아래 순서대로 검증을 수행한다:
1. **Python import 테스트**: 모듈 간 의존성 및 syntax 오류 확인
2. **데이터 loader 테스트**: `utils/data_loader.py` 데이터 로딩 동작 확인
3. **preprocessing 테스트**: `analysis/preprocessing.py` 데이터 전처리 확인
4. **analysis 테스트**: `analysis/` 통계 분석 및 연산 로직 확인
5. **visualization 테스트**: `visualization/` Plotly 차트 및 Folium 지도 생성 확인
6. **Streamlit 실행 테스트**: `uv run streamlit run app.py` 명령으로 서버 정상 구동 확인
7. **브라우저 렌더링 테스트**: (가능한 경우) 실제 브라우저 UI 렌더링 및 인터랙션 확인

---

## 3. 기본 실행 및 검증 명령
```bash
uv run streamlit run app.py
```
