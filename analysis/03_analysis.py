"""03_analysis.py

2024년 서울 자치구 범죄·가로등 데이터 팩트체크 및 통계 분석.
"""

import json
import os

import numpy as np
import pandas as pd


INPUT_PATH = "data/processed/seoul_security_consolidated_2024.csv"
OUTPUT_DIR = "analysis_output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "factcheck_statistics.json")


def spearman_corr(s1: pd.Series, s2: pd.Series) -> float:
    """두 변수의 Spearman 상관계수를 계산한다."""
    return float(s1.rank().corr(s2.rank(), method="pearson"))


def run_factcheck_analysis() -> None:
    df = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")

    # ---------------------------------------------------------
    # 1. 범죄 건수
    # ---------------------------------------------------------
    total_crime = int(df["crime_count_2024"].sum())
    violence = int(df["violence_2024"].sum())
    theft = int(df["theft_2024"].sum())
    sexual = int(df["sexual_violence_2024"].sum())
    murder = int(df["murder_2024"].sum())
    robbery = int(df["robbery_2024"].sum())

    # 폭력 + 절도 통합 건수
    violence_plus_theft = violence + theft

    # ---------------------------------------------------------
    # 2. 범죄 구성비
    # ---------------------------------------------------------
    v_pct = round(violence / total_crime * 100, 1)
    t_pct = round(theft / total_crime * 100, 1)
    s_pct = round(sexual / total_crime * 100, 1)
    m_pct = round(murder / total_crime * 100, 2)
    r_pct = round(robbery / total_crime * 100, 2)

    # 개별 범죄 유형을 단순 합산한 통합 비율
    vt_pct = round(violence_plus_theft / total_crime * 100, 1)

    # ---------------------------------------------------------
    # 3. 상관관계
    # ---------------------------------------------------------

    # 범죄 절대건수 vs 인구 1만 명당 범죄율
    pearson_a = float(
        df["crime_count_2024"].corr(
            df["crime_per_10k"],
            method="pearson",
        )
    )
    spearman_a = spearman_corr(
        df["crime_count_2024"],
        df["crime_per_10k"],
    )

    # 2023년 가로등 수 vs 2024년 범죄 절대건수
    pearson_b = float(
        df["streetlights_2023"].corr(
            df["crime_count_2024"],
            method="pearson",
        )
    )
    spearman_b = spearman_corr(
        df["streetlights_2023"],
        df["crime_count_2024"],
    )

    # 인구 1만 명당 가로등 vs 인구 1만 명당 범죄율
    pearson_c = float(
        df["streetlights_per_10k"].corr(
            df["crime_per_10k"],
            method="pearson",
        )
    )
    spearman_c = spearman_corr(
        df["streetlights_per_10k"],
        df["crime_per_10k"],
    )

    # ---------------------------------------------------------
    # 4. 단순 선형회귀
    # ---------------------------------------------------------
    slope, intercept = np.polyfit(
        df["streetlights_2023"],
        df["crime_count_2024"],
        1,
    )

    # ---------------------------------------------------------
    # 5. 결과 저장
    # ---------------------------------------------------------
    stat_results = {
        "exact_counts": {
            "total_crime": total_crime,
            "violence": {
                "count": violence,
                "pct": v_pct,
            },
            "theft": {
                "count": theft,
                "pct": t_pct,
            },
            "sexual_violence": {
                "count": sexual,
                "pct": s_pct,
            },
            "murder": {
                "count": murder,
                "pct": m_pct,
            },
            "robbery": {
                "count": robbery,
                "pct": r_pct,
            },
            "violence_plus_theft": {
                "count": violence_plus_theft,
                "pct": vt_pct,
            },
        },
        "correlations": {
            "crime_abs_vs_per10k": {
                "pearson_r": round(pearson_a, 3),
                "spearman_rho": round(spearman_a, 3),
            },
            "streetlights_vs_crime_abs": {
                "pearson_r": round(pearson_b, 3),
                "spearman_rho": round(spearman_b, 3),
            },
            "streetlights_10k_vs_crime_10k": {
                "pearson_r": round(pearson_c, 3),
                "spearman_rho": round(spearman_c, 3),
            },
        },
        "regression": {
            "slope": round(float(slope), 4),
            "intercept": round(float(intercept), 2),
        },
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(
            stat_results,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Violence + Theft ratio: {vt_pct}%")
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    run_factcheck_analysis()
