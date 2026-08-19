# Data layers

`data/raw/` holds source CSVs exactly as received and is never modified by the application.
The analysis-year selector discovers and reads these local source families in memory:

- `5대_범죄_발생현황_<YYYY>.csv`: UTF-8 BOM, 4-row header, district-level 5-major-crime occurrence/arrest counts.
- `등록인구_<YYYY>.csv`: UTF-8 BOM, 3-row header, district-level registered population.
- `서울시_가로등_위치_2023.csv`: CP949, management ID/WGS84 latitude/longitude.

`utils/crime_streetlight_loader.py` recognizes the year from only the two filename patterns above. A newly added matching crime or population file becomes selectable without a code change. The initial selection is 2024 when available. A selected year must have both sources; missing data is shown explicitly and is never substituted with another year. Other raw files (including the 2025–2026 crime-place, emergency-bell, safe-house, and parcel-locker datasets) are intentionally excluded from this analysis and Risk Score.

`data/reference/서울시 상권분석서비스(영역-자치구).shp` and its companion files are immutable reference data. `utils/district_boundary_loader.py` validates its 25 EPSG:5181 polygons, transforms the WGS84 streetlight points, and assigns only points strictly within one district. Invalid coordinates and points outside the boundaries remain unassigned and are reported.

`utils/crime_streetlight_loader.py` converts the raw CSVs to in-memory schemas. Processed files are intentionally not written. The comparison uses the selected analysis year's crime and population data with the separately displayed actual streetlight-data year; the resulting streetlight density is explicitly labelled as a reference installation density.
