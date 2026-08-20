"""04_visualization.py

03_analysis.py에서 계산한 통계 결과를 기반으로
시각화용 JSON asset을 생성한다.
"""

import json
import os

import pandas as pd


INPUT_PATH = "data/processed/seoul_security_consolidated_2024.csv"
STAT_PATH = "analysis_output/factcheck_statistics.json"
OUTPUT_PATH = "analysis_output/chart_data.json"


def generate_visualization_assets():
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    # 03_analysis.py의 실제 통계 결과 사용
    with open(STAT_PATH, "r", encoding="utf-8") as f:
        stats = json.load(f)

    # ---------------------------------------------------------
    # 1. 정렬
    # ---------------------------------------------------------
    by_abs = df.sort_values(
        by="crime_count_2024",
        ascending=False,
    )

    by_per10k = df.sort_values(
        by="crime_per_10k",
        ascending=False,
    )

    # ---------------------------------------------------------
    # 2. 산점도 데이터
    # ---------------------------------------------------------
    scatter_points = []

    for _, row in df.iterrows():
        scatter_points.append(
            {
                "district": row["district"],
                "x": int(row["streetlights_2023"]),
                "y": int(row["crime_count_2024"]),
                "crime_per_10k": float(row["crime_per_10k"]),
                "streetlights_per_10k": float(
                    row["streetlights_per_10k"]
                ),
                "population": int(row["population_2024"]),
            }
        )

    # ---------------------------------------------------------
    # 3. 회귀선
    # ---------------------------------------------------------
    slope = stats["regression"]["slope"]
    intercept = stats["regression"]["intercept"]

    x_min = 0
    x_max = int(df["streetlights_2023"].max())

    regression_line = [
        {
            "x": x_min,
            "y": round(slope * x_min + intercept, 2),
        },
        {
            "x": x_max,
            "y": round(slope * x_max + intercept, 2),
        },
    ]

    # ---------------------------------------------------------
    # 4. 시각화 데이터
    # ---------------------------------------------------------
    chart_data = {
        "districts": df["district"].tolist(),

        "crime_abs": {
            "districts": by_abs["district"].tolist(),
            "counts": by_abs["crime_count_2024"].tolist(),
            "per_10k": by_abs["crime_per_10k"].tolist(),
        },

        "crime_per10k": {
            "districts": by_per10k["district"].tolist(),
            "per_10k": by_per10k["crime_per_10k"].tolist(),
            "counts": by_per10k["crime_count_2024"].tolist(),
        },

        "scatter_data": scatter_points,

        "regression_line": regression_line,

        "factcheck_correlations": {
            "abs_vs_per10k": stats["correlations"]["crime_abs_vs_per10k"],
            "street_vs_crime_abs": stats["correlations"]["streetlights_vs_crime_abs"],
            "street10k_vs_crime10k": stats["correlations"]["streetlights_10k_vs_crime_10k"],
        },
    }

    # ---------------------------------------------------------
    # 5. 저장
    # ---------------------------------------------------------
    os.makedirs("analysis_output", exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(
            chart_data,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Visualization assets saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_visualization_assets()
