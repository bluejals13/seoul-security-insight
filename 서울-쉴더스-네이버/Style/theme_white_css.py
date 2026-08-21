"""
☀️ 서울 쉴더스 화이트 테마 CSS
"""

# ---------------------------------------------------------------------------
# 색상 팔레트
# ---------------------------------------------------------------------------

PRIMARY = "#2E7D32"
BG = "#FFFFFF"
SECONDARY_BG = "#F5F7F5"
TEXT = "#1B1B1B"
TEXT_MUTED = "#555555"

BORDER = "#E0E0E0"
CARD_BG = "#FFFFFF"
INPUT_BG = "#FFFFFF"

SPINNER_BORDER = "#C8E6C9"


# ---------------------------------------------------------------------------
# 전체 앱 라이트 테마
# ---------------------------------------------------------------------------

WHITE_CSS = f"""
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
    background-color: {SECONDARY_BG};
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

[data-testid="stCaptionContainer"] {{
    color: {TEXT_MUTED};
}}


/* =========================================================
   Metric
   ========================================================= */

div[data-testid="stMetric"] {{
    background-color: {CARD_BG};
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
    background-color: {CARD_BG};
    color: {TEXT};
    border: 1px solid {BORDER};
}}

.stButton > button:hover {{
    border-color: {PRIMARY};
    color: {PRIMARY};
}}


/* =========================================================
   Selectbox / Radio / 입력창
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
    background-color: {BG};
}}

[data-baseweb="menu"] {{
    background-color: {BG};
}}

[data-baseweb="menu"] li {{
    color: {TEXT};
}}

[data-baseweb="menu"] li:hover {{
    background-color: {SECONDARY_BG};
}}

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
# 공통 UI
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
