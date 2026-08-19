"""Seoul crime-rate and streetlight analysis landing page."""

import streamlit as st

from analysis.crime_streetlight_analysis import build_comparison_dataset
from utils.crime_streetlight_loader import (
    load_crime_data,
    load_population_data,
    load_streetlight_data,
    quality_report,
)

st.set_page_config(page_title="서울 범죄율·가로등 분석", page_icon="💡", layout="wide")


def main() -> None:
    st.title("서울 자치구별 범죄율과 가로등 설치 수준")
    st.caption(
        "범죄 발생과 가로등 설치 수준의 공간적·통계적 관계를 탐색합니다. 인과관계를 주장하지 않습니다."
    )
    crime, population, lights = (
        load_crime_data(),
        load_population_data(),
        load_streetlight_data(),
    )
    report = quality_report(crime, population, lights)
    comparison, reason = build_comparison_dataset(crime, population, lights)
    c1, c2, c3 = st.columns(3)
    c1.metric(
        "2024년 서울 5대 범죄 발생",
        f"{int(crime.loc[crime['crime_type'] == '소계', 'crime_count'].sum()):,}건",
    )
    c2.metric("2026년 6월 등록인구", f"{int(population['population'].sum()):,}명")
    c3.metric("가로등 위치 레코드", f"{len(lights):,}개")
    st.subheader("데이터 출처")
    st.write(
        "- 범죄: `5대_범죄_발생현황_20260819133035.csv` (2024년, 자치구별 발생/검거)\n- 인구: `등록인구(월별)_20260819133114.csv` (2026년 6월 등록인구)\n- 가로등: `서울시 가로등 위치 정보.csv` (관리번호·위도·경도)"
    )
    if reason:
        st.warning(reason)
        st.info(
            "가로등 원본에 자치구 또는 주소가 제공되고 2024년 인구 기준 데이터가 확보되면 자치구 비교·범죄율·4분면 분석이 활성화됩니다."
        )
    else:
        st.success(f"{len(comparison)}개 자치구 비교 데이터를 생성했습니다.")
    with st.expander("데이터 품질 검증 결과"):
        st.json(report)
    st.caption("왼쪽 페이지 메뉴에서 범죄 발생, 가로등 위치, 비교 분석을 확인하세요.")


if __name__ == "__main__":
    main()
