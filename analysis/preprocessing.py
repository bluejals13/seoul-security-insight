"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Preprocessing & Data Validation
"""

import pandas as pd
from config.settings import FACILITY_TYPES, REQUIRED_COLUMNS, SEOUL_DISTRICTS


class DataValidationError(Exception):
    """데이터 검증 실패 시 발생하는 예외 클래스"""
    pass


def validate_schema(df: pd.DataFrame) -> None:
    """필수 컬럼이 DataFrame에 존재하지 않는 경우 DataValidationError 발생"""
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise DataValidationError(f"필수 컬럼이 누락되었습니다: {missing_cols}")


def check_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """컬럼별 결측치 수량 및 비율 분석 표 반환"""
    missing_count = df.isnull().sum()
    missing_ratio = (missing_count / len(df) * 100).round(2) if len(df) > 0 else 0
    res_df = pd.DataFrame({"missing_count": missing_count, "missing_ratio": missing_ratio})
    return res_df


def validate_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """facility_id 중복 데이터 확인 및 중복 마킹 정보 반환"""
    if "facility_id" not in df.columns:
        return pd.DataFrame()
    duplicates = df[df.duplicated(subset=["facility_id"], keep=False)]
    return duplicates


def validate_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """위도/경도 유효성 검사 (서울 주변 범위: lat 37.0~38.0, lon 126.0~128.0)"""
    valid_lat = (df["latitude"] >= 37.0) & (df["latitude"] <= 38.0)
    valid_lon = (df["longitude"] >= 126.0) & (df["longitude"] <= 128.0)
    df_valid = df[valid_lat & valid_lon].copy()
    return df_valid


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """보안 인프라 데이터 검증 및 최소 전처리 수행

    Args:
        df (pd.DataFrame): 원본 데이터프레임

    Returns:
        pd.DataFrame: 검증 및 전처리 완료된 데이터프레임
    """
    if df is None or df.empty:
        raise DataValidationError("입력된 데이터프레임이 비어있습니다.")

    # 1. 스키마 검증
    validate_schema(df)

    # 카피본 생성
    cleaned_df = df.copy()

    # 2. 필수 문자열 데이터 공백 제거
    for str_col in ["district", "facility_type", "facility_name"]:
        if str_col in cleaned_df.columns:
            cleaned_df[str_col] = cleaned_df[str_col].astype(str).str.strip()

    # 3. 자치구 및 시설 유형 유효성 검사 (SEOUL_DISTRICTS & FACILITY_TYPES 필터링)
    cleaned_df = cleaned_df[
        cleaned_df["district"].isin(SEOUL_DISTRICTS)
        & cleaned_df["facility_type"].isin(FACILITY_TYPES)
    ].copy()

    # 4. 수치형 데이터 처리 (결측치를 무조건 0으로 바꾸지 않음)
    cleaned_df["latitude"] = pd.to_numeric(cleaned_df["latitude"], errors="coerce")
    cleaned_df["longitude"] = pd.to_numeric(cleaned_df["longitude"], errors="coerce")
    cleaned_df["count"] = pd.to_numeric(cleaned_df["count"], errors="coerce").fillna(1).astype(int)

    if "installed_year" in cleaned_df.columns:
        cleaned_df["installed_year"] = pd.to_numeric(cleaned_df["installed_year"], errors="coerce")

    # 5. 좌표 유효 범위 처리
    cleaned_df = validate_coordinates(cleaned_df)

    return cleaned_df

