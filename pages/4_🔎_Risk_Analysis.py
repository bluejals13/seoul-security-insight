"""Crime-rate and streetlight comparison page."""

import streamlit as st

from analysis.crime_streetlight_analysis import (
    build_comparison_dataset,
    classify_quadrants,
)
from utils.crime_streetlight_loader import (
    load_crime_data,
    load_population_data,
    load_streetlight_data,
)
from visualization.crime_streetlight_charts import risk_scatter

st.set_page_config(
    page_title="범죄율·가로등 설치 수준 분석", page_icon="🔎", layout="wide"
)


def main() -> None:
    st.title("범죄율 · 가로등 설치 수준 분석")
    st.caption(
        "상관 탐색 결과이며, 가로등이 범죄를 유발하거나 예방한다는 인과관계를 의미하지 않습니다."
    )
    data, reason = build_comparison_dataset(
        load_crime_data(), load_population_data(), load_streetlight_data()
    )
    if reason:
        st.error(reason)
        st.info(
            "현재 원본만으로는 district, crime_rate, crime_count, population, streetlight_count, streetlights_per_1000_people를 신뢰성 있게 결합할 수 없습니다."
        )
        return
    basis = st.radio("4분면 기준", ["평균", "중앙값"], horizontal=True)
    classified, cutoffs = classify_quadrants(data, basis)
    st.caption(
        f"{basis} 기준: 범죄율 {cutoffs['crime_rate']:.2f}, 가로등 밀도 {cutoffs['streetlight_density']:.2f}"
    )
    st.plotly_chart(risk_scatter(classified), use_container_width=True)
    st.subheader("우선관찰지역")
    st.write(
        "상대적으로 높은 범죄율과 낮은 가로등 밀도를 동시에 보이는 지역입니다. 인과 판단이 아닌 관찰 우선순위입니다."
    )
    st.dataframe(
        classified[classified.quadrant.str.startswith("🔴")],
        use_container_width=True,
        hide_index=True,
    )
    st.dataframe(classified, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
