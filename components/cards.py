"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Common Cards & UI Components
"""

from typing import Optional
import streamlit as st
from config.settings import COLOR_PALETTE


def render_section_title(title: str, description: Optional[str] = None) -> None:
    """섹션 타이틀 및 가이드 설명 렌더링"""
    st.markdown(f"### {title}")
    if description:
        st.markdown(f"<p style='color: #64748B; font-size: 14px; margin-top: -8px;'>{description}</p>", unsafe_allow_html=True)


def render_info_card(title: str, content: str) -> None:
    """정보성 요약 카드 렌더링"""
    st.markdown(
        f"""
        <div style="
            background-color: {COLOR_PALETTE['card']};
            border: 1px solid #E2E8F0;
            border-left: 4px solid {COLOR_PALETTE['accent']};
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 16px;
        ">
            <h4 style="margin: 0 0 6px 0; color: {COLOR_PALETTE['primary']}; font-size: 16px;">{title}</h4>
            <p style="margin: 0; color: {COLOR_PALETTE['text']}; font-size: 14px; line-height: 1.5;">{content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(message: str = "표시할 데이터가 없습니다.") -> None:
    """데이터 없음 (Empty State) 메시지 표시"""
    st.markdown(
        f"""
        <div style="
            background-color: #F8FAFC;
            border: 1px dashed #CBD5E1;
            padding: 32px 20px;
            border-radius: 8px;
            text-align: center;
            color: #64748B;
            margin: 16px 0;
        ">
            <p style="margin: 0; font-size: 15px; font-weight: 500;">📭 {message}</p>
            <p style="margin: 4px 0 0 0; font-size: 13px; color: #94A3B8;">필터 조건을 변경하거나 다른 검색어를 입력해 보세요.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_warning_card(message: str) -> None:
    """경고 메시지 카드 렌더링"""
    st.markdown(
        f"""
        <div style="
            background-color: #FFF7ED;
            border: 1px solid #FFEDD5;
            border-left: 4px solid {COLOR_PALETTE['warning']};
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 16px;
        ">
            <p style="margin: 0; color: #C2410C; font-size: 14px; font-weight: 500;">⚠️ {message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
