import subprocess
import sys
import pathlib
import os

SCRIPT_PATH = pathlib.Path(os.path.abspath(__file__))
SCRIPT_DIR = SCRIPT_PATH.parent

PDF_PATH = SCRIPT_DIR.parent.parent / "doc_ocr.pdf"
BUILD_DIR = SCRIPT_DIR.parent.parent / "build"


def page_count(pdf_path):
    out = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":")[1].strip())
    raise RuntimeError("could not determine page count")


def main():
    if not PDF_PATH.exists():
        sys.exit(f"PDF not found: {PDF_PATH}")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    n = page_count(PDF_PATH)

    for i in range(1, n + 1):
        out_file = BUILD_DIR / f"page-{i:03d}.txt"
        subprocess.run(
            ["pdftotext", "-f", str(i), "-l", str(i), str(PDF_PATH), str(out_file)],
            check=True,
        )

    print(f"Wrote {n} TXT files to {BUILD_DIR}")


if __name__ == "__main__":
    main()
