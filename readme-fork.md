# CubeSE fork

This repository is a fork of
[astro-tech-edu/CubeSE](https://github.com/astro-tech-edu/CubeSE).

The original Windows application remains available from the upstream project
and from this repository's immutable Windows baseline tag. Development in this
fork aims to make CubeSE work on both Windows and macOS while preserving the
original solver behavior.

The work is intentionally split into small stages:

1. Preserve and characterize the existing Windows application.
2. Add reproducible Windows and macOS builds for the C++ engine.
3. Introduce a platform-independent Python-to-engine launcher.
4. Port one feature at a time, beginning with the standard solver.
5. Refactor the C++ engine and Python GUI only after behavior is covered by
   tests.

See [DEVELOPMENT.md](DEVELOPMENT.md) for the contribution workflow and
[ROADMAP.md](ROADMAP.md) for the planned migration stages.

The project remains available under the MIT License. Copyright notices and the
original project attribution must be retained.
