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
from utils.district_boundary_loader import (
    load_district_boundaries,
    spatial_join_streetlights,
    validate_district_boundaries,
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


def test_boundary_loader_and_spatial_join_actual_data() -> None:
    boundaries = load_district_boundaries()
    boundary_report = validate_district_boundaries(boundaries)
    assigned, spatial_report = spatial_join_streetlights(load_streetlight_data(), boundaries)
    assert boundary_report["boundary_feature_count"] == 25
    assert boundary_report["boundary_invalid_geometry_count"] == 0
    assert set(boundaries["district"]) == set(SEOUL_DISTRICTS)
    assert spatial_report == {
        "streetlight_total_count": 19_316,
        "streetlight_valid_wgs84_count": 19_291,
        "streetlight_invalid_coordinate_count": 25,
        "streetlight_spatial_join_assigned_count": 18_861,
        "streetlight_outside_boundary_count": 430,
        "streetlight_unassigned_total_count": 455,
        "streetlight_assigned_district_sum": 18_861,
    }
    assert int(assigned["district"].notna().sum()) == 18_861


def test_quality_report_exposes_source_issues() -> None:
    report = quality_report(load_crime_data(), load_population_data(), load_streetlight_data())
    assert report["crime_years"] == [2024]
    assert report["population_years"] == [2024]
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
    assert comparison.loc[0, "crime_count_2024"] == 100
    assert comparison.loc[0, "population_2024"] == 20_000


def test_actual_final_dataset_has_complete_25_districts() -> None:
    joined, spatial_report = spatial_join_streetlights(load_streetlight_data())
    data, reason = build_comparison_dataset(load_crime_data(), load_population_data(), joined)
    report = quality_report(
        load_crime_data(), load_population_data(), joined, spatial_report=spatial_report, final_data=data
    )
    assert reason is None
    assert len(data) == 25
    assert set(data["district"]) == set(SEOUL_DISTRICTS)
    assert not data.isna().any().any()
    assert report["final_district_count"] == 25
    assert report["final_duplicate_districts"] == []


def test_quadrants_use_data_cutoffs() -> None:
    data = pd.DataFrame(
        {"crime_rate_per_10000": [1.0, 3.0], "streetlights_per_1000_people": [1.0, 3.0]}
    )
    result, cutoffs = classify_quadrants(data, "중앙값")
    assert cutoffs == {"crime_rate": 2.0, "streetlight_density": 2.0}
    assert result.loc[1, "quadrant"].startswith("🟠")
