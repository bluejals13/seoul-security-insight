"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Main Application Entrypoint
"""

import streamlit as st
from utils.data_loader import load_security_data
from analysis.statistics import get_kpi_metrics
from components.header import render_header
from components.metrics import render_kpi_cards
from components.cards import render_info_card, render_section_title

# 1. Streamlit 페이지 설정
st.set_page_config(
    page_title="서울시 보안 인프라 인사이트",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    # 2. 공통 헤더 및 DEMO DATA 안내
    render_header()

    # 3. 데이터 로딩 & 전처리 (Data Loader)
    df, is_mock, source_name = load_security_data()

    # 4. 전체 KPI 지표 계산 및 표시
    kpis = get_kpi_metrics(df)

    render_section_title("📌 서울시 보안 인프라 종합 요약 (Summary KPI)")
    render_kpi_cards(
        total_count=kpis["total_count"],
        district_count=kpis["district_count"],
        type_count=kpis["type_count"],
        avg_count=kpis["avg_per_district"],
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. 서비스 개요 및 사이드바 안내 카드
    render_info_card(
        title="🔍 대시보드 이용 가이드",
        content=(
            "왼쪽 사이드바의 <b>Pages 메뉴</b>를 통해 상세 분석 페이지로 이동할 수 있습니다.<br>"
            "• <b>1_📊_Overview</b>: 서울시 25개 자치구 전체의 보안 인프라 현황, 시설 유형별 비중, 분포 Heatmap, 연도별 추이를 종합 탐색합니다.<br>"
            "※ 현재 화면에 표시되는 모든 통계 수치 및 지도는 서비스 UI 검증용 Mock Data입니다."
        ),
    )


if __name__ == "__main__":
    main()
