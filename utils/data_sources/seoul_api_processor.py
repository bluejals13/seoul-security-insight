"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Seoul Open API Data Processor & Standardizer

NOTE:
1. API 원본 응답 데이터를 프로젝트 표준 9개 Schema로 정제/변환합니다.
2. API 응답에 존재하지 않는 수량(count), 설치연도(installed_year) 필드는 임의로 추정하거나 생성하지 않고 None/NaN 처리합니다.
3. 공식 ID가 미제공될 시 latitude, longitude, address, facility_name 조합의 SHA-256 deterministic ID를 생성합니다.
4. 표준 정제 완료 데이터는 data/processed/security_infrastructure.csv에 저장합니다.
"""

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
from config.settings import REQUIRED_COLUMNS, SEOUL_DISTRICTS

PROCESSED_DIR = Path("data/processed")
METADATA_DIR = Path("data/metadata")
PROCESSED_CSV_PATH = PROCESSED_DIR / "security_infrastructure.csv"
METADATA_JSON_PATH = METADATA_DIR / "security_infrastructure_metadata.json"


def _extract_district_from_address(address_str: str) -> Optional[str]:
    """주소 텍스트에서 서울시 25개 자치구명 추출"""
    if not address_str or not isinstance(address_str, str):
        return None
    for district in SEOUL_DISTRICTS:
        if district in address_str:
            return district
    return None


def _generate_deterministic_id(lat: Optional[float], lon: Optional[float], address: str, f_name: str) -> str:
    """공식 ID가 없을 때 동일 시설에 대해 항상 동일한 SHA-256 Deterministic ID 생성"""
    clean_lat = f"{lat:.6f}" if lat is not None else ""
    clean_lon = f"{lon:.6f}" if lon is not None else ""
    clean_addr = str(address).strip().replace(" ", "") if address else ""
    clean_name = str(f_name).strip().replace(" ", "") if f_name else ""

    raw_key = f"{clean_lat}|{clean_lon}|{clean_addr}|{clean_name}"
    hash_str = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:12].upper()
    return f"SEC-HASH-{hash_str}"


def _parse_installed_year(raw_val: Any) -> Optional[int]:
    """INSTALL_YM(YYYYMM), INST_YY(YYYY) 등 다양한 연도 포맷에서 4자리 YYYY 추출"""
    if raw_val is None:
        return None

    val_str = str(raw_val).strip()
    if not val_str:
        return None

    # 숫자만 추출 (예: "2020-05" -> "202005", "2020" -> "2020")
    digits_only = re.sub(r"\D", "", val_str)

    if len(digits_only) >= 4:
        yyyy_str = digits_only[:4]
        try:
            year = int(yyyy_str)
            if 1950 <= year <= 2030:
                return year
        except ValueError:
            pass

    return None


def transform_raw_api_to_standard(raw_data: Dict[str, Any], service_name: str = "SeoulDevicesCCTV") -> Tuple[pd.DataFrame, int]:
    """서울시 API 원본 JSON 데이터를 표준 9개 Schema DataFrame으로 변환

    Returns:
        Tuple[pd.DataFrame, int]: (표준화 DataFrame, 총 변환 레코드 수)
    """
    records: List[Dict[str, Any]] = []

    rows = []
    if isinstance(raw_data, dict):
        if service_name in raw_data and "row" in raw_data[service_name]:
            rows = raw_data[service_name]["row"]
        elif "row" in raw_data:
            rows = raw_data["row"]
    elif isinstance(raw_data, list):
        rows = raw_data

    for idx, row in enumerate(rows, 1):
        # 1. latitude & longitude
        lat = row.get("WGS84_Y") or row.get("LAT") or row.get("LATITUDE") or row.get("WGS84_LAT")
        lon = row.get("WGS84_X") or row.get("LOT") or row.get("LONGITUDE") or row.get("WGS84_LON")
        try:
            lat = float(lat) if lat is not None else None
            lon = float(lon) if lon is not None else None
        except (ValueError, TypeError):
            lat, lon = None, None

        # 2. address & district
        address = row.get("ADDR_ROAD") or row.get("ADDR_JIBUN") or row.get("ADDRESS") or row.get("LNM_ADR") or row.get("RN_ADR") or ""
        district = row.get("GU_NM") or row.get("DISTRICT") or row.get("CGG_NM") or row.get("JACHIGU")
        if not district and address:
            district = _extract_district_from_address(str(address))
        if not district:
            district = "미분류"

        # 3. facility_type & facility_name
        f_type = row.get("FACILITY_TYPE") or row.get("CCTV_USE") or row.get("PURPOSE") or "CCTV"
        f_name = row.get("CCTV_NAME") or row.get("FACILITY_NM") or row.get("LOC_DESC") or row.get("ADDR_DETAIL") or f"{district} {f_type}"

        # 4. facility_id (공식 ID 우선, 없을 경우 SHA-256 deterministic ID)
        official_id = row.get("CCTV_ID") or row.get("FACILITY_ID") or row.get("MNG_NO") or row.get("ID") or row.get("SERIAL_NO")
        if official_id and str(official_id).strip():
            f_id = str(official_id).strip()
        else:
            f_id = _generate_deterministic_id(lat, lon, address, f_name)

        # 5. installed_year (INSTALL_YM YYYYMM -> YYYY 변환, 없으면 None)
        raw_year = row.get("INSTALL_YEAR") or row.get("INST_YY") or row.get("YEAR") or row.get("INSTALL_YM") or row.get("INST_YM")
        inst_year = _parse_installed_year(raw_year)

        # 6. count (API 응답에 수량이 존재할 때만 int 변환, 없으면 None/NaN)
        raw_count = row.get("QTY") or row.get("CAMERA_COUNT") or row.get("CCTV_CNT") or row.get("CCTV_QTY") or row.get("COUNT")
        if raw_count is not None and str(raw_count).strip() != "":
            try:
                count_val = int(float(str(raw_count).strip()))
            except (ValueError, TypeError):
                count_val = None
        else:
            count_val = None

        record = {
            "facility_id": f_id,
            "district": str(district),
            "facility_type": str(f_type),
            "facility_name": str(f_name),
            "latitude": lat,
            "longitude": lon,
            "address": str(address),
            "installed_year": inst_year,
            "count": count_val,
        }
        records.append(record)

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.reindex(columns=REQUIRED_COLUMNS)

    return df, len(records)


def save_processed_data(df: pd.DataFrame, source_name: str = "Seoul Open API") -> Tuple[Path, Path]:
    """표준화된 DataFrame을 data/processed/security_infrastructure.csv에 저장하고 메타데이터 업데이트"""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(PROCESSED_CSV_PATH, index=False, encoding="utf-8")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    meta_info = {
        "dataset_name": "security_infrastructure",
        "source": source_name,
        "source_type": "api",
        "schema_version": "1.0.0",
        "collected_at": now_str,
        "updated_at": now_str,
        "status": "active_api",
        "total_records": len(df),
        "description": "서울시 Open API를 통해 정제/표준화된 치안 보안 인프라 데이터"
    }

    with open(METADATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, ensure_ascii=False, indent=2)

    return PROCESSED_CSV_PATH, METADATA_JSON_PATH
