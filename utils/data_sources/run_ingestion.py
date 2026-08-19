"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Independent Data Ingestion Pipeline CLI

NOTE:
1. Streamlit 앱 구동 시 자동 실행되지 않으며, 데이터 갱신 시 독립적으로 실행하는 파이프라인입니다.
2. API Key 미설정 또는 호출 실패 시 기존 sample/mock fallback에 영향을 주지 않고 안전하게 수집을 중단합니다.
"""

import sys
from utils.data_sources.seoul_api_client import fetch_seoul_api_data, save_raw_response
from utils.data_sources.seoul_api_processor import transform_raw_api_to_standard, save_processed_data


def run_pipeline(service_name: str = "SeoulDevicesCCTV", limit: int = 100) -> bool:
    """서울시 Open API 독립 수집 파이프라인 실행"""
    print("=" * 60)
    print("SEOUL OPEN API DATA INGESTION PIPELINE")
    print("=" * 60)

    # 1. API 호출
    print(f"[1/4] 서울시 Open API 수집 요청 (서비스: {service_name}, 수량: {limit})...")
    raw_data, success, msg = fetch_seoul_api_data(service_name=service_name, start_index=1, end_index=limit)

    if not success or not raw_data:
        print(f"❌ API 수집 실패: {msg}")
        print("💡 API Key가 설정되지 않았거나 호출에 실패한 환경입니다.")
        print("💡 기존 Sample/Mock Fallback 체계가 계속 유지됩니다.")
        return False

    # 2. Raw 보존
    print("[2/4] API 응답 원본 data/raw/ 보존 저장 중...")
    raw_path = save_raw_response(raw_data, filename=f"seoul_api_{service_name}_raw.json")
    print(f"   -> Raw 파일 저장 완료: {raw_path}")

    # 3. 표준 Schema 변환
    print("[3/4] 표준 9개 Schema 변환 및 25개 자치구 정제 중...")
    df, count = transform_raw_api_to_standard(raw_data, service_name=service_name)
    print(f"   -> 표준 레코드 변환 완료: {count}건 (Columns: {list(df.columns)})")

    # 4. Processed CSV & Metadata 저장
    print("[4/4] data/processed/ 및 메타데이터 저장 중...")
    processed_path, meta_path = save_processed_data(df, source_name=f"서울시 Open API ({service_name})")
    print(f"   -> Processed CSV: {processed_path}")
    print(f"   -> Metadata JSON: {meta_path}")

    print("=" * 60)
    print("SUCCESS: 서울시 Open API 데이터 파이프라인 갱신이 완료되었습니다.")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
