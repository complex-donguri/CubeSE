# Cross-platform roadmap

Each phase should be delivered through one or more focused pull requests. A
later phase must not be used to justify skipping verification in an earlier
one.

## Phase 0: Preserve and characterize

- [x] Record the upstream Windows baseline.
- [x] Document the branch and compatibility policy.
- [ ] Capture representative Windows outputs and screenshots.
- [x] Add tests that validate generated solutions instead of requiring one
  exact algorithm string.
- [ ] Inventory the binary files expected under `Tables` and determine how
  they are generated or distributed.

Exit condition: current behavior is documented well enough to detect accidental
changes.

## Phase 1: Reproducible engine builds

- [x] Add CMake without reorganizing the C++ implementation.
- [x] Declare the C++ standard and RapidJSON dependency.
- [x] Build the unchanged engine on Windows CI.
- [x] Add a macOS CI build and list the remaining compiler errors.

Exit condition: a documented command builds the engine on Windows, and macOS
porting failures are visible in CI.

## Phase 2: Portable C++ engine

- [x] Isolate `fopen_s` behind portable file I/O compatibility.
- [x] Resolve embedded path separators through `std::filesystem::path`.
- [x] Accept an explicit data directory.
- [ ] Report missing or malformed data with useful errors and non-zero exit
  codes.
- [ ] Emit UTF-8 output.

Exit condition: the standard solver runs from the command line on Windows and
macOS and passes the same solution-validity tests.

## Phase 3: Portable Python launcher

- [x] Centralize executable discovery and subprocess management.
- [x] Pass subprocess arguments as a list.
- [x] Isolate Windows-only process options.
- [x] Resolve images and data through `pathlib.Path`.
- [ ] Transfer worker output to Tkinter through a queue and `after()`.

Exit condition: the standard solver can be launched and stopped from the GUI on
Windows and macOS.

## Phase 4: Restore features incrementally

- [ ] Beginner solver.
- [ ] PLL Explorer.
- [ ] OLL Explorer.
- [ ] F2L Explorer.
- [ ] Sub-step Explorer.

Each feature requires representative Windows and macOS smoke tests before it is
marked complete.

Exit condition: every feature included in the original Windows application has
an explicit supported, deferred, or unavailable status.

## Phase 5: Refactor under tests

- [ ] Split cube state and move definitions from search code.
- [ ] Split coordinate conversion and table loading from solvers.
- [ ] Replace argument-count mode dispatch with named commands while retaining
  a temporary legacy protocol.
- [ ] Split the Python models, engine client, and Tkinter views.
- [ ] Remove duplication among explorer screens and search classes only when
  tests demonstrate equivalent behavior.

Exit condition: platform code, GUI code, and solver logic have clear boundaries
without changing supported behavior.

## Phase 6: Distribution

- [ ] Produce a Windows release artifact.
- [ ] Produce an Apple Silicon macOS application.
- [ ] Decide whether an Intel or universal macOS build is required.
- [ ] Document Gatekeeper behavior, signing, and notarization status.
- [ ] Reconsider the repository name after the cross-platform release identity
  is clear.
