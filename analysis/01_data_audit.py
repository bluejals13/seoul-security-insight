import os
import glob
import json
import pandas as pd

def get_df_info(filepath):
    encodings = ['utf-8', 'cp949', 'utf-8-sig', 'euc-kr']
    df = None
    used_enc = None
    for enc in encodings:
        try:
            df = pd.read_csv(filepath, encoding=enc)
            used_enc = enc
            break
        except Exception:
            continue
    if df is None:
        return None, None
    return df, used_enc

def analyze_dataset(filepath):
    df, enc = get_df_info(filepath)
    if df is None:
        return f"Could not read {filepath}"
    
    filename = os.path.basename(filepath)
    info = {
        "file_name": filename,
        "path": filepath,
        "encoding": enc,
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing": {col: int(nulls) for col, nulls in df.isnull().sum().items()},
        "duplicates": int(df.duplicated().sum()),
        "districts": [],
        "numeric_summary": {}
    }
    
    # Check district columns
    district_col = None
    for col in df.columns:
        if any(keyword in col for keyword in ['자치구', '구별', '지역', '시군구', '구']):
            district_col = col
            break
            
    if district_col:
        info["district_column"] = district_col
        info["districts"] = [str(x) for x in df[district_col].dropna().unique().tolist()]
    
    # Numeric summary
    num_df = df.select_dtypes(include=['number'])
    for col in num_df.columns:
        info["numeric_summary"][col] = {
            "min": float(num_df[col].min()) if not pd.isna(num_df[col].min()) else None,
            "max": float(num_df[col].max()) if not pd.isna(num_df[col].max()) else None,
            "mean": float(num_df[col].mean()) if not pd.isna(num_df[col].mean()) else None,
            "median": float(num_df[col].median()) if not pd.isna(num_df[col].median()) else None,
        }
        
    return info, df

def main():
    processed_files = sorted(glob.glob("data/processed/*.csv"))
    raw_files = sorted(glob.glob("data/raw/*.csv"))
    
    print("=== DATA AUDIT RUNNING ===")
    
    results = {}
    
    for f in processed_files:
        info, df = analyze_dataset(f)
        results[os.path.basename(f)] = info
        print(f"Processed: {os.path.basename(f)} - Rows: {info['rows']}, Cols: {info['cols']}")
        
    for f in raw_files:
        info, df = analyze_dataset(f)
        results[os.path.basename(f)] = info
        print(f"Raw: {os.path.basename(f)} - Rows: {info['rows']}, Cols: {info['cols']}")
        
    os.makedirs("analysis_output", exist_ok=True)
    with open("analysis_output/audit_summary.json", "w", encoding="utf-8") as jf:
        json.dump(results, jf, ensure_ascii=False, indent=2)
        
    print("Saved audit summary to analysis_output/audit_summary.json")

if __name__ == "__main__":
    main()
