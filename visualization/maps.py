"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Folium Security Map Component

NOTE: 이 모듈은 pure folium.Map 객체를 생성하여 반환하며, Streamlit UI 코드를 직접 호출하지 않습니다.
"""

from typing import Optional
import folium
import pandas as pd
from config.settings import FACILITY_COLORS, SEOUL_DISTRICTS

# Folium 기본 Marker 색상 매핑 (Fallback)
FOLIUM_COLOR_MAP = {
    "CCTV": "blue",
    "보안등": "orange",
    "비상벨": "red",
    "방범시설": "green",
    "안전시설": "purple",
}


def create_security_map(df: pd.DataFrame, zoom_start: int = 11) -> folium.Map:
    """서울시 보안 인프라 Folium 지도 생성

    Args:
        df (pd.DataFrame): latitude, longitude, facility_type, facility_name, district, address 컬럼 포함 raw df
        zoom_start (int): 초기 지도 확대 배율 (기본값: 11)

    Returns:
        folium.Map: 생성된 Folium 지도 객체
    """
    # 1. 서울 중심 기준 지도 생성
    seoul_center = [37.5665, 126.9780]
    m = folium.Map(location=seoul_center, zoom_start=zoom_start, tiles="OpenStreetMap")

    if df is None or df.empty or "latitude" not in df.columns or "longitude" not in df.columns:
        return m

    # 2. 좌표 유효성 검사 (NaN 및 범위 밖 좌표 필터링, 임의 좌표 생성 금지)
    valid_df = df.dropna(subset=["latitude", "longitude"]).copy()
    valid_df = valid_df[
        (valid_df["latitude"] >= 37.0)
        & (valid_df["latitude"] <= 38.0)
        & (valid_df["longitude"] >= 126.0)
        & (valid_df["longitude"] <= 128.0)
    ].copy()

    if valid_df.empty:
        return m

    # 3. Marker 생성 및 지토 추가
    for _, row in valid_df.iterrows():
        lat = float(row["latitude"])
        lon = float(row["longitude"])

        facility_name = str(row.get("facility_name", "보안시설"))
        facility_type = str(row.get("facility_type", "안전시설"))
        district = str(row.get("district", "-"))
        address = str(row.get("address", "-"))
        count = row.get("count", 1)

        # Popup 내용 작성
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; width: 200px;">
            <h4 style="margin: 0 0 5px 0; color: #1E293B;">{facility_name}</h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 3px 0;"><b>시설 유형:</b> {facility_type}</p>
            <p style="margin: 3px 0;"><b>자치구:</b> {district}</p>
            <p style="margin: 3px 0;"><b>주소:</b> {address}</p>
            <p style="margin: 3px 0;"><b>설치 수량:</b> {count}개</p>
        </div>
        """
        popup = folium.Popup(popup_html, max_width=250)

        # Hex 색상 & Folium 색상 매핑
        hex_color = FACILITY_COLORS.get(facility_type, "#0284C7")
        folium_color = FOLIUM_COLOR_MAP.get(facility_type, "blue")

        # CircleMarker 사용으로 정확한 Hex 색상 및 깔끔한 시각화 구현
        folium.CircleMarker(
            location=[lat, lon],
            radius=6 + min(int(count), 5),
            popup=popup,
            tooltip=f"{district} - {facility_name} ({facility_type})",
            color=hex_color,
            fill=True,
            fill_color=hex_color,
            fill_opacity=0.7,
        ).add_to(m)

    return m
