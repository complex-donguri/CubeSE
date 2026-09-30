# Development guide

## Goals

- Run CubeSE on Windows and macOS.
- Preserve the behavior and availability of the completed Windows version.
- Improve maintainability without combining behavior changes with structural
  refactoring.
- Keep changes small enough to review and test independently.

## Preserved Windows baseline

The original Windows baseline is the upstream `main` commit
`40cfd0b6addfa2b73859274bd97749ab6154b807`.

It is preserved by:

- the existing historical `CubeSEv1.0.0` tag;
- the `windows-baseline-2026-09-30` tag for the upstream state used to begin
  this port; and
- the `legacy/windows-v1` branch, reserved for critical fixes to the original
  Windows application.

Do not rewrite or move baseline tags. Do not use `legacy/windows-v1` for the
cross-platform port.

## Remotes

- `origin`: this fork, where cross-platform work is pushed.
- `upstream`: the original `astro-tech-edu/CubeSE` repository.

Fetch both remotes before starting work. Review upstream changes before
integrating them; do not merge them blindly after the port begins.

## Branch and pull request workflow

The `main` branch must remain stable. Never develop directly on it.

1. Create a short-lived branch from the latest `main`.
2. Make one independently reviewable change.
3. Run the checks appropriate to the affected platform and feature.
4. Open a pull request into `main`.
5. Merge only after required Windows and macOS checks pass.

Use descriptive branch names such as:

- `build/add-cmake`
- `port/portable-cpp-io`
- `port/python-engine-launcher`
- `test/solver-characterization`
- `refactor/split-cube-state`

Keep portability changes, refactoring, and behavior changes in separate pull
requests whenever possible.

## Compatibility rules

- A change must not remove a working Windows feature merely to make macOS
  development easier.
- Keep the existing command-line protocol working until the Python GUI has
  migrated to a documented replacement.
- Use `std::filesystem::path` in C++ and `pathlib.Path` in Python for paths.
- Pass subprocess arguments as a list; do not assemble shell command strings.
- Use UTF-8 for communication between the C++ engine and Python GUI.
- Keep platform-specific behavior behind small adapter functions or classes.
- Resolve resources relative to the installed application or module, not the
  process working directory.
- Add a regression test before changing solver behavior.

## Verification levels

Every pull request must state which checks were run and which were not run.

### Engine checks

- Build with MSVC on Windows.
- Build with Apple Clang on macOS.
- Run fixed-state and fixed-scramble solver tests.
- Verify that each reported algorithm reaches its requested target state.

### GUI checks

- Launch the application.
- Load move and PLL images from a different working directory.
- Start and stop a search.
- Confirm that solver output is displayed without blocking the interface.
- Smoke-test every screen affected by the change.

If a check cannot be run, mark it `NOT VERIFIED` and explain why.

## Initial technical constraints

The current implementation contains several platform-specific assumptions that
must be removed incrementally:

- `CubeSE.exe` is hard-coded by the Python GUI.
- Windows `subprocess.STARTUPINFO` is used directly.
- engine output is decoded as Shift-JIS.
- resource paths use Windows backslashes.
- the C++ code uses `fopen_s` and Windows-style paths.
- JSON and image files are loaded relative to the current working directory.
- some search modes refer to a `Tables` directory that is not present in this
  repository and must be located or regenerated before those modes are
  considered portable.

Do not address all of these in one pull request. Establish tests first, then
replace one boundary at a time.

## Repository naming

Keep the GitHub repository name `CubeSE` during the initial port. Existing clone
URLs, references, and upstream comparisons remain clearer this way.

Reconsider the name after the macOS minimum viable product is working. If a
distinct name is needed, prefer `CubeSE-cross-platform` for clarity.
`CubeSE-universal` is also reasonable, but on Apple platforms “universal” can
specifically imply a binary containing both Intel and Apple Silicon builds.
