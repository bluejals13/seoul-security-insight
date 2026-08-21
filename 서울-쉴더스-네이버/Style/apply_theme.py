#!/usr/bin/env python3
"""
Style/apply_theme.py — 원하는 테마를 frontend/.streamlit/config.toml에 한 번에 적용하는 CLI 헬퍼.

사용법 (프로젝트 루트 또는 Style/ 디렉토리에서 실행):
    python Style/apply_theme.py white   # [라이트] 화이트 테마 적용
    python Style/apply_theme.py dark    # [다크] 다크 테마 적용

적용 후 Streamlit 서버를 재시작해야 테마가 화면에 반영된다.
    Ctrl+C 로 종료 → streamlit run frontend/app.py
"""

import argparse
import pathlib
import shutil
import sys

# 이 스크립트 위치 기준 경로
STYLE_DIR   = pathlib.Path(__file__).parent
CONFIG_PATH = STYLE_DIR.parent / "frontend" / ".streamlit" / "config.toml"

THEMES = {
    "white": STYLE_DIR / "theme_white.toml",
    "dark":  STYLE_DIR / "theme_dark.toml",
}

THEME_EMOJI = {"white": "[라이트]", "dark": "[다크]"}


def apply(theme_name: str) -> None:
    src = THEMES.get(theme_name)
    if src is None:
        print(f"[오류]  알 수 없는 테마: {theme_name!r}. 'white' 또는 'dark' 중 하나를 선택하세요.")
        sys.exit(1)
    if not src.exists():
        print(f"[오류]  테마 파일을 찾을 수 없습니다: {src}")
        sys.exit(1)

    # 기존 config.toml 백업 (.bak)
    if CONFIG_PATH.exists():
        bak = CONFIG_PATH.with_suffix(".toml.bak")
        shutil.copy2(CONFIG_PATH, bak)
        print(f"[백업]  기존 config.toml → {bak.name} 으로 백업했습니다.")

    shutil.copy2(src, CONFIG_PATH)
    emoji = THEME_EMOJI[theme_name]
    print(f"{emoji}  {theme_name} 테마를 적용했습니다: {CONFIG_PATH}")
    print("-->  변경 사항을 반영하려면 Streamlit 서버를 재시작하세요.")
    print("    Ctrl+C  →  streamlit run frontend/app.py")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="서울 쉴더스 Streamlit 테마 전환 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "theme",
        choices=list(THEMES.keys()),
        help="적용할 테마 이름 (white / dark)",
    )
    args = parser.parse_args()
    apply(args.theme)


if __name__ == "__main__":
    main()

