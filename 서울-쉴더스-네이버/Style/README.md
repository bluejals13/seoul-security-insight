# 스타일(테마) 관리 — Style/

이 폴더는 **서울 쉴더스** 앱의 화이트/다크 테마 설정을 한 곳에서 관리합니다.

## 파일 구성

| 파일 | 설명 |
|------|------|
| 	heme_white.toml | ☀️ 화이트 테마 — .streamlit/config.toml 전체 교체본 |
| 	heme_dark.toml | 🌙 다크 테마 — .streamlit/config.toml 전체 교체본 |
| 	heme_white_css.py | 화이트 테마 커스텀 CSS 상수 (pp.py에서 import 가능) |
| 	heme_dark_css.py | 다크 테마 커스텀 CSS 상수 (pp.py에서 import 가능) |
| pply_theme.py | CLI 헬퍼 — 원클릭으로 .streamlit/config.toml 교체 |

## 색상 팔레트

### ☀️ 화이트(라이트) 테마

| 역할 | 색상 코드 | 미리보기 |
|------|-----------|---------|
| Primary (브랜드) | #2E7D32 | 진초록 |
| 배경 | #FFFFFF | 흰색 |
| 보조 배경 | #F5F7F5 | 밝은 초록빛 회색 |
| 텍스트 | #1B1B1B | 거의 검정 |

### 🌙 다크 테마

| 역할 | 색상 코드 | 미리보기 |
|------|-----------|---------|
| Primary (브랜드) | #66BB6A | 밝은 초록 |
| 배경 | #0E1117 | 거의 검정 |
| 보조 배경 | #1A2020 | 어두운 초록빛 검정 |
| 텍스트 | #E8F5E9 | 거의 흰색 (옅은 초록 tint) |

> **다크 Primary를 #66BB6A로 올린 이유**  
> #2E7D32(진초록)는 어두운 배경(#0E1117) 위에서 명도 대비가 3:1 미만으로 WCAG AA 접근성 기준에 미달한다.  
> #66BB6A는 같은 초록 계열이면서 다크 배경 대비가 5:1 이상으로 안전하다.

## 테마 전환 방법

### 방법 1: CLI 헬퍼 사용 (권장)

`ash
# 프로젝트 루트에서 실행
python Style/apply_theme.py white   # ☀️ 화이트 테마 적용
python Style/apply_theme.py dark    # 🌙 다크 테마 적용
`

적용 후 Streamlit 서버를 재시작해야 반영됩니다.
`ash
# 서버 재시작
Ctrl+C  →  streamlit run frontend/app.py
`

> pply_theme.py는 교체 전에 기존 config.toml을 config.toml.bak으로 자동 백업합니다.

### 방법 2: 수동 복사

	heme_white.toml 또는 	heme_dark.toml 파일을  
rontend/.streamlit/config.toml로 덮어쓰기하세요.

## 커스텀 CSS 연동 (선택)

pp.py의 CSS 상수(하드코딩)를 테마 모듈에서 import하는 방식으로 바꾸면  
테마 교체 시 GPS 스피너 배경색 등 인라인 CSS도 자동으로 바뀝니다.

`python
# app.py 상단에서 테마 선택
from Style.theme_white_css import (
    HIDE_STREAMLIT_CHROME_CSS,
    PAGE_TRANSITION_CSS,
    GPS_WAIT_SPINNER_HTML,
)
# 다크로 바꿀 땐 theme_dark_css 로 교체
`

현재 pp.py의 CSS는 화이트 테마 값으로 하드코딩되어 있어 즉시 동작합니다.  
이 import 방식은 향후 앱 내 테마 토글 기능을 붙일 때를 위한 준비입니다.
