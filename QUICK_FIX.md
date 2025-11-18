# Quick Fix for Build Error

## The Problem

Your build failed because **GMP library is missing**. The error message was:
```
Could NOT find GMP (missing: GMP_INCLUDE_DIRS GMP_LIBRARIES)
Cannot find GMP
```

## The Solution

Install GMP and other required dependencies in your conda environment:

```bash
# Activate your conda environment
conda activate meshing

# Install all required C++ dependencies
conda install -c conda-forge gmp eigen tbb

# Now install ftetwild
pip install . -v
```

## Step-by-Step Commands

```bash
# 1. Activate your environment
conda activate meshing

# 2. Install dependencies
conda install -c conda-forge gmp eigen tbb pybind11 numpy -y

# 3. Clean any partial builds
pip uninstall ftetwild -y  # If it was partially installed
rm -rf build/              # Clean build directory

# 4. Install ftetwild with verbose output
pip install . -v
```

## What Each Dependency Does

- **gmp**: GNU Multiple Precision Arithmetic Library (required for exact predicates)
- **eigen**: C++ template library for linear algebra (required for matrix operations)
- **tbb**: Intel Threading Building Blocks (optional, for parallel processing)
- **pybind11**: Python bindings generator (required for Python interface)
- **numpy**: Python numerical library (required for array handling)

## Verification

After installation completes, test it:

```bash
# Quick test
python -c "import ftetwild; print('Success!')"

# Full test
python python/test_installation.py

# Run example
python examples/basic_example.py
```

## Expected Output

During installation with `-v` flag, you should see:

```
Building wheel for ftetwild (pyproject.toml) ...
CMake configuration step...
Building ftetwild Python module...
[  5%] Building CXX object ...
[ 10%] Building CXX object ...
...
[100%] Built target ftetwild
Successfully built ftetwild
Successfully installed ftetwild-1.0.0
```

This will take 5-15 minutes with conda dependencies installed.

## Still Having Issues?

If you still get errors after installing GMP:

1. **Check GMP is installed**:
   ```bash
   conda list | grep gmp
   ```
   Should show: `gmp` package

2. **Try specifying GMP location**:
   ```bash
   export GMP_INC=$CONDA_PREFIX/include
   export GMP_LIB=$CONDA_PREFIX/lib
   pip install . -v
   ```

3. **Check for other missing dependencies**:
   ```bash
   python diagnose_build.py
   ```

## Why This Happened

The error message you saw didn't show the root cause:
```
subprocess.CalledProcessError: Command '['cmake', '--build', ...]' returned non-zero exit status 2.
```

This is because CMake configuration failed before compilation even started. The verbose build (`-v` flag) or diagnostic script would have shown the GMP error earlier.

## Prevention for Future Installs

Always install system dependencies **before** running pip install:

```bash
# Recommended installation order:
conda install -c conda-forge gmp eigen tbb pybind11 numpy  # Step 1
pip install . -v                                           # Step 2
```
