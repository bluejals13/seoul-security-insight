"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Data Loader & Architecture Layer

NOTE: 이 모듈은 데이터 소스(CSV 파일 / Sample Data / Raw Data / Processed Data / Mock Data)와 
분석 및 UI 계층을 격리하여 향후 공공데이터 CSV나 외부 API 연결 시 기존 분석/UI 코드 변경을 제로화합니다.
"""

import json
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import pandas as pd
from utils.mock_data import get_mock_data
from analysis.preprocessing import preprocess_data, validate_schema, DataValidationError

# 데이터 계층 경로 정의
PROCESSED_DATA_PATH = Path("data/processed/security_infrastructure.csv")
RAW_DATA_PATH = Path("data/raw/security_infrastructure.csv")
SAMPLE_DATA_PATH = Path("data/sample/sample_security_infrastructure.csv")
METADATA_DIR = Path("data/metadata")

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


def _try_read_csv(file_path: Path) -> pd.DataFrame:
    """CSV 파일을 utf-8, cp949 인코딩으로 안전하게 로드"""
    try:
        return pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(file_path, encoding="cp949")


def load_security_data(data_path: Optional[str] = None) -> Tuple[pd.DataFrame, bool, str]:
    """보안 인프라 데이터를 로드하고 전처리를 거쳐 (df, is_mock, source_name) 튜플 반환.

    탐색 우선순위 (data_path가 미지정된 경우):
    1. data/processed/security_infrastructure.csv (정제 완료 데이터)
    2. data/raw/security_infrastructure.csv (외부 원본 데이터)
    3. data/sample/sample_security_infrastructure.csv (샘플 개발 데이터)
    4. utils.mock_data.get_mock_data() (In-Memory Mock Data)

    Args:
        data_path (str, optional): 명시적 데이터 파일 경로

    Returns:
        Tuple[pd.DataFrame, bool, str]: (전처리 완료 DataFrame, is_mock/is_sample 여부, 데이터 소스 명칭)

    Raises:
        DataValidationError: 데이터 파일이 존재하지만 컬럼 검증/전처리에 실패한 경우
    """
    target_path = Path(data_path) if data_path else None

    # 명시적 경로가 전달된 경우
    if target_path:
        if target_path.exists() and target_path.is_file():
            try:
                raw_df = _try_read_csv(target_path)
                mapped_df = raw_df.rename(columns={col: COLUMN_MAPPING.get(col, col) for col in raw_df.columns})
                validate_schema(mapped_df)
                cleaned_df = preprocess_data(mapped_df)
                return cleaned_df, False, f"지정 파일 ({target_path.name})"
            except Exception as e:
                raise DataValidationError(f"지정 파일('{target_path}') 로드 실패: {e}") from e

    # 1. processed/ 데이터 확인 (실제 정제 데이터)
    if PROCESSED_DATA_PATH.exists() and PROCESSED_DATA_PATH.is_file():
        try:
            raw_df = _try_read_csv(PROCESSED_DATA_PATH)
            mapped_df = raw_df.rename(columns={col: COLUMN_MAPPING.get(col, col) for col in raw_df.columns})
            validate_schema(mapped_df)
            cleaned_df = preprocess_data(mapped_df)
            return cleaned_df, False, f"Processed 데이터 ({PROCESSED_DATA_PATH.name})"
        except Exception as e:
            raise DataValidationError(f"Processed 데이터 파일('{PROCESSED_DATA_PATH}') 로드 실패: {e}") from e

    # 2. raw/ 데이터 확인 (외부 API/다운로드 원본 데이터)
    if RAW_DATA_PATH.exists() and RAW_DATA_PATH.is_file():
        try:
            raw_df = _try_read_csv(RAW_DATA_PATH)
            mapped_df = raw_df.rename(columns={col: COLUMN_MAPPING.get(col, col) for col in raw_df.columns})
            validate_schema(mapped_df)
            cleaned_df = preprocess_data(mapped_df)
            return cleaned_df, False, f"Raw 공공데이터 ({RAW_DATA_PATH.name})"
        except Exception as e:
            raise DataValidationError(f"Raw 공공데이터 파일('{RAW_DATA_PATH}') 로드 실패: {e}") from e

    # 3. sample/ 데이터 확인 (샘플 데이터 파일)
    if SAMPLE_DATA_PATH.exists() and SAMPLE_DATA_PATH.is_file():
        try:
            raw_df = _try_read_csv(SAMPLE_DATA_PATH)
            mapped_df = raw_df.rename(columns={col: COLUMN_MAPPING.get(col, col) for col in raw_df.columns})
            validate_schema(mapped_df)
            cleaned_df = preprocess_data(mapped_df)
            return cleaned_df, True, f"Sample 데이터 ({SAMPLE_DATA_PATH.name})"
        except Exception as e:
            raise DataValidationError(f"Sample 데이터 파일('{SAMPLE_DATA_PATH}') 로드 실패: {e}") from e

    # 4. Fallback: In-memory Mock Data
    mock_df = get_mock_data()
    cleaned_df = preprocess_data(mock_df)
    return cleaned_df, True, "DEMO Mock Data"


def load_metadata(dataset_name: str = "security_infrastructure") -> Dict[str, Any]:
    """데이터셋 메타데이터 정보를 JSON 파일에서 읽어 반환.

    Args:
        dataset_name (str): 메타데이터 파일명 기준 (기본값: security_infrastructure)

    Returns:
        Dict[str, Any]: 메타데이터 딕셔너리
    """
    meta_path = METADATA_DIR / f"{dataset_name}_metadata.json"
    if meta_path.exists() and meta_path.is_file():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # 기본 Fallback 메타데이터 구조
    return {
        "dataset_name": dataset_name,
        "source": "Seoul Security Insight Registry",
        "source_type": "sample",
        "schema_version": "1.0.0",
        "collected_at": None,
        "updated_at": None,
        "status": "sample_mode",
        "description": "기본 메타데이터",
    }
