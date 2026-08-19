"""Shared Seoul configuration."""

SEOUL_DISTRICTS = [
    "강남구",
    "강동구",
    "강북구",
    "강서구",
    "관악구",
    "광진구",
    "구로구",
    "금천구",
    "노원구",
    "도봉구",
    "동대문구",
    "동작구",
    "마포구",
    "서대문구",
    "서초구",
    "성동구",
    "성북구",
    "송파구",
    "양천구",
    "영등포구",
    "용산구",
    "은평구",
    "종로구",
    "중구",
    "중랑구",
]

COLOR_PALETTE = {
    "primary": "#16324F",
    "secondary": "#0B1F33",
    "accent": "#1481BA",
    "highlight": "#5BC0EB",
    "background": "#F6F9FC",
    "card": "#FFFFFF",
    "warning": "#F59E0B",
    "danger": "#DC2626",
    "success": "#059669",
    "text": "#243447",
}

# Retained for the legacy infrastructure pages.
FACILITY_TYPES = ["CCTV", "보안등", "비상벨", "방범시설", "안전시설"]
REQUIRED_COLUMNS = [
    "facility_id",
    "district",
    "facility_type",
    "facility_name",
    "latitude",
    "longitude",
    "address",
    "installed_year",
    "count",
]
FACILITY_COLORS = {
    "CCTV": "#0284C7",
    "보안등": "#F59E0B",
    "비상벨": "#EF4444",
    "방범시설": "#10B981",
    "안전시설": "#8B5CF6",
}
MOCK_DATA_NOTICE = "데모 데이터는 기존 보안 인프라 페이지에서만 사용됩니다."
