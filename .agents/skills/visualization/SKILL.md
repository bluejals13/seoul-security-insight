---
name: visualization
description: Plotly 차트, Folium 지도 및 데이터 시각화 관련 코드를 작성하거나 수정할 때 사용한다.
---

# Visualization Guidelines

## 1. 시각화 라이브러리 및 모듈 구조
- **차트**: Plotly 기반 (`visualization/charts.py`)
- **지도**: Folium 기반 (`visualization/maps.py`)
- **보호 원칙**: 기존 Plotly 차트와 Folium 지도 구현을 함부로 삭제하거나 다른 라이브러리로 대체하지 않는다.

## 2. 지도 시각화 규칙
- 서울특별시 25개 자치구 전체 데이터를 다룬다.
- 서울시 외 좌표(위도/경도가 서울 영역을 벗어난 데이터)는 지도 데이터에서 자동 제외/필터링한다.
- 좌표 정보가 없는 데이터에 임의 좌표를 생성하여 지도에 표시하지 않는다.

## 3. 차트 시각화 규칙
- 통계 차트 작성 시 하드코딩된 데이터 수치를 넘기지 않는다.
- 데이터 레이어(`analysis/`)에서 계산된 DataFrame/Dict 결과를 시각화 함수 입력으로 전달받아 표현한다.
