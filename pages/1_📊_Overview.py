"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Page 1: Overview Dashboard
"""

import streamlit as st
from utils.data_loader import load_security_data
from analysis.regional_analysis import (
    get_facility_count_by_district,
    get_facility_count_by_type,
    get_district_facility_crosstab,
)
from analysis.statistics import get_kpi_metrics, get_yearly_facility_count
from visualization.charts import (
    create_district_bar_chart,
    create_facility_type_donut_chart,
    create_district_facility_heatmap,
    create_yearly_facility_line_chart,
)
from components.header import render_header
from components.sidebar import render_sidebar_filters
from components.metrics import render_kpi_cards
from components.tables import render_result_table
from components.cards import render_section_title, render_empty_state

# 1. Streamlit 페이지 설정
st.set_page_config(
    page_title="Overview | 서울 보안 인프라",
    page_icon="📊",
    layout="wide",
)


def main():
    # 2. 공통 헤더 및 DEMO DATA 안내
    render_header()

    # 3. 데이터 로딩 & 전처리 (Data Loader 계층 사용)
    df, is_mock, source_name = load_security_data()

    # 4. 공통 Sidebar 필터 적용
    filtered_df = render_sidebar_filters(df)


    if filtered_df is None or filtered_df.empty:
        render_empty_state("선택하신 조건에 해당하는 보안 인프라 데이터가 없습니다.")
        return

    # 5. KPI Cards 렌더링 (실제 설치 수량 count 기준)
    kpis = get_kpi_metrics(filtered_df)
    render_section_title("📌 주요 현황 KPI 지표")
    render_kpi_cards(
        total_count=kpis["total_count"],
        district_count=kpis["district_count"],
        type_count=kpis["type_count"],
        avg_count=kpis["avg_per_district"],
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 6. 메인 차트 2개 컬럼 배치 (자치구별 바 차트 & 시설 유형별 도넛 차트)
    col1, col2 = st.columns([1.2, 1])

    with col1:
        render_section_title("🏙️ 자치구별 보안 인프라 설치 수")
        dist_counts = get_facility_count_by_district(filtered_df)
        fig_dist = create_district_bar_chart(dist_counts)
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        render_section_title("🍩 시설 유형별 설치 비중")
        type_counts = get_facility_count_by_type(filtered_df)
        fig_type = create_facility_type_donut_chart(type_counts)
        st.plotly_chart(fig_type, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 7. 자치구 x 시설 유형 Heatmap
    render_section_title("🌡️ 자치구 × 시설 유형 분포 Heatmap")
    crosstab_df = get_district_facility_crosstab(filtered_df)
    fig_heatmap = create_district_facility_heatmap(crosstab_df)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 8. 연도별 설치 추이 (Line Chart)
    render_section_title("📈 연도별 보안 인프라 신규 설치 추이")
    yearly_df = get_yearly_facility_count(filtered_df)
    if not yearly_df.empty and len(yearly_df) > 1:
        fig_yearly = create_yearly_facility_line_chart(yearly_df)
        st.plotly_chart(fig_yearly, use_container_width=True)
    else:
        render_empty_state("연도별 설치 추이를 분석하기에 충분한 데이터가 없습니다.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 9. 자치구별 요약 Table
    render_section_title("📋 자치구별 보안 인프라 집계표 (Summary Table)")
    render_result_table(crosstab_df, title="자치구별 / 시설유형별 수량 집계")


if __name__ == "__main__":
    main()
