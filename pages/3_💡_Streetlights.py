"""Streetlight source coverage page."""

import streamlit as st
from streamlit_folium import st_folium

from utils.crime_streetlight_loader import load_streetlight_data
from utils.district_boundary_loader import (
    load_district_boundaries,
    spatial_join_streetlights,
)
from visualization.crime_streetlight_charts import streetlight_map

st.set_page_config(page_title="서울 가로등 설치 현황", page_icon="💡", layout="wide")


@st.cache_data(show_spinner="자치구 경계와 가로등 위치를 결합하는 중입니다…")
def load_joined_streetlights():
    """Reuse the shared boundary loader for the page-level presentation data."""
    return spatial_join_streetlights(
        load_streetlight_data(), load_district_boundaries()
    )


def render_accessible_styles() -> None:
    """Keep Streamlit's layout while raising text contrast and readable sizes."""
    st.markdown(
        """
        <style>
        .stMainBlockContainer {max-width: 1440px; padding-top: 2rem;}
        h1, h2, h3 {color: #102A43 !important; font-weight: 750 !important; letter-spacing: -0.02em;}
        h1 {font-size: clamp(2rem, 4vw, 2.8rem) !important;}
        h2 {font-size: clamp(1.4rem, 2.5vw, 1.85rem) !important; margin-top: 1.7rem !important;}
        [data-testid="stMetricLabel"] {color: #243B53 !important; font-size: 1rem !important; font-weight: 700 !important;}
        [data-testid="stMetricValue"] {color: #102A43 !important; font-size: clamp(1.55rem, 3vw, 2.25rem) !important; font-weight: 800 !important;}
        [data-testid="stMetric"] {background: #F8FBFF; border: 1px solid #B8D4E8; border-radius: 10px; padding: 1rem; min-height: 8.2rem;}
        .streetlight-note {background: #EAF4FF; border-left: 5px solid #1479B8; color: #102A43; padding: 1rem 1.15rem; border-radius: 6px; font-size: 1rem; line-height: 1.6; margin: 0.75rem 0 1.25rem;}
        .streetlight-note strong {color: #0B4F7C;}
        [data-testid="stDataFrame"] {border: 1px solid #B8D4E8; border-radius: 8px;}
        [data-testid="stDataFrame"] * {color: #102A43 !important; font-size: 0.92rem !important;}
        @media (max-width: 640px) {
          .stMainBlockContainer {padding-left: 1rem; padding-right: 1rem;}
          [data-testid="stMetric"] {min-height: 6.8rem; padding: 0.8rem;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    render_accessible_styles()
    st.title("서울 가로등 설치 현황")
    lights, spatial_report = load_joined_streetlights()
    assigned = lights.dropna(subset=["district"])
    district_counts = (
        assigned.groupby("district").size().reindex(load_district_boundaries()["district"], fill_value=0)
    )
    max_district, min_district = district_counts.idxmax(), district_counts.idxmin()
    st.markdown(
        """
        <div class="streetlight-note">
        <strong>공간결합 기준</strong><br>
        원본에는 자치구·주소·설치연도가 없으며, WGS84 좌표와 자치구 경계(EPSG:5181)의 공간결합으로 자치구를 산출합니다.
        좌표 이상과 경계 밖 위치는 어느 자치구에도 임의 배정하지 않습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )
    first_row = st.columns(3)
    second_row = st.columns(2)
    c1, c2, c3 = first_row
    c4, c5 = second_row
    c1.metric("서울 전체 가로등 위치", f"{len(lights):,}개")
    c2.metric("자치구 배정 가로등", f"{spatial_report['streetlight_spatial_join_assigned_count']:,}개")
    c3.metric("평균 자치구별 가로등 수", f"{district_counts.mean():,.1f}개")
    c4.metric("가장 많은 자치구", f"{max_district} · {district_counts[max_district]:,}개")
    c5.metric("가장 적은 자치구", f"{min_district} · {district_counts[min_district]:,}개")
    st.subheader("가로등 위치 지도")
    st.write(
        "성능을 위해 유효 좌표 최대 5,000개를 표시합니다. 지도 tooltip과 popup에는 공간결합으로 산출한 자치구를 함께 표시합니다."
    )
    st_folium(
        streetlight_map(lights),
        width="stretch",
        height=580,
        returned_objects=[],
    )
    st.write(
        f"품질 검증: 전체 {spatial_report['streetlight_total_count']:,}건 · 자치구 배정 {spatial_report['streetlight_spatial_join_assigned_count']:,}건 · 미배정 {spatial_report['streetlight_unassigned_total_count']:,}건 (좌표 이상 {spatial_report['streetlight_invalid_coordinate_count']:,}건, 경계 밖 {spatial_report['streetlight_outside_boundary_count']:,}건)"
    )
    st.subheader("가로등 표준 Schema")
    st.dataframe(lights.head(200), width="stretch", hide_index=True)


if __name__ == "__main__":
    main()
