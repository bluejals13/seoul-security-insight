"""Raw CSV loaders for the crime and streetlight analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from config.settings import SEOUL_DISTRICTS

RAW_DIR = Path("data/raw")
CRIME_FILE = RAW_DIR / "5대_범죄_발생현황_20260819133035.csv"
POPULATION_FILE = RAW_DIR / "등록인구(월별)_20260819133114.csv"
STREETLIGHT_FILE = RAW_DIR / "서울시 가로등 위치 정보.csv"


class SourceDataError(ValueError):
    """Raised when an expected local raw source cannot be read safely."""


def normalize_district(value: object) -> str | None:
    """Return a standard Seoul district or ``None`` without silently dropping it."""
    if pd.isna(value):
        return None
    name = str(value).strip().replace("서울특별시", "").replace(" ", "")
    return name if name in SEOUL_DISTRICTS else None


def _read_raw(path: Path, encoding: str) -> pd.DataFrame:
    if not path.exists():
        raise SourceDataError(f"원본 파일을 찾을 수 없습니다: {path}")
    return pd.read_csv(path, encoding=encoding, header=None)


def load_crime_data() -> pd.DataFrame:
    """Convert the observed 4-row 2024 crime header to the crime standard schema."""
    raw = _read_raw(CRIME_FILE, "utf-8-sig")
    if raw.shape[0] < 5 or raw.shape[1] < 4:
        raise SourceDataError("범죄 CSV의 다중 헤더 구조가 예상과 다릅니다.")
    year = int(str(raw.iloc[0, 2]).strip())
    records: list[dict[str, Any]] = []
    for col in range(2, raw.shape[1], 2):
        crime_type, measure = (
            str(raw.iloc[2, col]).strip(),
            str(raw.iloc[3, col]).strip(),
        )
        if measure != "발생":
            continue
        for _, row in raw.iloc[4:].iterrows():
            district = normalize_district(row.iloc[1])
            if district is not None:  # Total row is intentionally excluded.
                records.append(
                    {
                        "year": year,
                        "district": district,
                        "crime_type": crime_type,
                        "crime_count": pd.to_numeric(row.iloc[col], errors="coerce"),
                    }
                )
    return pd.DataFrame.from_records(records).astype(
        {
            "year": "int64",
            "district": "string",
            "crime_type": "string",
            "crime_count": "Float64",
        }
    )


def load_population_data() -> pd.DataFrame:
    """Load observed June 2026 district-summary rows and their total population."""
    raw = _read_raw(POPULATION_FILE, "utf-8-sig")
    if raw.shape[0] < 4 or raw.shape[1] < 5:
        raise SourceDataError("등록인구 CSV의 다중 헤더 구조가 예상과 다릅니다.")
    period, year = str(raw.iloc[0, 3]).strip(), int(str(raw.iloc[0, 3]).strip()[:4])
    records = []
    for _, row in raw.iloc[3:].iterrows():
        district = normalize_district(row.iloc[1])
        if district is not None and str(row.iloc[2]).strip() == "소계":
            records.append(
                {
                    "year": year,
                    "period": period,
                    "district": district,
                    "population": pd.to_numeric(row.iloc[4], errors="coerce"),
                }
            )
    return pd.DataFrame.from_records(records).astype(
        {
            "year": "int64",
            "period": "string",
            "district": "string",
            "population": "Float64",
        }
    )


def load_streetlight_data() -> pd.DataFrame:
    """Convert actual CP949 id/latitude/longitude table to the streetlight schema.

    District, address, and installation year do not exist in the source, so they
    stay missing rather than being inferred from coordinates or identifiers.
    """
    raw = _read_raw(STREETLIGHT_FILE, "cp949")
    if raw.shape[0] < 2 or raw.shape[1] != 3:
        raise SourceDataError("가로등 CSV의 3열 구조가 예상과 다릅니다.")
    data = raw.iloc[1:].copy()
    return pd.DataFrame(
        {
            "facility_id": data.iloc[:, 0].astype("string"),
            "district": pd.Series(pd.NA, index=data.index, dtype="string"),
            "latitude": pd.to_numeric(data.iloc[:, 1], errors="coerce"),
            "longitude": pd.to_numeric(data.iloc[:, 2], errors="coerce"),
            "address": pd.Series(pd.NA, index=data.index, dtype="string"),
            "year": pd.Series(pd.NA, index=data.index, dtype="Int64"),
            "facility_type": pd.Series("streetlight", index=data.index, dtype="string"),
        }
    ).reset_index(drop=True)


def quality_report(
    crime: pd.DataFrame, population: pd.DataFrame, streetlights: pd.DataFrame
) -> dict[str, Any]:
    """Return explicit quality counts for display and tests; no rows are hidden."""
    valid = streetlights["latitude"].between(37.0, 38.0) & streetlights[
        "longitude"
    ].between(126.0, 128.0)
    return {
        "crime_missing_count": int(crime["crime_count"].isna().sum()),
        "crime_negative_count": int((crime["crime_count"] < 0).sum()),
        "crime_unknown_districts": sorted(
            set(
                crime.loc[~crime["district"].isin(SEOUL_DISTRICTS), "district"].dropna()
            )
        ),
        "crime_duplicates": int(
            crime.duplicated(["year", "district", "crime_type"]).sum()
        ),
        "population_missing": int(population["population"].isna().sum()),
        "population_nonpositive": int((population["population"] <= 0).sum()),
        "population_unknown_districts": sorted(
            set(
                population.loc[
                    ~population["district"].isin(SEOUL_DISTRICTS), "district"
                ].dropna()
            )
        ),
        "streetlight_missing_latitude": int(streetlights["latitude"].isna().sum()),
        "streetlight_missing_longitude": int(streetlights["longitude"].isna().sum()),
        "streetlight_invalid_coordinates": int((~valid).sum()),
        "streetlight_duplicate_rows": int(streetlights.duplicated().sum()),
        "streetlight_duplicate_ids": int(
            streetlights["facility_id"].duplicated().sum()
        ),
        "streetlight_district_available": bool(streetlights["district"].notna().any()),
        "crime_years": sorted(crime["year"].dropna().unique().tolist()),
        "population_years": sorted(population["year"].dropna().unique().tolist()),
    }
