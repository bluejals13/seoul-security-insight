import pandas as pd

from analysis.crime_streetlight_analysis import (
    build_comparison_dataset,
    calculate_crime_rates,
    classify_quadrants,
)
from config.settings import SEOUL_DISTRICTS
from utils.crime_streetlight_loader import (
    load_crime_data,
    load_population_data,
    load_streetlight_data,
    normalize_district,
    quality_report,
)


def test_actual_raw_loaders_and_normalization() -> None:
    crime, population, streetlights = (
        load_crime_data(),
        load_population_data(),
        load_streetlight_data(),
    )
    assert set(crime.columns) == {"year", "district", "crime_type", "crime_count"}
    assert len(crime) == 150 and len(population) == 25 and len(streetlights) == 19_316
    assert set(crime["district"]) == set(SEOUL_DISTRICTS)
    assert normalize_district(" 서울특별시 종로구 ") == "종로구"
    assert normalize_district("알수없는구") is None


def test_quality_report_exposes_source_issues() -> None:
    report = quality_report(
        load_crime_data(), load_population_data(), load_streetlight_data()
    )
    assert report["crime_years"] == [2024]
    assert report["population_years"] == [2026]
    assert report["streetlight_district_available"] is False
    assert report["streetlight_invalid_coordinates"] == 25


def test_crime_rate_and_density_formulae() -> None:
    crime = pd.DataFrame(
        {
            "year": [2024],
            "district": ["종로구"],
            "crime_type": ["소계"],
            "crime_count": [100],
        }
    )
    population = pd.DataFrame(
        {"year": [2024], "district": ["종로구"], "population": [20_000]}
    )
    rated = calculate_crime_rates(crime, population)
    assert rated.loc[0, "crime_rate"] == 50

    lights = pd.DataFrame(
        {
            "district": ["종로구"] * 10,
            "facility_id": range(10),
            "latitude": [37.5] * 10,
            "longitude": [127.0] * 10,
        }
    )
    comparison, reason = build_comparison_dataset(crime, population, lights)
    assert reason is None
    assert comparison.loc[0, "streetlights_per_1000_people"] == 0.5


def test_year_mismatch_blocks_comparison() -> None:
    data, reason = build_comparison_dataset(
        load_crime_data(), load_population_data(), load_streetlight_data()
    )
    assert data.empty and reason is not None and "일치하지" in reason


def test_quadrants_use_data_cutoffs() -> None:
    data = pd.DataFrame(
        {"crime_rate": [1.0, 3.0], "streetlights_per_1000_people": [1.0, 3.0]}
    )
    result, cutoffs = classify_quadrants(data, "중앙값")
    assert cutoffs == {"crime_rate": 2.0, "streetlight_density": 2.0}
    assert result.loc[1, "quadrant"].startswith("🟠")
