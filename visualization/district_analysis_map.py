"""Folium map for the district-level crime and streetlight analysis."""

from __future__ import annotations

import folium
import geopandas as gpd
import pandas as pd
from branca.colormap import linear

METRIC_OPTIONS = {
    "범죄 발생건수": "crime_count_2024",
    "범죄율": "crime_rate_per_10000",
    "가로등 개수": "streetlight_count_2023",
    "가로등 밀도": "streetlights_per_1000_people",
}

TOOLTIP_FIELDS = [
    "district",
    "crime_count_2024",
    "population_2024",
    "crime_rate_per_10000",
    "streetlight_count_2023",
    "streetlights_per_1000_people",
]
TOOLTIP_ALIASES = [
    "자치구",
    "2024년 5대 범죄 발생건수",
    "2024년 등록인구",
    "인구 1만 명당 범죄 발생률",
    "2023년 가로등 개수",
    "인구 1,000명당 가로등 수 (참고용 설치 밀도)",
]


def create_district_analysis_map(
    boundaries: gpd.GeoDataFrame, analysis: pd.DataFrame, metric_label: str
) -> folium.Map:
    """Create a selectable-metric district choropleth with hover and click detail."""
    metric = METRIC_OPTIONS[metric_label]
    layer = boundaries.merge(analysis, on="district", how="left", validate="one_to_one")
    layer = layer.to_crs("EPSG:4326")
    values = layer[metric].fillna(0).astype(float)
    colormap = linear.YlOrRd_09.scale(float(values.min()), float(values.max() or 1))
    colormap.caption = metric_label
    district_map = folium.Map(
        location=[37.5665, 126.9780], zoom_start=10.4, tiles="CartoDB positron"
    )
    for field in TOOLTIP_FIELDS[1:]:
        layer[field] = pd.to_numeric(layer[field], errors="coerce").round(2)
    folium.GeoJson(
        layer,
        name="서울 25개 자치구",
        style_function=lambda feature: {
            "fillColor": colormap(float(feature["properties"].get(metric) or 0)),
            "color": "#334155",
            "weight": 1.2,
            "fillOpacity": 0.72,
        },
        highlight_function=lambda _: {"weight": 3, "color": "#0F172A", "fillOpacity": 0.88},
        tooltip=folium.GeoJsonTooltip(fields=TOOLTIP_FIELDS, aliases=TOOLTIP_ALIASES, localize=True),
        popup=folium.GeoJsonPopup(fields=TOOLTIP_FIELDS, aliases=TOOLTIP_ALIASES, localize=True),
    ).add_to(district_map)
    colormap.add_to(district_map)
    folium.LayerControl(collapsed=True).add_to(district_map)
    return district_map
