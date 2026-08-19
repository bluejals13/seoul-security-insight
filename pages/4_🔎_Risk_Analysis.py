"""Interactive 25-district crime and streetlight map."""

import streamlit as st
from streamlit_folium import st_folium

from analysis.crime_streetlight_analysis import (
    build_comparison_dataset,
    classify_quadrants,
)
from utils.crime_streetlight_loader import (
    load_crime_data,
    load_population_data,
    load_streetlight_data,
    quality_report,
)
from utils.district_boundary_loader import (
    load_district_boundaries,
    spatial_join_streetlights,
    validate_district_boundaries,
)
from visualization.crime_streetlight_charts import risk_scatter
from visualization.district_analysis_map import (
    METRIC_OPTIONS,
    create_district_analysis_map,
)

st.set_page_config(page_title="자치구 범죄·가로등 지도", page_icon="🔎", layout="wide")


@st.cache_data(show_spinner="자치구 경계와 가로등 위치를 결합하는 중입니다…")
def load_analysis_data():
    """Load immutable sources and return only analysis-ready in-memory frames."""
    boundaries = load_district_boundaries()
    streetlights, spatial_report = spatial_join_streetlights(load_streetlight_data(), boundaries)
    data, reason = build_comparison_dataset(load_crime_data(), load_population_data(), streetlights)
    return boundaries, streetlights, spatial_report, data, reason


def main() -> None:
    st.title("서울 자치구 범죄 · 가로등 분석 지도")
    st.caption(
        "가로등은 2023년 위치자료, 범죄·등록인구는 2024년 자료입니다. 가로등 밀도는 참고용 설치 밀도이며 인과관계를 의미하지 않습니다."
    )
    boundaries, streetlights, spatial_report, data, reason = load_analysis_data()
    if reason:
        st.error(reason)
        return
    metric_label = st.radio("지도 색상 지표", list(METRIC_OPTIONS), horizontal=True)
    map_result = st_folium(
        create_district_analysis_map(boundaries, data, metric_label),
        width="stretch",
        height=630,
        returned_objects=["last_active_drawing"],
        key=f"district-map-{metric_label}",
    )
    clicked = (map_result.get("last_active_drawing") or {}).get("properties", {}).get("district")
    districts = data["district"].tolist()
    selected = st.selectbox(
        "상세 분석 자치구",
        districts,
        index=districts.index(clicked) if clicked in districts else 0,
    )
    detail = data.loc[data["district"] == selected].iloc[0]
    a, b, c = st.columns(3)
    a.metric("2024년 5대 범죄 발생", f"{detail.crime_count_2024:,.0f}건")
    b.metric("인구 1만 명당 범죄율", f"{detail.crime_rate_per_10000:,.2f}건")
    c.metric("2023년 가로등", f"{detail.streetlight_count_2023:,.0f}개")
    st.metric("인구 1,000명당 가로등 수", f"{detail.streetlights_per_1000_people:,.2f}개", help="2023년 설치 위치 기준의 참고용 설치 밀도")

    st.subheader("25개 자치구 비교")
    chart_data, _ = classify_quadrants(data)
    st.plotly_chart(risk_scatter(chart_data), width="stretch")
    st.dataframe(data, width="stretch", hide_index=True)

    report = quality_report(
        load_crime_data(), load_population_data(), streetlights,
        validate_district_boundaries(boundaries), spatial_report, data,
    )
    with st.expander("데이터 품질 검증"):
        st.json(report)


if __name__ == "__main__":
    main()
