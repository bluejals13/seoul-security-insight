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
    crime: pd.DataFrame, population: pd.DataFrame, streetlights: pd.DataFrame
) -> tuple[pd.DataFrame, str | None]:
    """Build the 2024/2023 comparison after a spatial district assignment."""
    common_years = set(crime["year"].unique()) & set(population["year"].unique())
    if not common_years:
        return (
            pd.DataFrame(),
            f"범죄 기준연도({sorted(set(crime['year']))})와 등록인구 기준연도({sorted(set(population['year']))})가 일치하지 않아 범죄율을 계산하지 않았습니다.",
        )
    if streetlights["district"].notna().sum() == 0:
        return (
            pd.DataFrame(),
            "가로등 원본에는 자치구·주소가 없어 자치구별 가로등 수와 인구 대비 밀도를 계산하지 않았습니다.",
        )
    base = calculate_crime_rates(crime[crime["year"].isin(common_years)], population)
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
            "crime_count": "crime_count_2024",
            "population": "population_2024",
            "crime_rate": "crime_rate_per_10000",
            "streetlight_count": "streetlight_count_2023",
        }
    )[
        [
            "district",
            "crime_count_2024",
            "population_2024",
            "crime_rate_per_10000",
            "streetlight_count_2023",
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
