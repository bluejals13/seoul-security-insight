"""Load Seoul district boundaries and spatially assign streetlights."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import geopandas as gpd
import pandas as pd

from config.settings import SEOUL_DISTRICTS

REFERENCE_DIR = Path("data/reference")
BOUNDARY_FILE = REFERENCE_DIR / "서울시 상권분석서비스(영역-자치구).shp"
BOUNDARY_CRS = "EPSG:5181"
WGS84_CRS = "EPSG:4326"


class BoundaryDataError(ValueError):
    """Raised when the reference boundary data does not meet its contract."""


def normalize_district_name(value: object) -> str | None:
    """Normalize a Seoul district label without inventing an unknown district."""
    if pd.isna(value):
        return None
    name = str(value).strip().replace("서울특별시", "").replace(" ", "")
    return name if name in SEOUL_DISTRICTS else None


def validate_district_boundaries(boundaries: gpd.GeoDataFrame) -> dict[str, Any]:
    """Validate the 25-district reference-layer contract and return its audit."""
    required = {"SIGNGU_CD", "SIGNGU_NM", "geometry"}
    missing_columns = sorted(required - set(boundaries.columns))
    districts = boundaries.get("district", pd.Series(dtype="string"))
    duplicates = sorted(districts[districts.duplicated()].dropna().unique().tolist())
    unknown = sorted(set(districts.dropna()) - set(SEOUL_DISTRICTS))
    missing = sorted(set(SEOUL_DISTRICTS) - set(districts.dropna()))
    report = {
        "boundary_feature_count": len(boundaries),
        "boundary_missing_columns": missing_columns,
        "boundary_crs": boundaries.crs.to_string() if boundaries.crs else None,
        "boundary_geometry_types": sorted(boundaries.geom_type.dropna().unique().tolist()),
        "boundary_invalid_geometry_count": int((~boundaries.geometry.is_valid).sum()),
        "boundary_missing_districts": missing,
        "boundary_unknown_districts": unknown,
        "boundary_duplicate_districts": duplicates,
    }
    if (
        missing_columns
        or boundaries.crs is None
        or boundaries.crs.to_epsg() != 5181
        or len(boundaries) != 25
        or report["boundary_geometry_types"] != ["Polygon"]
        or report["boundary_invalid_geometry_count"]
        or missing
        or unknown
        or duplicates
    ):
        raise BoundaryDataError(f"자치구 경계 검증 실패: {report}")
    return report


def load_district_boundaries() -> gpd.GeoDataFrame:
    """Read the immutable reference Shapefile and validate its 25 districts."""
    if not BOUNDARY_FILE.is_file():
        raise BoundaryDataError(f"자치구 경계 파일을 찾을 수 없습니다: {BOUNDARY_FILE}")
    boundaries = gpd.read_file(BOUNDARY_FILE, encoding="utf-8")
    boundaries = boundaries.copy()
    boundaries["district"] = boundaries["SIGNGU_NM"].map(normalize_district_name)
    validate_district_boundaries(boundaries)
    return boundaries[["SIGNGU_CD", "SIGNGU_NM", "district", "geometry"]]


def spatial_join_streetlights(
    streetlights: pd.DataFrame, boundaries: gpd.GeoDataFrame | None = None
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Assign WGS84 streetlight points to a district, retaining outside rows as NA.

    A point is assigned only when it is strictly within one polygon. Invalid or
    unmatched coordinates remain unassigned and are reported; no fallback
    district is fabricated.
    """
    required = {"latitude", "longitude"}
    if missing := sorted(required - set(streetlights.columns)):
        raise BoundaryDataError(f"가로등 좌표 컬럼이 없습니다: {missing}")
    boundary_gdf = boundaries if boundaries is not None else load_district_boundaries()
    validate_district_boundaries(boundary_gdf)
    result = streetlights.copy()
    result["district"] = pd.Series(pd.NA, index=result.index, dtype="string")
    latitude = pd.to_numeric(result["latitude"], errors="coerce")
    longitude = pd.to_numeric(result["longitude"], errors="coerce")
    valid_wgs84 = latitude.between(37.0, 38.0) & longitude.between(126.0, 128.0)
    points = gpd.GeoDataFrame(
        result.loc[valid_wgs84].copy(),
        geometry=gpd.points_from_xy(longitude[valid_wgs84], latitude[valid_wgs84]),
        crs=WGS84_CRS,
    ).to_crs(BOUNDARY_CRS)
    joined = gpd.sjoin(
        points, boundary_gdf[["district", "geometry"]], how="left", predicate="within"
    )
    if joined.index.duplicated().any():
        raise BoundaryDataError("한 가로등이 둘 이상의 자치구에 결합되었습니다.")
    result.loc[joined.index, "district"] = joined["district_right"].astype("string")
    assigned = int(result["district"].notna().sum())
    report = {
        "streetlight_total_count": len(result),
        "streetlight_valid_wgs84_count": int(valid_wgs84.sum()),
        "streetlight_invalid_coordinate_count": int((~valid_wgs84).sum()),
        "streetlight_spatial_join_assigned_count": assigned,
        "streetlight_outside_boundary_count": int(valid_wgs84.sum()) - assigned,
        "streetlight_unassigned_total_count": int(result["district"].isna().sum()),
        "streetlight_assigned_district_sum": assigned,
    }
    return result, report
