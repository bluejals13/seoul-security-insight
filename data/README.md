# Data layers

`data/raw/` holds source CSVs exactly as received and is never modified by the application.
The current analysis reads these local sources in memory:

- `5대_범죄_발생현황_20260819133035.csv`: UTF-8 BOM, 4-row header, 2024 crime occurrence/arrest counts.
- `등록인구(월별)_20260819133114.csv`: UTF-8 BOM, 3-row header, June 2026 registered population.
- `서울시 가로등 위치 정보.csv`: CP949, management ID/latitude/longitude only.

`utils/crime_streetlight_loader.py` converts them to standard in-memory schemas. Processed files are intentionally not written: the source periods do not match (crime 2024 vs population June 2026), and the streetlight source contains no district/address key. The app blocks district-level rate/density joining until matching, spatially joinable source data is supplied.
