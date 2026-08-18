"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Mock Data Generator

NOTE: 이 모듈은 서비스 UI 및 데이터 분석 로직 검증용 Mock Data를 생성합니다.
실제 통계 데이터를 대표하지 않습니다 (DEMO DATA).
"""

import numpy as np
import pandas as pd
from config.settings import FACILITY_TYPES, SEOUL_DISTRICTS

# 서울시 자치구별 대략적인 중심 좌표
DISTRICT_CENTERS = {
    "강남구": (37.5172, 127.0473),
    "강동구": (37.5301, 127.1238),
    "강북구": (37.6396, 127.0255),
    "강서구": (37.5509, 126.8495),
    "관악구": (37.4784, 126.9516),
    "광진구": (37.5385, 127.0823),
    "구로구": (37.4954, 126.8874),
    "금천구": (37.4568, 126.8954),
    "노원구": (37.6542, 127.0568),
    "도봉구": (37.6688, 127.0471),
    "동대문구": (37.5744, 127.0400),
    "동작구": (37.5124, 126.9393),
    "마포구": (37.5663, 126.9016),
    "서대문구": (37.5791, 126.9368),
    "서초구": (37.4837, 127.0324),
    "성동구": (37.5635, 127.0369),
    "성북구": (37.5894, 127.0167),
    "송파구": (37.5145, 127.1061),
    "양천구": (37.5169, 126.8665),
    "영등포구": (37.5263, 126.8962),
    "용산구": (37.5326, 126.9900),
    "은평구": (37.6027, 126.9291),
    "종로구": (37.5730, 126.9794),
    "중구": (37.5641, 126.9979),
    "중랑구": (37.6065, 127.0927),
}


def generate_mock_data(sample_count_per_district: int = 20, seed: int = 42) -> pd.DataFrame:
    """서울시 25개 자치구와 5개 시설 유형이 모두 포함된 DEMO Mock Data 생성.

    Returns:
        pd.DataFrame: 데이터 스키마를 따르는 DataFrame
    """
    np.random.seed(seed)
    records = []
    facility_id_counter = 10001

    years = list(range(2018, 2025))
    year_weights = [0.08, 0.10, 0.12, 0.15, 0.18, 0.19, 0.18]

    # 시설 유형별 가중치 (CCTV와 보안등이 상대적으로 많음)
    type_weights = [0.40, 0.30, 0.15, 0.10, 0.05]

    for idx, district in enumerate(SEOUL_DISTRICTS, 1):
        center_lat, center_lon = DISTRICT_CENTERS.get(district, (37.5665, 126.9780))

        # 구별 생성 개수에 약간의 자율성 부여 (15 ~ 25개)
        count = int(np.random.normal(loc=sample_count_per_district, scale=3))
        count = max(12, min(count, 30))

        for i in range(count):
            f_type = np.random.choice(FACILITY_TYPES, p=type_weights)
            year = np.random.choice(years, p=year_weights)

            # 구 중심 기준 위치 산출 (+/- 0.015 deg 이내 변위)
            lat = round(center_lat + np.random.uniform(-0.015, 0.015), 6)
            lon = round(center_lon + np.random.uniform(-0.015, 0.015), 6)

            # count 컬럼 (해당 지점에 설치된 개수, 보통 1~5개)
            inst_count = int(np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03]))

            record = {
                "facility_id": f"SEC-{idx:02d}-{facility_id_counter}",
                "district": district,
                "facility_type": f_type,
                "facility_name": f"{district} {f_type} #{i+1}",
                "latitude": lat,
                "longitude": lon,
                "address": f"서울특별시 {district} 데모로 {np.random.randint(1, 200)}",
                "installed_year": int(year),
                "count": inst_count,
            }
            records.append(record)
            facility_id_counter += 1

    df = pd.DataFrame(records)
    return df


def get_mock_data() -> pd.DataFrame:
    """Mock Data 가져오기 Wrapper"""
    return generate_mock_data()
