# fTetWild Python Bindings

This directory contains the Python bindings for fTetWild.

## Files

- `ftetwild_pybind.cpp` - pybind11 bindings implementation
- `CMakeLists.txt` - CMake build configuration for Python module
- `test_installation.py` - Installation verification script

## Building

### Requirements

- Python 3.6+
- pybind11
- NumPy
- CMake 3.20+
- C++14 compatible compiler

### Method 1: Using pip (Recommended)

From the repository root:

```bash
# Install dependencies
pip install pybind11 numpy

# Install ftetwild
pip install .

# Or for development
pip install -e .
```

### Method 2: Manual CMake build

From the repository root:

```bash
mkdir build
cd build
cmake .. -DFLOAT_TETWILD_WITH_PYTHON=ON
make
```

The Python module will be in `build/python/ftetwild.*.so` (or `.pyd` on Windows).

### Method 3: Using conda

```bash
# Create and activate environment
conda create -n ftetwild python=3.11
conda activate ftetwild

# Install dependencies
conda install -c conda-forge eigen gmp tbb pybind11 numpy cmake

# Install ftetwild
pip install .
```

## Testing Installation

After installation, run the test script:

```bash
python python/test_installation.py
```

Or test manually:

```python
import ftetwild
import numpy as np

# Create simple test mesh
vertices = np.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1]], dtype=np.float64)
faces = np.array([[0,1,2], [0,1,3], [0,2,3], [1,2,3]], dtype=np.int32)

# Generate tetrahedral mesh
params = ftetwild.Parameters()
tet_v, tet_e = ftetwild.tetrahedralize(vertices, faces, params)

print(f"Generated {len(tet_v)} vertices and {len(tet_e)} tetrahedra")
```

## Usage

See the main [PYTHON.md](../PYTHON.md) documentation and [examples/](../examples/) directory for usage examples.

## Troubleshooting

### "No module named 'ftetwild'"

Make sure you installed the package:
```bash
pip install .
```

### Build errors related to pybind11

Install pybind11:
```bash
pip install pybind11
```

Or with conda:
```bash
conda install -c conda-forge pybind11
```

### Missing GMP/Eigen/TBB

With conda (recommended):
```bash
conda install -c conda-forge eigen gmp tbb
```

With apt (Ubuntu/Debian):
```bash
sudo apt-get install libeigen3-dev libgmp-dev libtbb-dev
```

### CMake can't find Python

Specify Python explicitly:
```bash
cmake .. -DFLOAT_TETWILD_WITH_PYTHON=ON -DPYTHON_EXECUTABLE=$(which python3)
```

## Development

For development, install in editable mode:

```bash
pip install -e .
```

This allows you to modify the C++ code and rebuild without reinstalling:

```bash
cd build
make
```

## API Overview

### Main function

```python
ftetwild.tetrahedralize(V, F, params, boolean_op=-1, skip_simplify=False)
```

**Parameters:**
- `V`: Input vertices (Nx3 NumPy array)
- `F`: Input faces (Mx3 NumPy array)
- `params`: Parameters object
- `boolean_op`: Optional boolean operation (-1=none, 0=union, 1=intersection, 2=difference)
- `skip_simplify`: Skip preprocessing

**Returns:**
- `V_out`: Output vertices (Nx3 NumPy array)
- `T_out`: Output tetrahedra (Mx4 NumPy array)

### Parameters class

```python
params = ftetwild.Parameters()
params.ideal_edge_length_rel = 0.05  # Edge length as fraction of bbox diagonal
params.eps_rel = 1e-3                # Envelope size as fraction of bbox diagonal
params.max_its = 80                  # Max optimization iterations
params.stop_energy = 10.0            # Energy threshold to stop
params.is_quiet = False              # Show/hide console output
```

See [PYTHON.md](../PYTHON.md) for complete parameter documentation.

## License

Mozilla Public License 2.0 (MPL-2.0)
