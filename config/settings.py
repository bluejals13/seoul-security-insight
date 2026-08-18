"""
SEOUL SECURITY INFRASTRUCTURE INSIGHT - Configuration & Settings
"""

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

FACILITY_TYPES = [
    "CCTV",
    "보안등",
    "비상벨",
    "방범시설",
    "안전시설",
]

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

# Demo Data Notice Text
MOCK_DATA_NOTICE = "DEMO DATA: 현재 화면은 서비스 UI 및 분석 로직 검증을 위한 Mock Data입니다."

# UI Color Palette (Dark Navy / Security Blue)
COLOR_PALETTE = {
    "primary": "#1E293B",       # Slate Navy
    "secondary": "#0F172A",     # Dark Navy
    "accent": "#0284C7",        # Security Blue
    "highlight": "#38BDF8",     # Sky Blue
    "background": "#F8FAFC",    # Light Gray
    "card": "#FFFFFF",          # White
    "warning": "#F97316",       # Orange
    "danger": "#EF4444",        # Red
    "success": "#10B981",       # Emerald Green
    "text": "#334155",          # Dark Gray Text
}

FACILITY_COLORS = {
    "CCTV": "#0284C7",        # Security Blue
    "보안등": "#F59E0B",      # Amber Yellow
    "비상벨": "#EF4444",      # Bright Red
    "방범시설": "#10B981",    # Emerald Green
    "안전시설": "#8B5CF6",    # Purple
}
