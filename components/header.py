"""Shared dashboard header."""

import streamlit as st

from config.settings import COLOR_PALETTE


def render_header() -> None:
    """Render the shared header for the current crime/streetlight scope."""
    st.markdown(
        f"""<div style="background:linear-gradient(135deg,{COLOR_PALETTE["secondary"]}, {COLOR_PALETTE["primary"]});padding:24px 32px;border-radius:12px;color:#fff;margin-bottom:24px"><h1 style="margin:0;font-size:28px">서울 범죄율 · 가로등 분석</h1><p style="margin:8px 0 0;color:#cbd5e1">자치구별 범죄 발생과 가로등 설치 수준을 실제 로컬 원본 데이터로 점검합니다.</p></div>""",
        unsafe_allow_html=True,
    )
