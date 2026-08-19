"""Reusable KPI renderers for legacy and analysis dashboards."""

from __future__ import annotations

import streamlit as st

from config.settings import COLOR_PALETTE


def render_kpi_cards(
    total_count: int, district_count: int, type_count: int, avg_count: float
) -> None:
    """Retain the legacy four-metric interface for existing infrastructure pages."""
    render_analysis_metrics(
        [
            ("전체 시설 수량", f"{total_count:,}개"),
            ("분석 자치구", f"{district_count}개 구"),
            ("시설 유형", f"{type_count}개"),
            ("구별 평균 시설 수", f"{avg_count:,.1f}개"),
        ]
    )


def render_analysis_metrics(metrics: list[tuple[str, str]]) -> None:
    """Render arbitrary analysis KPIs; preserves the project card component role."""
    columns = st.columns(len(metrics))
    for column, (label, value) in zip(columns, metrics):
        with column:
            st.markdown(
                f"""<div style="background:{COLOR_PALETTE["card"]};padding:16px 20px;border-radius:8px;border-left:4px solid {COLOR_PALETTE["accent"]};box-shadow:0 1px 3px rgba(0,0,0,.05)"><p style="margin:0;color:#64748b;font-size:13px">{label}</p><h3 style="margin:4px 0 0;color:{COLOR_PALETTE["primary"]}">{value}</h3></div>""",
                unsafe_allow_html=True,
            )
