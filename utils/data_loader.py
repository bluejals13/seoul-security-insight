"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Data Loader & Architecture Layer

NOTE: 이 모듈은 데이터 소스(CSV 파일 / Mock Data)와 분석 및 UI 계층을 격리하여 
향후 공공데이터 CSV나 외부 API 연결 시 기존 분석/UI 코드 변경을 최소화합니다.
"""

from pathlib import Path
from typing import Tuple, Optional
import pandas as pd
from utils.mock_data import get_mock_data
from analysis.preprocessing import preprocess_data, validate_schema, DataValidationError

DEFAULT_RAW_DATA_PATH = Path("data/raw/security_infrastructure.csv")

# 공공데이터 한글/영문 컬럼 매핑 사전 (향후 실제 공공데이터 연결 대응용)
COLUMN_MAPPING = {
    "연번": "facility_id",
    "관리번호": "facility_id",
    "자치구": "district",
    "시군구명": "district",
    "구명": "district",
    "시설구분": "facility_type",
    "시설유형": "facility_type",
    "설치목적": "facility_type",
    "시설명": "facility_name",
    "보안등명": "facility_name",
    "위도": "latitude",
    "경도": "longitude",
    "주소": "address",
    "소재지도로명주소": "address",
    "소재지지번주소": "address",
    "설치년도": "installed_year",
    "설치연도": "installed_year",
    "수량": "count",
    "카메라대수": "count",
}


def load_security_data(data_path: Optional[str] = None) -> Tuple[pd.DataFrame, bool, str]:
    """보안 인프라 데이터를 로드하고 전처리를 거쳐 (df, is_mock, source_name) 튜플 반환

    Args:
        data_path (str, optional): 데이터 파일 경로 (기본값: data/raw/security_infrastructure.csv)

    Returns:
        Tuple[pd.DataFrame, bool, str]: (전처리 완료 DataFrame, is_mock 여부, 데이터 소스 명칭)
        
    Raises:
        DataValidationError: 실제 데이터 파일이 존재하지만 컬럼 검증에 실패한 경우
    """
    target_path = Path(data_path) if data_path else DEFAULT_RAW_DATA_PATH

    # 1. 실제 데이터 파일이 존재하는 경우 로드 시도
    if target_path.exists() and target_path.is_file():
        try:
            # Encoding fallback (utf-8 -> cp949 / euc-kr)
            try:
                raw_df = pd.read_csv(target_path, encoding="utf-8")
            except UnicodeDecodeError:
                raw_df = pd.read_csv(target_path, encoding="cp949")

            # 컬럼 매핑 표준화
            renamed_cols = {col: COLUMN_MAPPING.get(col, col) for col in raw_df.columns}
            mapped_df = raw_df.rename(columns=renamed_cols)

            # 스키마 검증 (실제 데이터 오류 시 조용히 넘기지 않고 예외 전달)
            validate_schema(mapped_df)

            cleaned_df = preprocess_data(mapped_df)
            return cleaned_df, False, f"실제 데이터 ({target_path.name})"

        except Exception as e:
            # 실제 파일이 존재하지만 훼손/오류가 발생한 경우 예외를 그대로 전파
            raise DataValidationError(f"실제 데이터 파일('{target_path}') 로드 실패: {e}") from e

    # 2. 실제 데이터 파일이 존재하지 않는 개발 환경: Mock Data 사용
    mock_df = get_mock_data()
    cleaned_df = preprocess_data(mock_df)
    return cleaned_df, True, "DEMO Mock Data"
