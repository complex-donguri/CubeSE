# Building CubeSE

The C++ engine is built separately from the Python/Tkinter GUI. The initial
build target intentionally keeps `CubeSE.cpp` intact so build-system changes
can be reviewed independently from the portability refactor.

## Requirements

- CMake 3.24 or newer
- A C++20 compiler
- Git and network access during initial configuration

CMake fetches the header-only RapidJSON 1.1.0 dependency at the commit recorded
in `CMakeLists.txt`. Subsequent builds reuse the copy in the build directory.

## Configure and build

Use an out-of-source build:

```console
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

With a multi-configuration generator such as Visual Studio, the executable is
written under `build/Release/CubeSE.exe`. Single-configuration generators write
it under `build/CubeSE` (or `CubeSE.exe` on Windows).

## Run the characterization tests

On Windows, run:

```console
python tests/verify_windows_baseline.py ^
  --engine build/Release/CubeSE.exe ^
  --cases tests/fixtures/windows-v1.json ^
  --output build/windows-fixed-scrambles.txt
```

The engine currently loads its precomputed data relative to the process working
directory, so run this command from the repository root. Making the data path
explicit is tracked as a later portability change.

## Current platform status

- Windows/MSVC: built and tested in GitHub Actions.
- macOS/Apple Clang: not yet supported by the original source. Portable file
  I/O and path handling are the next migration step.
