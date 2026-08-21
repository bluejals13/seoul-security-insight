import streamlit as st

from Style.theme_white_css import WHITE_CSS
from Style.theme_dark_css import DARK_CSS


def _init_theme() -> None:
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False


def apply_runtime_theme() -> None:
    _init_theme()

    css = DARK_CSS if st.session_state.dark_mode else WHITE_CSS

    st.markdown(
        css,
        unsafe_allow_html=True,
    )


def render_theme_toggle() -> None:
    _init_theme()

    with st.sidebar:
        st.divider()

        st.toggle(
            "🌙 다크 모드",
            key="dark_mode",
            help="라이트 모드와 다크 모드를 전환합니다.",
        )

        st.caption(
            "현재 테마: "
            + ("다크" if st.session_state.dark_mode else "라이트")
        )
