"""Pure calculations for crime rates and streetlight-density comparisons."""

from __future__ import annotations

import pandas as pd


def calculate_crime_rates(
    crime: pd.DataFrame, population: pd.DataFrame
) -> pd.DataFrame:
    """Join only same-year district data and calculate incidents per 10,000 people."""
    merged = crime.merge(
        population[["year", "district", "population"]],
        on=["year", "district"],
        how="left",
        validate="many_to_one",
    )
    merged["crime_rate"] = merged["crime_count"] / merged["population"] * 10_000
    return merged


def build_comparison_dataset(
    crime: pd.DataFrame,
    population: pd.DataFrame,
    streetlights: pd.DataFrame,
    analysis_year: int | None = None,
    streetlight_year: int | None = None,
) -> tuple[pd.DataFrame, str | None]:
    """Build a selected-year comparison after spatial district assignment.

    The selected year is never substituted with another available source year.
    """
    crime_years = set(crime["year"].dropna().astype(int))
    population_years = set(population["year"].dropna().astype(int))
    if analysis_year is None:
        common_years = crime_years & population_years
        if len(common_years) == 1:
            analysis_year = next(iter(common_years))
        else:
            return (
                pd.DataFrame(),
                "분석 기준 연도를 하나로 결정할 수 없습니다. 범죄와 등록인구의 같은 연도를 선택하세요.",
            )
    if analysis_year not in crime_years or analysis_year not in population_years:
        return (
            pd.DataFrame(),
            (
                f"분석 기준 연도 {analysis_year}년의 범죄 또는 등록인구 데이터가 없습니다. "
                f"범죄: {sorted(crime_years)}, 인구: {sorted(population_years)}. 다른 연도 데이터로 대체하지 않습니다."
            ),
        )
    if streetlights["district"].notna().sum() == 0:
        return (
            pd.DataFrame(),
            "가로등 원본에는 자치구·주소가 없어 자치구별 가로등 수와 인구 대비 밀도를 계산하지 않았습니다.",
        )
    base = calculate_crime_rates(
        crime[crime["year"] == analysis_year],
        population[population["year"] == analysis_year],
    )
    totals = base[base["crime_type"] == "소계"].copy()
    lights = (
        streetlights.groupby("district", as_index=False)
        .size()
        .rename(columns={"size": "streetlight_count"})
    )
    result = totals.merge(lights, on="district", how="left").fillna({"streetlight_count": 0})
    result["streetlight_count"] = result["streetlight_count"].astype("int64")
    result["streetlights_per_1000_people"] = result["streetlight_count"] / result["population"] * 1_000
    final = result.rename(
        columns={
            "crime_count": f"crime_count_{analysis_year}",
            "population": f"population_{analysis_year}",
            "crime_rate": "crime_rate_per_10000",
            "streetlight_count": f"streetlight_count_{streetlight_year or 'reference'}",
        }
    )[
        [
            "district",
            f"crime_count_{analysis_year}",
            f"population_{analysis_year}",
            "crime_rate_per_10000",
            f"streetlight_count_{streetlight_year or 'reference'}",
            "streetlights_per_1000_people",
        ]
    ].sort_values("district").reset_index(drop=True)
    return final, None


def classify_quadrants(
    data: pd.DataFrame, basis: str = "평균"
) -> tuple[pd.DataFrame, dict[str, float]]:
    """Classify rates/densities using data-derived mean or median cutoffs."""
    agg = "mean" if basis == "평균" else "median"
    rate_cutoff, light_cutoff = (
        float(getattr(data["crime_rate_per_10000"], agg)()),
        float(getattr(data["streetlights_per_1000_people"], agg)()),
    )
    result = data.copy()
    high_rate = result["crime_rate_per_10000"] >= rate_cutoff
    high_light = result["streetlights_per_1000_people"] >= light_cutoff
    result["quadrant"] = "🟡 낮은 범죄율 + 낮은 가로등 밀도"
    result.loc[high_rate & ~high_light, "quadrant"] = (
        "🔴 높은 범죄율 + 낮은 가로등 밀도"
    )
    result.loc[high_rate & high_light, "quadrant"] = "🟠 높은 범죄율 + 높은 가로등 밀도"
    result.loc[~high_rate & high_light, "quadrant"] = (
        "🟢 낮은 범죄율 + 높은 가로등 밀도"
    )
    return result, {"crime_rate": rate_cutoff, "streetlight_density": light_cutoff}
