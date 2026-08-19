"""Streetlight source coverage page."""

import streamlit as st
from streamlit_folium import st_folium

from utils.crime_streetlight_loader import load_streetlight_data
from visualization.crime_streetlight_charts import streetlight_map

st.set_page_config(page_title="서울 가로등 설치 현황", page_icon="💡", layout="wide")


def main() -> None:
    st.title("서울 가로등 설치 현황")
    lights = load_streetlight_data()
    st.warning(
        "원본 CSV에는 자치구, 주소, 설치연도가 없습니다. 좌표만으로 자치구를 추정하지 않았으므로 자치구별 수·인구 1,000명당 가로등 수·연도 추이는 제공하지 않습니다."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("서울 전체 가로등 위치", f"{len(lights):,}개")
    c2.metric("평균 자치구별 가로등 수", "계산 불가")
    c3.metric("가장 많은 자치구", "판별 불가")
    c4.metric("가장 적은 자치구", "판별 불가")
    st.subheader("가로등 위치 지도")
    st.caption(
        "성능을 위해 유효 좌표 최대 5,000개를 표시합니다. 원본에는 시설 유형을 모두 streetlight로 표준화했습니다."
    )
    st_folium(
        streetlight_map(lights),
        use_container_width=True,
        height=580,
        returned_objects=[],
    )
    st.subheader("가로등 표준 Schema")
    st.dataframe(lights.head(200), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
