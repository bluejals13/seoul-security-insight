"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Overall Statistics Analysis

NOTE: 이 모듈은 Pure Data Analysis 로직만 포함하며, Streamlit UI 코드를 호출하지 않습니다.
"""

from typing import Dict, Union
import pandas as pd
from config.settings import FACILITY_TYPES, SEOUL_DISTRICTS


def get_kpi_metrics(df: pd.DataFrame) -> Dict[str, Union[int, float]]:
    """전체 데이터에 대한 핵심 KPI 지표를 계산하여 반환

    Returns:
        dict: {
            "total_records": 전체 레코드 수,
            "total_count": 총 시설 개수 (count 합계),
            "district_count": 데이터에 존재하는 자치구 수,
            "type_count": 데이터에 존재하는 시설 유형 수,
            "avg_per_district": 자치구당 평균 시설 개수
        }
    """
    if df is None or df.empty:
        return {
            "total_records": 0,
            "total_count": 0,
            "district_count": 0,
            "type_count": 0,
            "avg_per_district": 0.0,
        }

    total_records = len(df)
    total_count = int(df["count"].sum()) if "count" in df.columns else total_records
    district_count = df["district"].nunique()
    type_count = df["facility_type"].nunique()
    avg_per_district = round(total_count / 25.0, 1)  # 서울시 25개 구 기준 평균

    return {
        "total_records": total_records,
        "total_count": total_count,
        "district_count": district_count,
        "type_count": type_count,
        "avg_per_district": avg_per_district,
    }


def get_type_facility_count(df: pd.DataFrame) -> pd.DataFrame:
    """시설 유형별 시설 수 및 설치 개수 집계

    Returns:
        pd.DataFrame: ['facility_type', 'facility_count', 'percentage']
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["facility_type", "facility_count", "percentage"])

    grouped = (
        df.groupby("facility_type")["count"]
        .sum()
        .reindex(FACILITY_TYPES, fill_value=0)
        .reset_index(name="facility_count")
    )
    total = grouped["facility_count"].sum()
    grouped["percentage"] = (
        (grouped["facility_count"] / total * 100).round(1) if total > 0 else 0.0
    )
    grouped = grouped.sort_values(by="facility_count", ascending=False).reset_index(drop=True)
    return grouped


def get_yearly_facility_count(df: pd.DataFrame) -> pd.DataFrame:
    """설치 연도별 시설 설치 추이 집계

    Returns:
        pd.DataFrame: ['installed_year', 'facility_count']
    """
    if df is None or df.empty or "installed_year" not in df.columns:
        return pd.DataFrame(columns=["installed_year", "facility_count"])

    valid_df = df.dropna(subset=["installed_year"]).copy()
    valid_df["installed_year"] = valid_df["installed_year"].astype(int)

    grouped = (
        valid_df.groupby("installed_year")["count"]
        .sum()
        .reset_index(name="facility_count")
        .sort_values(by="installed_year")
        .reset_index(drop=True)
    )
    return grouped


def get_overall_statistics_summary(df: pd.DataFrame) -> pd.DataFrame:
    """전체 데이터에 대한 요약 통계 표 (Summary Table) 생성"""
    kpis = get_kpi_metrics(df)
    summary_data = [
        {"항목": "전체 데이터 레코드 수", "수치": f"{kpis['total_records']:,} 건"},
        {"항목": "총 시설 설치 수량", "수치": f"{kpis['total_count']:,} 개"},
        {"항목": "분석 대상 자치구 수", "수치": f"{kpis['district_count']} 개 구"},
        {"항목": "분석 대상 시설 유형 수", "수치": f"{kpis['type_count']} 개 유형"},
        {"항목": "자치구당 평균 시설 수", "수치": f"{kpis['avg_per_district']:,} 개"},
    ]
    return pd.DataFrame(summary_data)

