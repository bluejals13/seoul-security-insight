"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Plotly Chart Components

NOTE: 이 모듈은 Plotly Figure 객체를 생성하여 반환하며, Streamlit UI 코드를 호출하지 않습니다.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config.settings import COLOR_PALETTE, FACILITY_COLORS, SEOUL_DISTRICTS


def apply_chart_theme(fig: go.Figure, title: str, x_title: str = "", y_title: str = "") -> go.Figure:
    """Plotly Figure에 보안 인프라 대시보드 공통 스타일 및 레이아웃 적용"""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "x": 0.02,
            "xanchor": "left",
            "font": {"size": 16, "color": COLOR_PALETTE["primary"], "family": "Malgun Gothic, sans-serif"},
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,250,252,0.5)",
        font={"family": "Malgun Gothic, sans-serif", "color": COLOR_PALETTE["text"]},
        margin={"l": 40, "r": 40, "t": 60, "b": 40},
        xaxis={
            "title": x_title,
            "showgrid": True,
            "gridcolor": "#E2E8F0",
            "zeroline": False,
        },
        yaxis={
            "title": y_title,
            "showgrid": True,
            "gridcolor": "#E2E8F0",
            "zeroline": False,
        },
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
    )
    return fig


def create_district_bar_chart(df: pd.DataFrame) -> go.Figure:
    """Chart 1: 자치구별 보안 인프라 수 (Horizontal Bar Chart)
    시설 수 기준 내림차순 정렬
    """
    if df is None or df.empty:
        fig = go.Figure()
        return apply_chart_theme(fig, "자치구별 보안 인프라 수 (데이터 없음)")

    # count / facility_count 컬럼 대응
    val_col = "facility_count" if "facility_count" in df.columns else "count"
    
    # Horizontal Bar Chart에서는 화면 위에서 아래로 내림차순 표시되도록 ascending=True 정렬
    sorted_df = df.sort_values(by=val_col, ascending=True)

    fig = px.bar(
        sorted_df,
        x=val_col,
        y="district",
        orientation="h",
        labels={val_col: "시설 수 (개)", "district": "자치구"},
        color=val_col,
        color_continuous_scale=["#BAE6FD", "#0284C7", "#0F172A"],
        text=val_col,
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_coloraxes(showscale=False)
    return apply_chart_theme(fig, "자치구별 보안 인프라 수", x_title="시설 수 (개)", y_title="자치구")


def create_facility_type_donut_chart(df: pd.DataFrame) -> go.Figure:
    """Chart 2: 시설 유형별 분포 (Donut Chart)"""
    if df is None or df.empty:
        fig = go.Figure()
        return apply_chart_theme(fig, "시설 유형별 분포 (데이터 없음)")

    val_col = "facility_count" if "facility_count" in df.columns else "count"

    colors = [FACILITY_COLORS.get(ft, "#64748B") for ft in df["facility_type"]]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=df["facility_type"],
                values=df[val_col],
                hole=0.5,
                marker={"colors": colors},
                textinfo="label+percent",
                hoverinfo="label+value+percent",
                insidetextorientation="radial",
            )
        ]
    )
    return apply_chart_theme(fig, "시설 유형별 설치 비중")


def create_district_facility_heatmap(df: pd.DataFrame) -> go.Figure:
    """Chart 3: 자치구 x 시설 유형 Heatmap
    행: district (SEOUL_DISTRICTS 순서 일치), 열: facility_type
    """
    if df is None or df.empty:
        fig = go.Figure()
        return apply_chart_theme(fig, "자치구 × 시설 유형 분포 Heatmap (데이터 없음)")

    # 입력이 이미 Crosstab 형태인지, Raw DataFrame 형태인지 판단
    if "district" in df.columns and "facility_type" in df.columns:
        ct = pd.crosstab(
            index=df["district"],
            columns=df["facility_type"],
            values=df["count"],
            aggfunc="sum",
        ).fillna(0).astype(int)
    else:
        ct = df.copy()
        if "district" in ct.columns:
            ct = ct.set_index("district")

    if "합계" in ct.columns:
        ct = ct.drop(columns=["합계"])

    # SEOUL_DISTRICTS 순서에 맞춤
    available_districts = [d for d in SEOUL_DISTRICTS if d in ct.index]
    ct = ct.reindex(index=available_districts)

    fig = px.imshow(
        ct,
        labels={"x": "시설 유형", "y": "자치구", "color": "시설 수"},
        x=ct.columns,
        y=ct.index,
        color_continuous_scale="Blues",
        aspect="auto",
        text_auto=True,
    )
    return apply_chart_theme(fig, "자치구 × 시설 유형 분포 Heatmap", x_title="시설 유형", y_title="자치구")


def create_facility_type_bar_chart(df: pd.DataFrame) -> go.Figure:
    """Chart 4: 시설 유형별 시설 수 비교 (Vertical Bar Chart)
    시설 수 기준 내림차순 정렬
    """
    if df is None or df.empty:
        fig = go.Figure()
        return apply_chart_theme(fig, "시설 유형별 시설 수 비교 (데이터 없음)")

    val_col = "facility_count" if "facility_count" in df.columns else "count"
    sorted_df = df.sort_values(by=val_col, ascending=False)

    colors = [FACILITY_COLORS.get(ft, COLOR_PALETTE["accent"]) for ft in sorted_df["facility_type"]]

    fig = px.bar(
        sorted_df,
        x="facility_type",
        y=val_col,
        labels={val_col: "시설 수 (개)", "facility_type": "시설 유형"},
        text=val_col,
    )
    fig.update_traces(marker_color=colors, textposition="outside")
    return apply_chart_theme(fig, "시설 유형별 시설 수 비교", x_title="시설 유형", y_title="시설 수 (개)")


def create_yearly_facility_line_chart(df: pd.DataFrame) -> go.Figure:
    """Chart 5: 연도별 설치 추이 (Line Chart)
    installed_year 기준. 결측 연도는 임의로 채우지 않음.
    """
    if df is None or df.empty or ("installed_year" not in df.columns and "installed_year" not in getattr(df, "index", [])):
        fig = go.Figure()
        return apply_chart_theme(fig, "연도별 설치 추이 (데이터 없음)")

    val_col = "facility_count" if "facility_count" in df.columns else "count"

    # installed_year가 NaN인 데이터는 제외 후 정렬
    valid_df = df.dropna(subset=["installed_year"]).copy()
    if valid_df.empty:
        fig = go.Figure()
        return apply_chart_theme(fig, "연도별 설치 추이 (데이터 없음)")

    valid_df["installed_year"] = valid_df["installed_year"].astype(int)
    valid_df = valid_df.sort_values(by="installed_year")

    fig = px.line(
        valid_df,
        x="installed_year",
        y=val_col,
        markers=True,
        labels={"installed_year": "설치 연도", val_col: "신규 설치 수량 (개)"},
        color_discrete_sequence=[COLOR_PALETTE["accent"]],
    )
    fig.update_traces(line={"width": 3}, marker={"size": 8})
    return apply_chart_theme(fig, "연도별 보안 인프라 신규 설치 추이", x_title="설치 연도 (년)", y_title="설치 수량 (개)")
