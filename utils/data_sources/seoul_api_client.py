"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Seoul Open API Client

NOTE:
1. 서울시 Open API 환경변수는 'SEOUL_OPEN_API_KEY' 하나로 통일합니다.
2. API Key 값을 코드에 하드코딩하거나 로그, raw 파일, 예외 메시지에 기록하지 않습니다.
3. 원본 API 응답은 data/raw/에 그대로 보존합니다.
"""

import os
import json
from pathlib import Path
from typing import Tuple, Optional, Dict, Any
import requests

try:
    from dotenv import load_dotenv
    # 현재 디렉터리 .env가 있는 경우에만 무경고 로드
    env_file = Path(".env")
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
except ImportError:
    pass

RAW_DIR = Path("data/raw")
SEOUL_API_BASE_URL = "http://openAPI.seoul.go.kr:8088"
ENV_KEY_NAME = "SEOUL_OPEN_API_KEY"


def get_api_key() -> Optional[str]:
    """환경변수 또는 Streamlit secrets에서 SEOUL_OPEN_API_KEY 가져오기"""
    api_key = os.getenv(ENV_KEY_NAME)
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get(ENV_KEY_NAME)
        except Exception:
            pass
    return api_key


def fetch_seoul_api_data(
    service_name: str = "SeoulDevicesCCTV",
    start_index: int = 1,
    end_index: int = 100,
    data_type: str = "json"
) -> Tuple[Optional[Dict[str, Any]], bool, str]:
    """서울시 Open API 데이터를 안전하게 호출

    API REST URL 규격:
    http://openAPI.seoul.go.kr:8088/{KEY}/{TYPE}/{SERVICE}/{START_INDEX}/{END_INDEX}/

    Returns:
        Tuple[Optional[Dict[str, Any]], bool, str]: (raw 응답 dict, 성공 여부, 결과 메시지)
    """
    api_key = get_api_key()

    if not api_key:
        return None, False, f"{ENV_KEY_NAME} 환경변수가 설정되지 않았습니다 (Sample Fallback 모드)."

    url = f"{SEOUL_API_BASE_URL}/{api_key}/{data_type}/{service_name}/{start_index}/{end_index}/"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            # 서울시 API 응답 내부 Result Code 확인 (예: RESULT.CODE == 'INFO-000')
            if service_name in data and "RESULT" in data[service_name]:
                res_code = data[service_name]["RESULT"].get("CODE", "")
                if res_code != "INFO-000":
                    msg = data[service_name]["RESULT"].get("MESSAGE", "오류")
                    return None, False, f"서울시 API 서비스 응답 오류 [{res_code}]: {msg}"
            
            return data, True, "서울시 Open API 데이터 수집 성공"
        else:
            return None, False, f"HTTP 요청 실패 (Status Code: {response.status_code})"

    except requests.exceptions.RequestException as e:
        safe_msg = str(e).replace(api_key, "***") if api_key else str(e)
        return None, False, f"네트워크 통신 오류: {safe_msg}"
    except Exception as e:
        safe_msg = str(e).replace(api_key, "***") if api_key else str(e)
        return None, False, f"API 응답 파싱 중 오류: {safe_msg}"


def save_raw_response(raw_data: Dict[str, Any], filename: str = "seoul_api_cctv_raw.json") -> Path:
    """API 원본 응답을 data/raw/에 원본 그대로 보존하여 저장"""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    target_path = RAW_DIR / filename
    
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
        
    return target_path
