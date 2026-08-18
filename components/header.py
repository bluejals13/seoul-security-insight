"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Header Component
"""

import streamlit as st
from config.settings import MOCK_DATA_NOTICE, COLOR_PALETTE


def render_header() -> None:
    """공통 서비스 헤더 및 DEMO DATA 안내 표시"""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {COLOR_PALETTE['secondary']} 0%, {COLOR_PALETTE['primary']} 100%);
            padding: 24px 32px;
            border-radius: 12px;
            color: #FFFFFF;
            margin-bottom: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        ">
            <h1 style="margin: 0 0 8px 0; font-size: 28px; font-weight: 700; color: #FFFFFF;">
                🛡️ SEOUL SECURITY INFRASTRUCTURE INSIGHT
            </h1>
            <p style="margin: 0 0 16px 0; font-size: 16px; color: #94A3B8;">
                서울지역 보안 인프라 데이터 분석 Dashboard
            </p>
            <p style="margin: 0; font-size: 13px; color: #CBD5E1; line-height: 1.5;">
                서울시 25개 자치구별 CCTV, 보안등, 비상벨, 방범시설, 안전시설 등 주요 보안 인프라의 
                지역별·유형별 분포 현황을 다각도로 탐색하고 비교 분석합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # DEMO DATA 경고 안내 메시지
    st.warning(f"ℹ️ {MOCK_DATA_NOTICE}")
