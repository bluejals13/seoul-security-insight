"""Plotly/Folium charts consuming standardized analysis frames."""

from __future__ import annotations

import folium
import pandas as pd
import plotly.express as px

from visualization.charts import apply_chart_theme


def crime_rate_bar(data: pd.DataFrame):
    return apply_chart_theme(
        px.bar(
            data.sort_values("crime_rate_per_10000"),
            x="crime_rate_per_10000",
            y="district",
            orientation="h",
            color="crime_rate_per_10000",
            color_continuous_scale="Reds",
            labels={"crime_rate_per_10000": "인구 1만 명당 범죄 발생 건수", "district": "자치구"},
        ),
        "자치구별 범죄율",
        "인구 1만 명당 범죄 발생 건수",
        "자치구",
    )


def crime_count_bar(data: pd.DataFrame):
    return apply_chart_theme(
        px.bar(
            data.sort_values("crime_count"),
            x="crime_count",
            y="district",
            orientation="h",
            labels={"crime_count": "범죄 발생 건수", "district": "자치구"},
        ),
        "자치구별 범죄 발생 건수",
        "범죄 발생 건수",
        "자치구",
    )


def crime_type_pie(data: pd.DataFrame):
    return apply_chart_theme(
        px.pie(data, names="crime_type", values="crime_count", hole=0.45),
        "범죄 유형별 발생 비중",
    )


def crime_heatmap(data: pd.DataFrame):
    return apply_chart_theme(
        px.imshow(
            data.pivot(
                index="district", columns="crime_type", values="crime_count"
            ).fillna(0),
            aspect="auto",
            color_continuous_scale="Reds",
            labels={"color": "발생 건수"},
        ),
        "자치구 × 범죄 유형",
        "범죄 유형",
        "자치구",
    )


def streetlight_map(data: pd.DataFrame, limit: int = 5000) -> folium.Map:
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=11, tiles="OpenStreetMap")
    valid = data.dropna(subset=["latitude", "longitude"])
    valid = valid[
        valid["latitude"].between(37.0, 38.0) & valid["longitude"].between(126.0, 128.0)
    ].head(limit)
    for row in valid.itertuples(index=False):
        folium.CircleMarker(
            [row.latitude, row.longitude],
            radius=2,
            color="#F59E0B",
            fill=True,
            fill_opacity=0.6,
            popup=folium.Popup(
                f"<div style='font-size:14px; line-height:1.5; color:#102A43;'><b>자치구</b>: {str(row.district) if pd.notna(row.district) else '미배정'}<br><b>관리번호</b>: {row.facility_id}</div>",
                max_width=260,
            ),
            tooltip=folium.Tooltip(
                f"{str(row.district) if pd.notna(row.district) else '미배정'} · {row.facility_id}",
                style="font-size:14px; font-weight:600; color:#102A43; background:#FFFFFF; border:1px solid #1479B8;",
            ),
        ).add_to(m)
    return m


def risk_scatter(data: pd.DataFrame):
    return px.scatter(
        data,
        x="streetlights_per_1000_people",
        y="crime_rate_per_10000",
        text="district",
        color="quadrant",
        hover_data=["crime_count_2024", "population_2024", "streetlight_count_2023"],
        labels={
            "streetlights_per_1000_people": "인구 1,000명당 가로등 수",
            "crime_rate_per_10000": "인구 1만 명당 범죄 발생 건수",
        },
    )
