"""Crime occurrence and rate page."""

import streamlit as st

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
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("서울 전체 범죄 발생 건수", f"{int(total_only.crime_count.sum()):,}건")
    k2.metric("서울 평균 범죄율", "계산 불가")
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
    st.warning(
        f"범죄 데이터는 {year}년, 등록인구 데이터는 {sorted(population.year.unique())}년 {population.period.iloc[0]} 기준입니다. 연도가 일치하지 않아 인구 1만 명당 범죄율은 계산하지 않았습니다."
    )
    st.subheader("자치구별 범죄 발생 건수 (소계)")
    st.plotly_chart(crime_count_bar(total_only), use_container_width=True)
    left, right = st.columns(2)
    with left:
        st.subheader("범죄 유형별 발생 비중")
        st.plotly_chart(
            crime_type_pie(
                filtered[filtered.crime_type != "소계"]
                .groupby("crime_type", as_index=False)
                .crime_count.sum()
            ),
            use_container_width=True,
        )
    with right:
        st.subheader("자치구 × 범죄유형")
        st.plotly_chart(
            crime_heatmap(filtered[filtered.crime_type != "소계"]),
            use_container_width=True,
        )
    st.subheader("자치구 상세")
    st.dataframe(
        filtered.sort_values(["district", "crime_type"]),
        use_container_width=True,
        hide_index=True,
    )


if __name__ == "__main__":
    main()
