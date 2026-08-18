"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Sidebar Filter Component
"""

from typing import Optional, List
import pandas as pd
import streamlit as st
from config.settings import FACILITY_TYPES, SEOUL_DISTRICTS


def filter_data(
    df: pd.DataFrame,
    selected_district: str = "전체",
    selected_type: str = "전체",
    selected_year: str = "전체",
) -> pd.DataFrame:
    """Sidebar 필터 선택 조건에 따라 DataFrame을 필터링하는 헬퍼 함수

    Args:
        df (pd.DataFrame): 원본 DataFrame
        selected_district (str): 선택된 자치구 ("전체" 또는 특정 자치구)
        selected_type (str): 선택된 시설 유형 ("전체" 또는 특정 시설 유형)
        selected_year (str): 선택된 설치 연도 ("전체" 또는 연도 수치/문자열)

    Returns:
        pd.DataFrame: 필터링된 DataFrame
    """
    if df is None or df.empty:
        return pd.DataFrame()

    filtered_df = df.copy()

    # 1. 자치구 필터 적용
    if selected_district != "전체" and "district" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["district"] == selected_district]

    # 2. 시설 유형 필터 적용
    if selected_type != "전체" and "facility_type" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["facility_type"] == selected_type]

    # 3. 설치 연도 필터 적용
    if selected_year != "전체" and "installed_year" in filtered_df.columns:
        try:
            year_val = int(selected_year)
            filtered_df = filtered_df[filtered_df["installed_year"] == year_val]
        except (ValueError, TypeError):
            pass

    return filtered_df


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Streamlit Sidebar 필터를 UI에 표시하고 선택된 조건에 따라 필터링된 DataFrame 반환

    Args:
        df (pd.DataFrame): 원본 DataFrame

    Returns:
        pd.DataFrame: 선택 조건이 적용된 필터링 DataFrame
    """
    st.sidebar.markdown("## 🔍 검색 & 필터")
    st.sidebar.markdown("---")

    # 자치구 선택 옵션
    district_options = ["전체"] + SEOUL_DISTRICTS
    selected_district = st.sidebar.selectbox(
        "📍 자치구 선택",
        options=district_options,
        index=0,
        help="특정 자치구를 선택하거나 전체 서울시 현황을 탐색합니다.",
    )

    # 시설 유형 선택 옵션
    type_options = ["전체"] + FACILITY_TYPES
    selected_type = st.sidebar.selectbox(
        "🛡️ 시설 유형 선택",
        options=type_options,
        index=0,
        help="CCTV, 보안등, 비상벨 등 시설 유형별로 필터링합니다.",
    )

    # 설치 연도 선택 옵션 (데이터에 존재하는 연도 추출)
    year_options = ["전체"]
    if df is not None and not df.empty and "installed_year" in df.columns:
        valid_years = df["installed_year"].dropna().astype(int).unique()
        sorted_years = [str(y) for y in sorted(valid_years, reverse=True)]
        year_options.extend(sorted_years)

    selected_year = st.sidebar.selectbox(
        "📅 설치 연도 선택",
        options=year_options,
        index=0,
        help="특정 연도에 신규 설치된 보안 인프라를 조회합니다.",
    )

    st.sidebar.markdown("---")
    
    # 필터링 수행
    filtered_df = filter_data(
        df,
        selected_district=selected_district,
        selected_type=selected_type,
        selected_year=selected_year,
    )

    # 필터 결과 요약 표시
    total_raw = len(df) if df is not None else 0
    total_filtered = len(filtered_df)
    st.sidebar.caption(f"📊 조회 결과: {total_filtered:,} / {total_raw:,} 건")

    return filtered_df
