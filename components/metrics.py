"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - KPI Metrics Component
"""

import streamlit as st
from config.settings import COLOR_PALETTE


def render_kpi_cards(
    total_count: int,
    district_count: int,
    type_count: int,
    avg_count: float,
) -> None:
    """분석 결과에서 계산된 KPI 지표 카드를 표시

    Args:
        total_count (int): 총 시설 수량 (count 합계)
        district_count (int): 분석 자치구 수
        type_count (int): 시설 유형 수
        avg_count (float): 자치구당 평균 시설 수량
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div style="
                background-color: {COLOR_PALETTE['card']};
                padding: 16px 20px;
                border-radius: 8px;
                border-left: 4px solid {COLOR_PALETTE['accent']};
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
                <p style="margin: 0; font-size: 13px; color: #64748B; font-weight: 500;">전체 시설 수량</p>
                <h3 style="margin: 4px 0 0 0; font-size: 24px; color: {COLOR_PALETTE['primary']}; font-weight: 700;">
                    {total_count:,} <span style="font-size: 14px; font-weight: 400;">개</span>
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="
                background-color: {COLOR_PALETTE['card']};
                padding: 16px 20px;
                border-radius: 8px;
                border-left: 4px solid #10B981;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
                <p style="margin: 0; font-size: 13px; color: #64748B; font-weight: 500;">분석 자치구 수</p>
                <h3 style="margin: 4px 0 0 0; font-size: 24px; color: {COLOR_PALETTE['primary']}; font-weight: 700;">
                    {district_count} <span style="font-size: 14px; font-weight: 400;">개 구</span>
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="
                background-color: {COLOR_PALETTE['card']};
                padding: 16px 20px;
                border-radius: 8px;
                border-left: 4px solid #8B5CF6;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
                <p style="margin: 0; font-size: 13px; color: #64748B; font-weight: 500;">시설 유형 수</p>
                <h3 style="margin: 4px 0 0 0; font-size: 24px; color: {COLOR_PALETTE['primary']}; font-weight: 700;">
                    {type_count} <span style="font-size: 14px; font-weight: 400;">개 유형</span>
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div style="
                background-color: {COLOR_PALETTE['card']};
                padding: 16px 20px;
                border-radius: 8px;
                border-left: 4px solid #F59E0B;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
                <p style="margin: 0; font-size: 13px; color: #64748B; font-weight: 500;">구별 평균 시설 수</p>
                <h3 style="margin: 4px 0 0 0; font-size: 24px; color: {COLOR_PALETTE['primary']}; font-weight: 700;">
                    {avg_count:,.1f} <span style="font-size: 14px; font-weight: 400;">개</span>
                </h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
