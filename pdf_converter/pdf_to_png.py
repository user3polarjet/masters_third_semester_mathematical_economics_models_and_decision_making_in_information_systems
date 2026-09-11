import subprocess
import sys
import pathlib
import os

SCRIPT_PATH = pathlib.Path(os.path.abspath(__file__))
SCRIPT_DIR = SCRIPT_PATH.parent

PDF_PATH = SCRIPT_DIR.parent / "КОНСПЕКТ ЛЕКЦІЯ.pdf"
BUILD_DIR = SCRIPT_DIR.parent / "build" / PDF_PATH.name
DPI = 150


def main():
    if not PDF_PATH.exists():
        sys.exit(f"PDF not found: {PDF_PATH}")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [
            "pdftoppm",
            "-png",
            "-r", str(DPI),
            str(PDF_PATH),
            str(BUILD_DIR / "page"),
        ],
        check=True,
    )

    # pdftoppm pads page numbers inconsistently across versions; normalize to page-001.png etc.
    for f in sorted(BUILD_DIR.glob("page-*.png")):
        digits = f.stem.split("-")[-1]
        new_name = BUILD_DIR / f"page-{int(digits):03d}.png"
        if f != new_name:
            f.rename(new_name)

    pages = sorted(BUILD_DIR.glob("page-*.png"))
    print(f"Wrote {len(pages)} PNGs to {BUILD_DIR}")


if __name__ == "__main__":
    main()
