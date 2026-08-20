import os
import pandas as pd

def load_with_enc(filepath):
    for enc in ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr']:
        try:
            return pd.read_csv(filepath, encoding=enc)
        except Exception:
            continue
    raise ValueError(f"Could not load {filepath}")

def clean_and_consolidate():
    # 1. Load Crime Data 2024 (Processed)
    crime_df = load_with_enc('data/processed/5대_범죄_자치구별_2024.csv')
    # Rename columns standard
    # Columns: district, crime_count_2024, murder_2024, robbery_2024, sexual_violence_2024, theft_2024, violence_2024
    
    # 2. Load Streetlight Data 2023 (Processed)
    street_df = load_with_enc('data/processed/서울시_가로등_자치구별_2023.csv')
    street_df.columns = ['district', 'streetlights_2023']
    
    # 3. Load Population Data 2024 (Raw)
    pop_raw = load_with_enc('data/raw/등록인구_2024.csv')
    
    # Extract district and total population from pop_raw
    # In pop_raw, column 1 is district name ('자치구'), column 2 is total population ('계 (명)')
    # Let's inspect rows from row 2 down
    pop_list = []
    for idx, row in pop_raw.iterrows():
        dist = str(row.iloc[1]).strip()
        pop_str = str(row.iloc[2]).replace(',', '').strip()
        if dist not in ['자치구', '소계', 'nan', '동(2)'] and pop_str.isdigit():
            pop_list.append({'district': dist, 'population_2024': int(pop_str)})
            
    pop_df = pd.DataFrame(pop_list)
    
    # 4. Merge all datasets on 'district'
    merged = pd.merge(crime_df, street_df, on='district', how='inner')
    merged = pd.merge(merged, pop_df, on='district', how='inner')
    
    # 5. Derived Metrics
    # Crime per 10k population
    merged['crime_per_10k'] = (merged['crime_count_2024'] / merged['population_2024'] * 10000).round(2)
    merged['murder_per_10k'] = (merged['murder_2024'] / merged['population_2024'] * 10000).round(3)
    merged['robbery_per_10k'] = (merged['robbery_2024'] / merged['population_2024'] * 10000).round(3)
    merged['sexual_violence_per_10k'] = (merged['sexual_violence_2024'] / merged['population_2024'] * 10000).round(2)
    merged['theft_per_10k'] = (merged['theft_2024'] / merged['population_2024'] * 10000).round(2)
    merged['violence_per_10k'] = (merged['violence_2024'] / merged['population_2024'] * 10000).round(2)
    
    # Streetlights per 10k population
    merged['streetlights_per_10k'] = (merged['streetlights_2023'] / merged['population_2024'] * 10000).round(2)
    
    # Crime per streetlight ratio (Cautionary metric)
    # Handling 0 streetlights if any (e.g. 중랑구 in sample)
    merged['crime_per_streetlight'] = merged.apply(
        lambda r: round(r['crime_count_2024'] / r['streetlights_2023'], 2) if r['streetlights_2023'] > 0 else None,
        axis=1
    )
    
    # Save consolidated dataset
    os.makedirs('data/processed', exist_ok=True)
    merged.to_csv('data/processed/seoul_security_consolidated_2024.csv', index=False, encoding='utf-8-sig')
    print(f"Consolidated dataset created successfully! Total rows: {len(merged)}")
    print(merged.head(5))
    return merged

if __name__ == '__main__':
    clean_and_consolidate()
