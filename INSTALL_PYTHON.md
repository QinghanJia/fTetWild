# Installing fTetWild Python Bindings

This guide helps you install the fTetWild Python package, especially if you're experiencing build issues.

## Quick Start (If Build Gets Stuck)

The build can take **10-30 minutes** on the first run because CMake downloads and compiles many dependencies (Eigen, Geogram, TBB, etc.). This is normal!

### Installation Steps

#### Option 1: Using Conda (Recommended - Fastest)

```bash
# Create new environment
conda create -n ftetwild python=3.11
conda activate ftetwild

# Install all C++ dependencies from conda-forge
conda install -c conda-forge eigen gmp tbb cmake pybind11 numpy

# Install ftetwild (this will be much faster now)
pip install . -v
```

**Why this is faster**: Conda provides pre-built C++ libraries, so CMake doesn't need to download and compile them.

#### Option 2: Using System Package Manager (Linux)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    cmake \
    build-essential \
    libeigen3-dev \
    libgmp-dev \
    libtbb-dev \
    python3-dev

# Install Python dependencies
pip3 install pybind11 numpy

# Install ftetwild
pip3 install . -v
```

#### Option 3: Patient Install (Minimal Dependencies)

If you don't have conda or apt access, just install the Python requirements and wait:

```bash
pip install pybind11 numpy
pip install . -v   # This will take 10-30 minutes - BE PATIENT!
```

## Monitoring the Build

### See What's Happening

Use verbose mode to see build progress:

```bash
pip install . -v
```

You'll see output like:
```
Building wheel for ftetwild (setup.py) ...
[cmake] -- Downloading geogram...
[cmake] -- Building FloatTetwild library...
[ 23%] Building CXX object src/CMakeFiles/FloatTetwild.dir/AABBWrapper.cpp.o
[ 45%] Building CXX object src/CMakeFiles/FloatTetwild.dir/EdgeSplitting.cpp.o
...
```

### Check System Resources

While building, you can check CPU usage in another terminal:

```bash
# Watch CPU usage
top

# Or specifically watch the build
ps aux | grep -E "(cmake|make|c\+\+|g\+\+)"
```

## Troubleshooting

### "Build is stuck at XX%"

**It's probably NOT stuck!** C++ compilation is slow. Each file can take 30-60 seconds.

Wait indicators:
- ✓ CPU usage is high (50-100%) → It's working!
- ✗ CPU usage is low (< 10%) → Might be stuck

If truly stuck (low CPU for > 5 minutes):
1. Press Ctrl+C
2. Try again with verbose: `pip install . -v`
3. Check the last line of output

### "Cannot find GMP/Eigen/TBB"

Install system dependencies:

**Conda:**
```bash
conda install -c conda-forge gmp eigen tbb
```

**Ubuntu/Debian:**
```bash
sudo apt-get install libgmp-dev libeigen3-dev libtbb-dev
```

**macOS (Homebrew):**
```bash
brew install gmp eigen tbb
```

### "CMake Error: Could not find Python"

Specify Python explicitly:
```bash
PYTHON_EXECUTABLE=$(which python3) pip install . -v
```

### Out of Memory

If build crashes with "killed" or "out of memory":

1. **Reduce parallel jobs**: Edit `setup.py` line 53:
   ```python
   num_jobs = 2  # Instead of multiprocessing.cpu_count()
   ```

2. **Use swap space**: Add swap if needed:
   ```bash
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

3. **Clean and retry**:
   ```bash
   rm -rf build/
   pip install . -v
   ```

## Verify Installation

After installation completes:

```bash
# Quick test
python3 -c "import ftetwild; print(ftetwild.__version__)"

# Full test
python3 python/test_installation.py

# Run example
python3 examples/basic_example.py
```

## Build Time Expectations

Typical build times (first install):

| System | Time | Notes |
|--------|------|-------|
| With conda deps | 3-5 min | Dependencies pre-built |
| Modern desktop (8+ cores) | 5-10 min | Parallel compilation |
| Laptop (4 cores) | 10-20 min | Slower but normal |
| Limited resources (1-2 cores) | 20-30 min | Be very patient |
| Raspberry Pi / low memory | 30-60 min | May need swap |

Subsequent reinstalls are much faster (2-3 minutes) because dependencies are cached.

## Alternative: Pre-build with CMake

If pip install keeps failing, try building manually first:

```bash
# Configure
mkdir build && cd build
cmake .. -DFLOAT_TETWILD_WITH_PYTHON=ON

# Build (this is the slow part)
make -j$(nproc)

# Test the module
python3 -c "import sys; sys.path.insert(0, 'python'); import ftetwild; print('OK')"

# Then install with pip
cd ..
pip install .
```

## Still Having Issues?

Run the diagnostic script:

```bash
python3 diagnose_build.py
```

This will check all dependencies and try a test build to identify the problem.

## Common Error Messages Explained

### "Building wheel for ftetwild ... " (stuck for minutes)

**Status**: NORMAL - wait patiently

**Reason**: Compiling thousands of lines of C++ code

**Action**: None needed, make coffee ☕

### "error: command 'cmake' failed"

**Status**: ERROR - need to fix

**Reason**: CMake configuration failed

**Action**: Check CMake version (`cmake --version`, need 3.20+)

### "fatal error: Eigen/Dense: No such file"

**Status**: ERROR - missing dependency

**Reason**: Eigen not found

**Action**: Install Eigen (`conda install eigen` or `apt install libeigen3-dev`)

### "undefined reference to '__gmpz_init'"

**Status**: ERROR - missing dependency

**Reason**: GMP not found or not linked

**Action**: Install GMP (`conda install gmp` or `apt install libgmp-dev`)

## Pro Tips

1. **Use conda**: It's the easiest way with all pre-built dependencies

2. **Be patient**: First build takes time, this is normal for C++ projects

3. **Use verbose mode**: Always use `-v` flag to see progress

4. **Check diagnostics first**: Run `python3 diagnose_build.py` before installing

5. **Subsequent installs are fast**: Rebuilding after code changes is quick

6. **Development mode**: Use `pip install -e .` for active development

## Success Indicators

You'll know it worked when you see:

```bash
$ python3 -c "import ftetwild; print('Success!')"
Success!

$ python3 -c "import ftetwild; print(ftetwild.__version__)"
1.0.0
```

## Getting Help

If stuck after trying this guide:

1. Run diagnostics: `python3 diagnose_build.py`
2. Try verbose install: `pip install . -v 2>&1 | tee build.log`
3. Check the build log for specific errors
4. Open an issue with the build log attached

## Technical Details

The build process:

1. **CMake Configure** (1-2 min): Download dependencies, configure build
2. **Compile Dependencies** (3-10 min): Build Geogram, Eigen, etc.
3. **Compile fTetWild** (2-5 min): Build main library
4. **Compile Python Bindings** (1-2 min): Build pybind11 wrapper
5. **Create Wheel** (< 1 min): Package everything

Total: 7-20 minutes depending on system
