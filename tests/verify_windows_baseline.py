"""Validate solutions emitted by the original Windows CubeSE engine."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class CubeState:
    cp: tuple[int, ...]
    co: tuple[int, ...]
    ep: tuple[int, ...]
    eo: tuple[int, ...]

    def apply(self, move: "CubeState") -> "CubeState":
        return CubeState(
            cp=tuple(self.cp[position] for position in move.cp),
            co=tuple(
                (self.co[position] + move.co[index]) % 3
                for index, position in enumerate(move.cp)
            ),
            ep=tuple(self.ep[position] for position in move.ep),
            eo=tuple(
                (self.eo[position] + move.eo[index]) % 2
                for index, position in enumerate(move.ep)
            ),
        )


SOLVED = CubeState(
    cp=tuple(range(8)),
    co=(0,) * 8,
    ep=tuple(range(12)),
    eo=(0,) * 12,
)

QUARTER_TURNS = {
    "U": CubeState(
        (3, 0, 1, 2, 4, 5, 6, 7),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ),
    "D": CubeState(
        (0, 1, 2, 3, 5, 6, 7, 4),
        (0, 0, 0, 0, 0, 0, 0, 0),
        (0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ),
    "L": CubeState(
        (4, 1, 2, 0, 7, 5, 6, 3),
        (2, 0, 0, 1, 1, 0, 0, 2),
        (11, 1, 2, 7, 4, 5, 6, 0, 8, 9, 10, 3),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ),
    "R": CubeState(
        (0, 2, 6, 3, 4, 1, 5, 7),
        (0, 1, 2, 0, 0, 2, 1, 0),
        (0, 5, 9, 3, 4, 2, 6, 7, 8, 1, 10, 11),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ),
    "F": CubeState(
        (0, 1, 3, 7, 4, 5, 2, 6),
        (0, 0, 1, 2, 0, 0, 2, 1),
        (0, 1, 6, 10, 4, 5, 3, 7, 8, 9, 2, 11),
        (0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0),
    ),
    "B": CubeState(
        (1, 5, 2, 3, 0, 4, 6, 7),
        (1, 2, 0, 0, 2, 1, 0, 0),
        (4, 8, 2, 3, 1, 5, 6, 7, 0, 9, 10, 11),
        (1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0),
    ),
}


def build_moves() -> dict[str, CubeState]:
    moves = dict(QUARTER_TURNS)
    for name, quarter_turn in QUARTER_TURNS.items():
        half_turn = quarter_turn.apply(quarter_turn)
        moves[f"{name}2"] = half_turn
        moves[f"{name}'"] = half_turn.apply(quarter_turn)
    return moves


MOVES = build_moves()


def apply_algorithm(state: CubeState, algorithm: Iterable[str]) -> CubeState:
    for move_name in algorithm:
        try:
            move = MOVES[move_name]
        except KeyError as error:
            raise AssertionError(f"Unknown move in algorithm: {move_name}") from error
        state = state.apply(move)
    return state


def engine_arguments(
    state: CubeState, min_depth: int, max_depth: int
) -> list[str]:
    values = [*state.cp, *state.co, *state.ep, *state.eo]
    return [*(str(value) for value in values), str(min_depth), str(max_depth), "1"]


def extract_solutions(output: str) -> list[list[str]]:
    solution_lines = re.findall(r"^Solution:(.*)$", output, flags=re.MULTILINE)
    solutions = []
    for line in solution_lines:
        moves = line.replace(".", " ").split()
        unknown_moves = [move for move in moves if move not in MOVES]
        if unknown_moves:
            raise AssertionError(f"Unknown moves in engine output: {unknown_moves}")
        solutions.append(moves)
    return solutions


def verify_case(
    engine: Path,
    case: dict[str, object],
    working_directory: Path,
    environment: dict[str, str],
) -> str:
    name = str(case["name"])
    scramble = [str(move) for move in case["scramble"]]
    min_depth = int(case["min_depth"])
    max_depth = int(case["max_depth"])
    scrambled_state = apply_algorithm(SOLVED, scramble)

    result = subprocess.run(
        [
            str(engine),
            *engine_arguments(scrambled_state, min_depth, max_depth),
        ],
        cwd=working_directory,
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        check=False,
    )
    output = result.stdout + result.stderr
    if result.returncode != 0:
        raise AssertionError(
            f"{name}: engine exited with code {result.returncode}\n{output}"
        )

    solutions = extract_solutions(output)
    if not solutions:
        raise AssertionError(f"{name}: engine produced no solution\n{output}")

    for solution in solutions:
        final_state = apply_algorithm(scrambled_state, solution)
        if final_state != SOLVED:
            raise AssertionError(
                f"{name}: invalid solution {' '.join(solution)!r}\n{output}"
            )

    return (
        f"CASE: {name}\n"
        f"SCRAMBLE: {' '.join(scramble)}\n"
        f"RESULT: PASS\n"
        f"{output.rstrip()}\n"
    )


def verify_missing_data_error(engine: Path, working_directory: Path) -> str:
    missing_directory = working_directory / "missing-cubese-data"
    environment = os.environ.copy()
    environment["CUBESE_DATA_DIR"] = str(missing_directory)
    result = subprocess.run(
        [str(engine), *engine_arguments(SOLVED, 0, 0)],
        cwd=working_directory,
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )
    output = result.stdout + result.stderr
    if result.returncode == 0:
        raise AssertionError("engine succeeded with a missing data directory")
    if "Unable to open required CubeSE data file" not in output:
        raise AssertionError(f"engine returned an unclear missing-data error:\n{output}")
    return f"CASE: missing-data-directory\nRESULT: PASS\n{output.rstrip()}\n"


def check_model() -> None:
    for face in QUARTER_TURNS:
        state = apply_algorithm(SOLVED, [face] * 4)
        if state != SOLVED:
            raise AssertionError(f"Four {face} turns did not restore the cube")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", required=True, type=Path)
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--data-dir", type=Path)
    parser.add_argument("--working-directory", type=Path, default=Path.cwd())
    parser.add_argument("--check-missing-data-error", action="store_true")
    options = parser.parse_args()

    check_model()
    engine = options.engine.resolve()
    cases_file = options.cases.resolve()
    cases = json.loads(cases_file.read_text(encoding="utf-8"))["cases"]
    working_directory = options.working_directory.resolve()
    environment = os.environ.copy()
    if options.data_dir is not None:
        environment["CUBESE_DATA_DIR"] = str(options.data_dir.resolve())

    reports = [
        verify_case(engine, case, working_directory, environment) for case in cases
    ]
    if options.check_missing_data_error:
        reports.append(verify_missing_data_error(engine, working_directory))
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text("\n".join(reports), encoding="utf-8")
    print("\n".join(reports))


if __name__ == "__main__":
    main()
