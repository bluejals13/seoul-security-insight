"""Crime occurrence and rate page."""

import streamlit as st

from analysis.crime_streetlight_analysis import calculate_crime_rates
from utils.crime_streetlight_loader import load_crime_data, load_population_data
from visualization.crime_streetlight_charts import (
    crime_count_bar,
    crime_heatmap,
    crime_type_pie,
)

st.set_page_config(page_title="서울 지역별 범죄율 분석", page_icon="📈", layout="wide")


def main() -> None:
    st.title("서울 지역별 범죄율 분석")
    crime, population = load_crime_data(), load_population_data()
    years, districts, types = (
        sorted(crime.year.unique()),
        sorted(crime.district.unique()),
        sorted(crime.crime_type.unique()),
    )
    a, b, c = st.columns(3)
    year = a.selectbox("연도", years)
    selected_districts = b.multiselect("자치구", districts, default=districts)
    selected_types = c.multiselect("범죄 유형", types, default=types)
    filtered = crime[
        (crime.year == year)
        & crime.district.isin(selected_districts)
        & crime.crime_type.isin(selected_types)
    ]
    total_only = filtered[filtered.crime_type == "소계"]
    rated_totals = calculate_crime_rates(total_only, population)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("서울 전체 범죄 발생 건수", f"{int(total_only.crime_count.sum()):,}건")
    k2.metric("자치구 평균 범죄율", f"{rated_totals.crime_rate.mean():,.2f}건" if not rated_totals.empty else "-")
    k3.metric(
        "발생이 가장 많은 자치구",
        total_only.loc[total_only.crime_count.idxmax(), "district"]
        if not total_only.empty
        else "-",
    )
    k4.metric(
        "발생이 가장 적은 자치구",
        total_only.loc[total_only.crime_count.idxmin(), "district"]
        if not total_only.empty
        else "-",
    )
    st.info(
        f"범죄와 등록인구 모두 {year}년 기준입니다. 인구 1만 명당 범죄율은 자치구별 총 발생건수를 등록인구로 나누어 계산합니다."
    )
    st.subheader("자치구별 범죄 발생 건수 (소계)")
    st.plotly_chart(crime_count_bar(total_only), width="stretch")
    left, right = st.columns(2)
    with left:
        st.subheader("범죄 유형별 발생 비중")
        st.plotly_chart(
            crime_type_pie(
                filtered[filtered.crime_type != "소계"]
                .groupby("crime_type", as_index=False)
                .crime_count.sum()
            ),
            width="stretch",
        )
    with right:
        st.subheader("자치구 × 범죄유형")
        st.plotly_chart(
            crime_heatmap(filtered[filtered.crime_type != "소계"]),
            width="stretch",
        )
    st.subheader("자치구 상세")
    st.dataframe(
        filtered.sort_values(["district", "crime_type"]),
        width="stretch",
        hide_index=True,
    )


if __name__ == "__main__":
    main()
