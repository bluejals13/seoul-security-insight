"""Raw CSV loaders for the crime and streetlight analysis."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pandas as pd

from config.settings import SEOUL_DISTRICTS

RAW_DIR = Path("data/raw")
DEFAULT_ANALYSIS_YEAR = 2024

# Only these source families participate in the risk analysis.  Other raw CSVs
# may contain a year in their filename, but are intentionally not auto-enrolled.
_DATASET_PATTERNS = {
    "crime": re.compile(r"^5대_범죄_발생현황_(?P<year>\d{4})\.csv$"),
    "population": re.compile(r"^등록인구_(?P<year>\d{4})\.csv$"),
    "streetlight": re.compile(r"^서울시_가로등_위치_(?P<year>\d{4})\.csv$"),
}


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


def discover_dataset_files(dataset: str) -> dict[int, Path]:
    """Return explicitly supported source files indexed by the year in their name."""
    try:
        pattern = _DATASET_PATTERNS[dataset]
    except KeyError as exc:
        raise ValueError(f"지원하지 않는 데이터셋입니다: {dataset}") from exc

    discovered: dict[int, Path] = {}
    for path in RAW_DIR.glob("*.csv"):
        match = pattern.fullmatch(path.name)
        if match is None:
            continue
        year = int(match["year"])
        if year in discovered:
            raise SourceDataError(f"{dataset} {year}년 원본 파일이 둘 이상입니다.")
        discovered[year] = path
    return discovered


def available_analysis_years() -> list[int]:
    """Return all selectable years discovered for crime or population sources.

    A year with just one of the two files remains selectable so the UI can
    clearly explain the missing counterpart instead of substituting another year.
    """
    return sorted(
        set(discover_dataset_files("crime")) | set(discover_dataset_files("population")),
        reverse=True,
    )


def source_years(analysis_year: int) -> dict[str, int | None]:
    """Expose actual source years for the selected analysis year and streetlights."""
    return {
        "crime": analysis_year if analysis_year in discover_dataset_files("crime") else None,
        "population": (
            analysis_year if analysis_year in discover_dataset_files("population") else None
        ),
        "streetlight": next(iter(discover_dataset_files("streetlight")), None),
    }


def _source_file(dataset: str, year: int) -> Path:
    files = discover_dataset_files(dataset)
    if path := files.get(year):
        return path
    available = ", ".join(map(str, sorted(files))) or "없음"
    raise SourceDataError(
        f"선택한 분석 기준 연도 {year}년의 {dataset} 데이터가 없습니다. "
        f"사용 가능한 연도: {available}. 다른 연도 데이터로 대체하지 않습니다."
    )


def load_crime_data(year: int = DEFAULT_ANALYSIS_YEAR) -> pd.DataFrame:
    """Convert the selected year's 5-major-crime source to the standard schema."""
    raw = _read_raw(_source_file("crime", year), "utf-8-sig")
    if raw.shape[0] < 5 or raw.shape[1] < 4:
        raise SourceDataError("범죄 CSV의 다중 헤더 구조가 예상과 다릅니다.")
    source_year = int(str(raw.iloc[0, 2]).strip())
    if source_year != year:
        raise SourceDataError(
            f"범죄 파일명 연도({year})와 CSV 내부 연도({source_year})가 일치하지 않습니다."
        )
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
                        "year": source_year,
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


def load_population_data(year: int = DEFAULT_ANALYSIS_YEAR) -> pd.DataFrame:
    """Load selected-year registered population by district from the local source."""
    raw = _read_raw(_source_file("population", year), "utf-8-sig")
    if raw.shape[0] < 4 or raw.shape[1] < 5:
        raise SourceDataError("등록인구 CSV의 다중 헤더 구조가 예상과 다릅니다.")
    source_year = int(str(raw.iloc[0, 3]).strip()[:4])
    if source_year != year:
        raise SourceDataError(
            f"등록인구 파일명 연도({year})와 CSV 내부 연도({source_year})가 일치하지 않습니다."
        )
    records = []
    for _, row in raw.iloc[3:].iterrows():
        district = normalize_district(row.iloc[1])
        if district is not None:
            records.append(
                {
                    "year": source_year,
                    "period": f"{source_year}년",
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
    streetlight_files = discover_dataset_files("streetlight")
    if len(streetlight_files) != 1:
        raise SourceDataError(
            "가로등 원본은 현재 하나의 연도만 지원합니다. "
            f"발견된 연도: {', '.join(map(str, sorted(streetlight_files))) or '없음'}"
        )
    raw = _read_raw(next(iter(streetlight_files.values())), "cp949")
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
    crime: pd.DataFrame,
    population: pd.DataFrame,
    streetlights: pd.DataFrame,
    boundary_report: dict[str, Any] | None = None,
    spatial_report: dict[str, Any] | None = None,
    final_data: pd.DataFrame | None = None,
) -> dict[str, Any]:
    """Return explicit quality counts for display and tests; no rows are hidden."""
    valid = streetlights["latitude"].between(37.0, 38.0) & streetlights[
        "longitude"
    ].between(126.0, 128.0)
    report: dict[str, Any] = {
        "crime_district_count": int(crime["district"].nunique()),
        "crime_missing_districts": sorted(set(SEOUL_DISTRICTS) - set(crime["district"])),
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
        "population_district_count": int(population["district"].nunique()),
        "population_missing_districts": sorted(set(SEOUL_DISTRICTS) - set(population["district"])),
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
    if boundary_report:
        report.update(boundary_report)
    if spatial_report:
        report.update(spatial_report)
    if final_data is not None:
        report.update(
            {
                "final_district_count": int(final_data["district"].nunique()),
                "final_missing_values": {
                    column: int(final_data[column].isna().sum())
                    for column in final_data.columns
                },
                "final_duplicate_districts": sorted(
                    final_data.loc[final_data["district"].duplicated(), "district"].tolist()
                ),
            }
        )
    return report
