import sys
import pathlib
import os
import asyncio

SCRIPT_PATH = pathlib.Path(os.path.abspath(__file__))
SCRIPT_DIR = SCRIPT_PATH.parent

PDF_PATH = SCRIPT_DIR.parent / "ДОДАТКИ для виконання практичних робіт 2.1-2.3.pdf"
BUILD_DIR = SCRIPT_DIR.parent / "build" /   'ДОДАТКИ для виконання практичних робіт 2.1-2.3'
DPI = 150


async def main():
    if not PDF_PATH.exists():
        sys.exit(f"PDF not found: {PDF_PATH}")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    process = await asyncio.subprocess.create_subprocess_exec(
        "pdftoppm",
        "-png",
        "-r", str(DPI),
        str(PDF_PATH),
        str(BUILD_DIR / "page"),
    )
    await process.communicate()

    # pdftoppm pads page numbers inconsistently across versions; normalize to page-001.png etc.
    for f in sorted(BUILD_DIR.glob("page-*.png")):
        digits = f.stem.split("-")[-1]
        new_name = BUILD_DIR / f"page-{int(digits):03d}.png"
        if f != new_name:
            f.rename(new_name)

    pages = sorted(BUILD_DIR.glob("page-*.png"))
    print(f"Wrote {len(pages)} PNGs to {BUILD_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
