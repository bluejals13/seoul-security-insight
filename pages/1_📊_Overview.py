"""Integrated overview retaining the established component-oriented page structure."""

import streamlit as st

from analysis.crime_streetlight_analysis import build_comparison_dataset
from components.cards import (
    render_empty_state,
    render_info_card,
    render_section_title,
    render_warning_card,
)
from components.header import render_header
from components.metrics import render_analysis_metrics
from components.sidebar import render_crime_filters
from components.tables import render_result_table
from utils.crime_streetlight_loader import (
    load_crime_data,
    load_population_data,
    load_streetlight_data,
    quality_report,
)
from visualization.crime_streetlight_charts import (
    crime_count_bar,
    crime_heatmap,
    crime_type_pie,
)

st.set_page_config(
    page_title="Overview | 서울 범죄율·가로등", page_icon="📊", layout="wide"
)


def main() -> None:
    """Render the former dashboard flow with the new, scoped source data."""
    render_header()
    crime, population, lights = (
        load_crime_data(),
        load_population_data(),
        load_streetlight_data(),
    )
    filtered = render_crime_filters(crime)
    if filtered.empty:
        render_empty_state("선택한 조건에 해당하는 범죄 발생 데이터가 없습니다.")
        return

    totals = filtered[filtered["crime_type"] == "소계"]
    total_count = int(totals["crime_count"].sum()) if not totals.empty else 0
    max_district = (
        totals.loc[totals["crime_count"].idxmax(), "district"]
        if not totals.empty
        else "-"
    )
    render_section_title(
        "📌 주요 현황 KPI 지표", "각 원본의 실제 기준 시점을 유지해 표시합니다."
    )
    render_analysis_metrics(
        [
            ("범죄 발생 건수", f"{total_count:,}건"),
            ("범죄 발생 최다 자치구", max_district),
            ("2026년 6월 등록인구", f"{int(population['population'].sum()):,}명"),
            ("가로등 위치 레코드", f"{len(lights):,}개"),
        ]
    )

    render_section_title("데이터 출처 및 기준")
    render_info_card(
        "로컬 원본 CSV",
        "범죄: 2024년 5대 범죄 발생현황 / 등록인구: 2026년 6월 / 가로등: 관리번호·위도·경도 위치 정보",
    )
    comparison, reason = build_comparison_dataset(crime, population, lights)
    if reason:
        render_warning_card(reason)
    else:
        st.success(f"{len(comparison)}개 자치구의 결합 분석을 생성했습니다.")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1.2, 1])
    with left:
        render_section_title("🏙️ 자치구별 범죄 발생 건수")
        st.plotly_chart(crime_count_bar(totals), use_container_width=True)
    with right:
        render_section_title("🍩 범죄 유형별 발생 비중")
        type_counts = (
            filtered[filtered["crime_type"] != "소계"]
            .groupby("crime_type", as_index=False)["crime_count"]
            .sum()
        )
        st.plotly_chart(crime_type_pie(type_counts), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("🌡️ 자치구 × 범죄 유형 분포 Heatmap")
    heatmap_data = filtered[filtered["crime_type"] != "소계"]
    if heatmap_data.empty:
        render_empty_state("범죄 유형별 발생 데이터를 표시할 수 없습니다.")
    else:
        st.plotly_chart(crime_heatmap(heatmap_data), use_container_width=True)

    render_section_title("📋 자치구별 범죄 집계표")
    render_result_table(
        filtered.sort_values(["district", "crime_type"]),
        title="자치구별 / 범죄유형별 발생 건수",
    )
    with st.expander("데이터 품질 검증 결과"):
        st.json(quality_report(crime, population, lights))
    st.caption(
        "가로등 자치구 매핑과 동일연도 인구가 제공되기 전까지 범죄율·가로등 밀도·4분면 분석은 비활성화됩니다."
    )


if __name__ == "__main__":
    main()
