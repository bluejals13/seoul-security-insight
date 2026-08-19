"""Shared analysis-year selection UI."""

from __future__ import annotations

import streamlit as st

from utils.crime_streetlight_loader import (
    DEFAULT_ANALYSIS_YEAR,
    available_analysis_years,
    source_years,
)


def render_analysis_year_selector(*, key: str) -> int | None:
    """Render a selectable source year and its actual dataset-year labels."""
    years = available_analysis_years()
    if not years:
        st.error("분석에 사용할 5대 범죄 또는 등록인구 원본 파일을 찾을 수 없습니다.")
        return None

    default_index = years.index(DEFAULT_ANALYSIS_YEAR) if DEFAULT_ANALYSIS_YEAR in years else 0
    year = st.selectbox("분석 기준 연도", years, index=default_index, key=key)
    actual_years = source_years(year)
    status = " · ".join(
        f"{label}: {actual_years[name]}" if actual_years[name] is not None else f"{label}: 없음"
        for name, label in (("crime", "범죄"), ("population", "인구"), ("streetlight", "가로등"))
    )
    st.caption(f"분석 기준 연도: {year} · {status}")
    if actual_years["crime"] is None or actual_years["population"] is None:
        st.warning(
            f"{year}년 범죄와 등록인구 데이터가 모두 있어야 분석할 수 있습니다. "
            "다른 연도 데이터로 대체하지 않습니다."
        )
    return year
