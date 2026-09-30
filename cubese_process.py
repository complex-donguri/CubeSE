"""Platform adapter for launching the native CubeSE engine."""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Iterable, Sequence
from typing import Union

from cubese_runtime import engine_environment, engine_path


def legacy_command_arguments(command: str) -> list[str]:
    """Extract arguments from the GUI's legacy `CubeSE.exe ...` strings."""

    parts = command.split()
    if not parts:
        raise ValueError("CubeSE engine command is empty")
    if parts[0].lower() in {"cubese", "cubese.exe"}:
        return parts[1:]
    return parts


def start_engine(arguments: Union[str, Sequence[str]]) -> subprocess.Popen[str]:
    """Start the engine with portable paths, environment, and text output."""

    engine_arguments = (
        legacy_command_arguments(arguments)
        if isinstance(arguments, str)
        else [str(argument) for argument in arguments]
    )
    popen_options: dict[str, object] = {}
    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        popen_options["startupinfo"] = startupinfo

    return subprocess.Popen(
        [str(engine_path()), *engine_arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=engine_environment(),
        **popen_options,
    )


def iter_engine_output(process: subprocess.Popen[str]) -> Iterable[str]:
    if process.stdout is None:
        raise RuntimeError("CubeSE engine stdout is not available")
    for line in iter(process.stdout.readline, ""):
        yield line.rstrip("\r\n")
