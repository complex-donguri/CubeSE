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
directory by default. Set `CUBESE_DATA_DIR` to run it from another directory:

```console
CUBESE_DATA_DIR=/path/to/CubeSE ./build/CubeSE [arguments...]
```

The directory must contain the `pre_culculation*.json` files. Explorer modes
also expect their binary files below its `Tables` subdirectory. Missing files
produce an error on standard error and a non-zero exit status.

## Current platform status

- Windows/MSVC: built and tested in GitHub Actions.
- macOS/Apple Clang: built and tested in GitHub Actions for the standard solver.

The original Explorer modes also refer to binary files under `Tables`. Those
files are not present in this repository, so the compatibility file-opening
layer is compiled but those modes cannot yet be exercised end to end.

## Run the GUI during development

Install Python 3, Tkinter, and Pillow, then point the GUI at the engine built
above. On macOS:

```console
CUBESE_ENGINE="$PWD/build/CubeSE" python3 CubeSE.pyw
```

On Windows PowerShell:

```powershell
$env:CUBESE_ENGINE = "$PWD\build\Release\CubeSE.exe"
python CubeSE.pyw
```

The Source build workflow also uploads each platform's compiled engine with its
test output. A downloaded macOS executable may require `chmod +x CubeSE` before
it can be launched. These CI artifacts are development builds, not signed or
notarized releases.
