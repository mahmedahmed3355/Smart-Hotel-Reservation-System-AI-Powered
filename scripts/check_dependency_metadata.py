from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_IN = ROOT / "requirements.in"
PYPROJECT = ROOT / "pyproject.toml"


def normalize_requirement(requirement: str) -> str:
    name = re.split(r"[<>=!~;\[\s]", requirement, maxsplit=1)[0]
    return name.lower().replace("_", "-").replace(".", "-")


def load_requirements() -> set[str]:
    dependencies: set[str] = set()

    for raw_line in REQUIREMENTS_IN.read_text().splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#") or line.startswith("-"):
            continue

        dependencies.add(normalize_requirement(line))

    return dependencies


def load_pyproject_dependencies() -> set[str]:
    with PYPROJECT.open("rb") as file:
        data = tomllib.load(file)

    dependencies = data.get("project", {}).get("dependencies", [])
    return {normalize_requirement(dependency) for dependency in dependencies}


def main() -> int:
    requirements_dependencies = load_requirements()
    pyproject_dependencies = load_pyproject_dependencies()

    missing_from_pyproject = sorted(
        requirements_dependencies - pyproject_dependencies
    )
    missing_from_requirements = sorted(
        pyproject_dependencies - requirements_dependencies
    )

    if missing_from_pyproject or missing_from_requirements:
        print("Dependency metadata mismatch detected.")

        if missing_from_pyproject:
            print(
                "Present in requirements.in but missing from "
                "pyproject.toml:"
            )
            for dependency in missing_from_pyproject:
                print(f"  - {dependency}")

        if missing_from_requirements:
            print(
                "Present in pyproject.toml but missing from "
                "requirements.in:"
            )
            for dependency in missing_from_requirements:
                print(f"  - {dependency}")

        return 1

    print(
        "Dependency metadata is consistent: "
        f"{len(requirements_dependencies)} runtime dependencies."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
