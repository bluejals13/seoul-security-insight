"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Table Component
"""


import pandas as pd
import streamlit as st


def render_result_table(
    df: pd.DataFrame,
    columns: list[str] | None = None,
    title: str | None = None,
    height: int | None = None,
) -> None:
    """분석 결과 DataFrame을 깔끔하게 테이블 형태로 렌더링

    Args:
        df (pd.DataFrame): 표시할 DataFrame
        columns (list, optional): 화면에 노출할 컬럼 선택 리스트
        title (str, optional): 테이블 상단 타이틀
        height (int, optional): 테이블 높이
    """
    if title:
        st.markdown(f"##### 📋 {title}")

    if df is None or df.empty:
        st.info("ℹ️ 조건에 해당하는 표 데이터가 없습니다.")
        return

    display_df = df.copy()

    # 특정 컬럼 선택 지정 시 처리
    if columns:
        valid_cols = [c for c in columns if c in display_df.columns]
        if valid_cols:
            display_df = display_df[valid_cols]

    # height 전달 유무에 따른 안전한 st.dataframe 호출
    if height is not None:
        if not isinstance(height, int) or height <= 0:
            raise ValueError(f"유효하지 않은 height 값입니다: {height}. 양의 정수이어야 합니다.")
        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True,
            height=height,
        )
    else:
        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True,
        )
