# Windows v1 baseline

This document records observed behavior of the original Windows application
before cross-platform changes are introduced.

## Reference

- Original source baseline: `windows-baseline-2026-09-30`
- Tested pull request commit: `7d045c7`
- Workflow: `.github/workflows/windows-baseline.yml`
- Runner: GitHub-hosted `windows-2022`
- Workflow run: [Windows baseline run 36662322519](https://github.com/complex-donguri/CubeSE/actions/runs/36662322519)

## Solved-state smoke test

- Input: solved corner and edge permutation and orientation
- Search axis: UD
- Minimum depth: 0
- Maximum depth: 0
- Expected result: a zero-move solution
- Result: **PASS**

Observed output:

```text
Solution:.
(0moves) in 0 ms (UD)
```

The `.` separates the two search phases. No moves appear on either side because
the input state is already solved.

## Confirmed behavior

- The checked-in `CubeSE.exe` starts on a GitHub-hosted Windows runner.
- The required precomputed JSON files are available to the executable.
- A solved state is recognized as requiring zero moves.
- The process emits a solution and exits successfully.

## Not verified

- Solving a non-solved fixed scramble.
- Validating that a generated algorithm solves its input state.
- RL and FB search axes.
- Beginner, PLL, OLL, F2L, and sub-step modes.
- Windows GUI rendering and interaction.
- Rebuilding `CubeSE.exe` from `CubeSE.cpp`.
