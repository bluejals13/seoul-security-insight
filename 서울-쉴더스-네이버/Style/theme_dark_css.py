"""
🌙 서울 쉴더스 다크 테마 CSS

런타임 테마 전환에서 사용하는 색상 및 CSS를 정의한다.
"""

# ---------------------------------------------------------------------------
# 색상 팔레트
# ---------------------------------------------------------------------------

PRIMARY = "#66BB6A"
BG = "#0E1117"
SECONDARY_BG = "#1A2020"
TEXT = "#E8F5E9"
TEXT_MUTED = "#A5C8A8"
SPINNER_BORDER = "#2E4A30"

BORDER = "#30363D"
CARD_BG = "#151A1A"
INPUT_BG = "#1A2020"


# ---------------------------------------------------------------------------
# 전체 앱 다크 테마
# ---------------------------------------------------------------------------

DARK_CSS = f"""
<style>

/* =========================================================
   전체 앱
   ========================================================= */

.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

[data-testid="stAppViewContainer"] {{
    background-color: {BG};
}}

[data-testid="stMain"] {{
    background-color: {BG};
    color: {TEXT};
}}


/* =========================================================
   사이드바
   ========================================================= */

[data-testid="stSidebar"] {{
    background-color: {CARD_BG};
}}

[data-testid="stSidebar"] * {{
    color: {TEXT};
}}


/* =========================================================
   제목 / 본문
   ========================================================= */

h1, h2, h3, h4, h5, h6 {{
    color: {TEXT};
}}

p, li, label {{
    color: {TEXT};
}}

.stCaption,
[data-testid="stCaptionContainer"] {{
    color: {TEXT_MUTED};
}}


/* =========================================================
   Metric
   ========================================================= */

div[data-testid="stMetric"] {{
    background-color: {SECONDARY_BG};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 12px;
}}

div[data-testid="stMetricLabel"] {{
    color: {TEXT_MUTED};
}}

div[data-testid="stMetricValue"] {{
    color: {TEXT};
}}


/* =========================================================
   버튼
   ========================================================= */

.stButton > button {{
    background-color: {SECONDARY_BG};
    color: {TEXT};
    border: 1px solid {BORDER};
}}

.stButton > button:hover {{
    border-color: {PRIMARY};
    color: {PRIMARY};
}}


/* =========================================================
   입력창 / Selectbox / Radio
   ========================================================= */

[data-baseweb="select"] > div {{
    background-color: {INPUT_BG};
    color: {TEXT};
    border-color: {BORDER};
}}

[data-baseweb="select"] span {{
    color: {TEXT};
}}

[data-baseweb="popover"] {{
    background-color: {SECONDARY_BG};
}}

[data-baseweb="menu"] {{
    background-color: {SECONDARY_BG};
}}

[data-baseweb="menu"] li {{
    color: {TEXT};
}}

[data-baseweb="menu"] li:hover {{
    background-color: {CARD_BG};
}}


/* =========================================================
   Text input
   ========================================================= */

input {{
    background-color: {INPUT_BG} !important;
    color: {TEXT} !important;
    border-color: {BORDER} !important;
}}


/* =========================================================
   Expander
   ========================================================= */

[data-testid="stExpander"] {{
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
}}

[data-testid="stExpander"] summary {{
    color: {TEXT};
}}


/* =========================================================
   Dataframe
   ========================================================= */

[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
}}


/* =========================================================
   Divider
   ========================================================= */

hr {{
    border-color: {BORDER};
}}


/* =========================================================
   Streamlit 기본 UI 제거
   ========================================================= */

footer {{
    visibility: hidden;
}}

div[data-testid="stDecoration"] {{
    display: none;
}}


/* =========================================================
   페이지 전환
   ========================================================= */

@keyframes fadeSlideIn {{
    from {{
        opacity: 0;
        transform: translateY(6px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

div[data-testid="stMain"]
div[data-testid="stElementContainer"]:not(:has(iframe)) {{
    animation: fadeSlideIn 0.28s ease-out;
}}

</style>
"""


# ---------------------------------------------------------------------------
# GPS 대기 스피너
# ---------------------------------------------------------------------------

GPS_WAIT_SPINNER_HTML = f"""
<style>
@keyframes gpsSpin {{
    to {{
        transform: rotate(360deg);
    }}
}}
</style>

<div style="
    display:flex;
    align-items:center;
    gap:12px;
    padding:16px;
    background:{SECONDARY_BG};
    border:1px solid {BORDER};
    border-radius:8px;
    margin-bottom:8px;
">

    <div style="
        width:22px;
        height:22px;
        border-radius:50%;
        flex-shrink:0;
        border:3px solid {SPINNER_BORDER};
        border-top-color:{PRIMARY};
        animation:gpsSpin 0.8s linear infinite;
    "></div>

    <span style="
        font-size:14px;
        color:{TEXT};
    ">
        브라우저가 위치 권한을 물어보면 허용해주세요.
        내 위치를 가져오는 중입니다...
    </span>

</div>
"""


# ---------------------------------------------------------------------------
# 별도 사용용 CSS
# ---------------------------------------------------------------------------

HIDE_STREAMLIT_CHROME_CSS = """
<style>
footer {
    visibility: hidden;
}

div[data-testid="stDecoration"] {
    display: none;
}
</style>
"""


PAGE_TRANSITION_CSS = """
<style>
@keyframes fadeSlideIn {
    from {
        opacity: 0;
        transform: translateY(6px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

div[data-testid="stMain"]
div[data-testid="stElementContainer"]:not(:has(iframe)) {
    animation: fadeSlideIn 0.28s ease-out;
}
</style>
"""
