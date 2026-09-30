"""Cross-platform locations used by the CubeSE desktop application."""

from __future__ import annotations

import os
import sys
from pathlib import Path


APPLICATION_DIRECTORY = Path(__file__).resolve().parent


def resource_path(*parts: str) -> Path:
    """Return a resource path independent of the process working directory."""

    return APPLICATION_DIRECTORY.joinpath(*parts)


def image_path(name: str) -> Path:
    return resource_path("RP", f"{name}.png")


def engine_path() -> Path:
    """Return the configured engine, or the platform's bundled executable."""

    configured_engine = os.environ.get("CUBESE_ENGINE")
    if configured_engine:
        return Path(configured_engine).expanduser().resolve()
    executable_name = "CubeSE.exe" if sys.platform == "win32" else "CubeSE"
    return APPLICATION_DIRECTORY / executable_name


def engine_environment() -> dict[str, str]:
    """Return an environment that points the engine at bundled data files."""

    environment = os.environ.copy()
    environment.setdefault("CUBESE_DATA_DIR", str(APPLICATION_DIRECTORY))
    return environment
