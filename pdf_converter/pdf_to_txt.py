import subprocess
import sys
import pathlib
import os
import asyncio

SCRIPT_PATH = pathlib.Path(os.path.abspath(__file__))
SCRIPT_DIR = SCRIPT_PATH.parent

PDF_PATH = SCRIPT_DIR.parent / "ДОДАТКИ для виконання практичних робіт 2.1-2.3.pdf"
BUILD_DIR = SCRIPT_DIR.parent / "build" /   'ДОДАТКИ для виконання практичних робіт 2.1-2.3'


async def page_count(pdf_path: pathlib.Path):
    process = await asyncio.create_subprocess_exec(
        "pdfinfo", 
        str(pdf_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    stdout = stdout.decode()
    for line in stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":")[1].strip())
    raise RuntimeError("could not determine page count")


async def main():
    if not PDF_PATH.exists():
        sys.exit(f"PDF not found: {PDF_PATH}")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    n = await page_count(PDF_PATH)

    processes = [asyncio.create_subprocess_exec("pdftotext", "-f", str(i), "-l", str(i), str(PDF_PATH), str(BUILD_DIR / f"page-{i:03d}.txt")) for i in range(1, n + 1)]
    processes = await asyncio.gather(*processes)
    await asyncio.gather(*[process.communicate() for process in processes])

    print(f"Wrote {n} TXT files to {BUILD_DIR}")


if __name__ == "__main__":
    asyncio.run(main())
