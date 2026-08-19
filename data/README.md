# Data layers

`data/raw/` holds source CSVs exactly as received and is never modified by the application.
The current analysis reads these local sources in memory:

- `5대_범죄_발생현황_2024.csv`: UTF-8 BOM, 4-row header, 2024 crime occurrence/arrest counts.
- `등록인구_2024.csv`: UTF-8 BOM, 3-row header, 2024 registered population.
- `서울시_가로등_위치_2023.csv`: CP949, management ID/WGS84 latitude/longitude.

`data/reference/서울시 상권분석서비스(영역-자치구).shp` and its companion files are immutable reference data. `utils/district_boundary_loader.py` validates its 25 EPSG:5181 polygons, transforms the WGS84 streetlight points, and assigns only points strictly within one district. Invalid coordinates and points outside the boundaries remain unassigned and are reported.

`utils/crime_streetlight_loader.py` converts the raw CSVs to in-memory schemas. Processed files are intentionally not written. The comparison combines 2024 crime and population with 2023 streetlight positions; the resulting streetlight density is explicitly labelled as a reference installation density.
