"""Seoul crime-rate and streetlight analysis landing page."""

import streamlit as st

from analysis.crime_streetlight_analysis import build_comparison_dataset
from components.analysis_year import render_analysis_year_selector
from utils.crime_streetlight_loader import (
    SourceDataError,
    load_crime_data,
    load_population_data,
    load_streetlight_data,
    quality_report,
    source_years,
)
from utils.district_boundary_loader import (
    load_district_boundaries,
    spatial_join_streetlights,
    validate_district_boundaries,
)

st.set_page_config(page_title="서울 범죄율·가로등 분석", page_icon="💡", layout="wide")


def main() -> None:
    st.title("서울 자치구별 범죄율과 가로등 설치 수준")
    st.caption(
        "범죄 발생과 가로등 설치 수준의 공간적·통계적 관계를 탐색합니다. 인과관계를 주장하지 않습니다."
    )
    analysis_year = render_analysis_year_selector(key="landing-analysis-year")
    if analysis_year is None:
        return
    try:
        crime, population, lights = (
            load_crime_data(analysis_year),
            load_population_data(analysis_year),
            load_streetlight_data(),
        )
    except SourceDataError as exc:
        st.error(str(exc))
        return
    boundaries = load_district_boundaries()
    joined_lights, spatial_report = spatial_join_streetlights(lights, boundaries)
    years = source_years(analysis_year)
    comparison, reason = build_comparison_dataset(
        crime, population, joined_lights, analysis_year, years["streetlight"]
    )
    report = quality_report(crime, population, joined_lights, validate_district_boundaries(boundaries), spatial_report, comparison)
    c1, c2, c3 = st.columns(3)
    c1.metric(
        f"{analysis_year}년 서울 5대 범죄 발생",
        f"{int(crime.loc[crime['crime_type'] == '소계', 'crime_count'].sum()):,}건",
    )
    c2.metric(f"{analysis_year}년 등록인구", f"{int(population['population'].sum()):,}명")
    c3.metric("가로등 위치 레코드", f"{len(lights):,}개")
    st.subheader("데이터 출처")
    st.write(
        f"- 범죄: {analysis_year}년 5대 범죄 발생현황\n- 인구: {analysis_year}년 등록인구\n- 가로등: {years['streetlight']}년 위치 자료 (WGS84 위도·경도)\n- 경계: `data/reference/서울시 상권분석서비스(영역-자치구).shp` (EPSG:5181)"
    )
    if reason:
        st.warning(reason)
        st.info("원본 데이터와 공간결합 결과를 확인하세요.")
    else:
        st.success(f"{len(comparison)}개 자치구 비교 데이터를 생성했습니다.")
    with st.expander("데이터 품질 검증 결과"):
        st.json(report)
    st.caption("왼쪽 페이지 메뉴에서 범죄 발생, 가로등 위치, 비교 분석을 확인하세요.")


if __name__ == "__main__":
    main()
