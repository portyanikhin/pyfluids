from __future__ import annotations

import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str], env: Optional[dict[str, str]] = None) -> int:
    task_env = os.environ.copy()
    task_env.setdefault("UV_CACHE_DIR", str(PROJECT_ROOT / ".cache" / "uv"))

    if env is not None:
        task_env.update(env)

    return subprocess.run(command, cwd=PROJECT_ROOT, env=task_env).returncode


def clean() -> int:
    directories = [
        ".cache/pytest-tmp",
        ".pytest_cache",
        ".ruff_cache",
        "htmlcov",
        "dist",
        "build",
        "src/pyfluids.egg-info",
    ]
    files = [
        ".coverage",
        "coverage.xml",
    ]

    for directory in directories:
        shutil.rmtree(PROJECT_ROOT / directory, ignore_errors=True)

    for directory in PROJECT_ROOT.rglob("__pycache__"):
        shutil.rmtree(directory, ignore_errors=True)

    for file in files:
        (PROJECT_ROOT / file).unlink(missing_ok=True)

    return 0


def formatting() -> int:
    result = run(["uv", "run", "ruff", "check", "--select", "I", "--fix", "."])
    if result != 0:
        return result

    return run(["uv", "run", "ruff", "format", "."])


def pytest_basetemp() -> str:
    basetemp = PROJECT_ROOT / ".cache" / "pytest-tmp" / str(os.getpid())
    basetemp.parent.mkdir(parents=True, exist_ok=True)
    return str(basetemp)


def tests() -> int:
    return run(
        [
            "uv",
            "run",
            "pytest",
            "-p",
            "no:cacheprovider",
            f"--basetemp={pytest_basetemp()}",
        ]
    )


def coverage() -> int:
    result = run(
        [
            "uv",
            "run",
            "pytest",
            "-p",
            "no:cacheprovider",
            f"--basetemp={pytest_basetemp()}",
            "--cov",
            "pyfluids",
            "--cov-report=xml",
            "--cov-report=html",
        ]
    )
    if result != 0:
        return result

    if os.environ.get("PYFLUIDS_SKIP_OPEN_COVERAGE") != "1":
        webbrowser.open((PROJECT_ROOT / "htmlcov" / "index.html").as_uri())

    return 0


TASKS = {
    "clean": clean,
    "formatting": formatting,
    "tests": tests,
    "coverage": coverage,
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in TASKS:
        task_names = ", ".join(sorted(TASKS))
        print(f"Usage: python .zed/tasks.py <{task_names}>", file=sys.stderr)
        return 2

    return TASKS[sys.argv[1]]()


if __name__ == "__main__":
    raise SystemExit(main())
