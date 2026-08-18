"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Regional Analysis Logic

NOTE: 이 모듈은 pure data analysis 로직만 포함하며, Streamlit UI 코드를 호출하지 않습니다.
"""

from typing import Dict, Any
import pandas as pd
from config.settings import FACILITY_TYPES, SEOUL_DISTRICTS


def get_district_facility_count(df: pd.DataFrame) -> pd.DataFrame:
    """자치구별 시설 개수 합계 집계 (서울시 25개 구 전체 재색인 포함)

    Returns:
        pd.DataFrame: ['district', 'facility_count']
    """
    if df is None or df.empty:
        return pd.DataFrame({"district": SEOUL_DISTRICTS, "facility_count": 0})

    grouped = (
        df.groupby("district")["count"]
        .sum()
        .reindex(SEOUL_DISTRICTS, fill_value=0)
        .reset_index(name="facility_count")
        .sort_values(by="facility_count", ascending=False)
        .reset_index(drop=True)
    )
    return grouped


def get_district_type_crosstab(df: pd.DataFrame) -> pd.DataFrame:
    """자치구 x 시설 유형 교차 집계표 (Crosstab Matrix)

    Returns:
        pd.DataFrame: index='district', columns=FACILITY_TYPES + ['합계']
    """
    if df is None or df.empty:
        empty_matrix = pd.DataFrame(
            0, index=SEOUL_DISTRICTS, columns=FACILITY_TYPES + ["합계"]
        )
        empty_matrix.index.name = "district"
        return empty_matrix

    ct = pd.crosstab(
        index=df["district"],
        columns=df["facility_type"],
        values=df["count"],
        aggfunc="sum",
    ).fillna(0).astype(int)

    # 25개 자치구 및 5개 시설 유형 모두 존재하도록 재색인
    ct = ct.reindex(index=SEOUL_DISTRICTS, columns=FACILITY_TYPES, fill_value=0)
    ct["합계"] = ct.sum(axis=1)
    ct.index.name = "district"
    return ct.reset_index()


def get_selected_district_summary(df: pd.DataFrame, district: str) -> Dict[str, Any]:
    """특정 자치구 선택 시 해당 자치구의 요약 정보 계산

    Returns:
        dict: {
            "district": 구 이름,
            "total_count": 해당 구의 전체 시설 개수,
            "rank": 25개 자치구 중 순위 (1~25),
            "type_breakdown": 시설 유형별 개수 df,
            "filtered_df": 해당 자치구만 필터링된 raw df
        }
    """
    if df is None or df.empty or district not in SEOUL_DISTRICTS:
        return {
            "district": district,
            "total_count": 0,
            "rank": "-",
            "type_breakdown": pd.DataFrame(columns=["facility_type", "count"]),
            "filtered_df": pd.DataFrame(),
        }

    district_df = df[df["district"] == district].copy()
    total_count = int(district_df["count"].sum())

    # 순위 계산
    all_district_counts = get_district_facility_count(df)
    rank = "-"
    if not all_district_counts.empty and district in all_district_counts["district"].values:
        r_series = all_district_counts[all_district_counts["district"] == district].index
        if len(r_series) > 0:
            rank = f"{r_series[0] + 1}위 / 25개 구"

    type_breakdown = (
        district_df.groupby("facility_type")["count"]
        .sum()
        .reindex(FACILITY_TYPES, fill_value=0)
        .reset_index(name="facility_count")
        .sort_values(by="facility_count", ascending=False)
        .reset_index(drop=True)
    )

    return {
        "district": district,
        "total_count": total_count,
        "rank": rank,
        "type_breakdown": type_breakdown,
        "filtered_df": district_df,
    }


def get_selected_type_summary(df: pd.DataFrame, facility_type: str) -> Dict[str, Any]:
    """특정 시설 유형 선택 시 자치구별 분포 및 요약 정보 계산

    Returns:
        dict: {
            "facility_type": 시설 유형,
            "total_count": 전체 설치 개수,
            "top_district": 가장 많이 설치된 자치구,
            "district_breakdown": 자치구별 개수 df,
            "filtered_df": 해당 시설 유형만 필터링된 raw df
        }
    """
    if df is None or df.empty or facility_type not in FACILITY_TYPES:
        return {
            "facility_type": facility_type,
            "total_count": 0,
            "top_district": "-",
            "district_breakdown": pd.DataFrame(columns=["district", "facility_count"]),
            "filtered_df": pd.DataFrame(),
        }

    type_df = df[df["facility_type"] == facility_type].copy()
    total_count = int(type_df["count"].sum())

    district_breakdown = (
        type_df.groupby("district")["count"]
        .sum()
        .reindex(SEOUL_DISTRICTS, fill_value=0)
        .reset_index(name="facility_count")
        .sort_values(by="facility_count", ascending=False)
        .reset_index(drop=True)
    )

    top_district = "-"
    if not district_breakdown.empty and district_breakdown["facility_count"].iloc[0] > 0:
        top_district = district_breakdown["district"].iloc[0]

    return {
        "facility_type": facility_type,
        "total_count": total_count,
        "top_district": top_district,
        "district_breakdown": district_breakdown,
        "filtered_df": type_df,
    }


# 함수명 별칭 (Function Name Aliases for Contract Compliance)
get_facility_count_by_district = get_district_facility_count
get_district_facility_crosstab = get_district_type_crosstab


def get_facility_count_by_type(df: pd.DataFrame) -> pd.DataFrame:
    """시설 유형별 시설 수 합계 집계 (regional_analysis 내 편의용)"""
    if df is None or df.empty:
        return pd.DataFrame({"facility_type": FACILITY_TYPES, "facility_count": 0})

    grouped = (
        df.groupby("facility_type")["count"]
        .sum()
        .reindex(FACILITY_TYPES, fill_value=0)
        .reset_index(name="facility_count")
        .sort_values(by="facility_count", ascending=False)
        .reset_index(drop=True)
    )
    return grouped

