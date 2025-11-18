# fTetWild Python Bindings

Python interface for **fTetWild** (Fast Tetrahedral Meshing in the Wild), enabling robust tetrahedral mesh generation directly from Python.

## Overview

The Python bindings provide a simple, intuitive interface to fTetWild's powerful meshing capabilities. Input and output are handled using NumPy arrays, making it easy to integrate with the Python scientific computing ecosystem.

## Installation

### Prerequisites

- **Python**: 3.6 or higher
- **CMake**: 3.20 or higher
- **C++ Compiler**: Supporting C++14
- **Dependencies**: GMP, Eigen3, TBB (optional)

### Install from Source

#### Option 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/wildmeshing/fTetWild.git
cd fTetWild

# Install dependencies (conda)
conda install -c conda-forge eigen gmp tbb pybind11 numpy

# Or using apt (Linux)
sudo apt-get install libeigen3-dev libgmp-dev libtbb-dev
pip install pybind11 numpy

# Install the package
pip install .

# Or in development mode
pip install -e .
```

#### Option 2: Using CMake directly

```bash
mkdir build
cd build
cmake .. -DFLOAT_TETWILD_WITH_PYTHON=ON
make
# The Python module will be in build/python/ftetwild.*.so
```

### Verify Installation

```python
import ftetwild
print(ftetwild.__version__)
```

## Quick Start

```python
import numpy as np
import ftetwild

# Your input surface mesh (triangle mesh)
vertices = np.array([...])  # Shape: (n_vertices, 3)
faces = np.array([...])     # Shape: (n_faces, 3)

# Create parameters with defaults
params = ftetwild.Parameters()
params.ideal_edge_length_rel = 0.05  # 5% of bounding box diagonal
params.eps_rel = 1e-3                # Envelope size

# Generate tetrahedral mesh
tet_vertices, tet_elements = ftetwild.tetrahedralize(
    vertices, faces, params
)

# Results are NumPy arrays
print(f"Output: {tet_vertices.shape[0]} vertices, {tet_elements.shape[0]} tetrahedra")
```

## API Reference

### Main Function

#### `ftetwild.tetrahedralize(V, F, params, boolean_op=-1, skip_simplify=False)`

Generate a tetrahedral mesh from a triangle surface mesh.

**Parameters:**
- `V` : array_like, shape (n, 3)
  - Input vertex positions (x, y, z coordinates)
- `F` : array_like, shape (m, 3)
  - Input triangle face indices (0-indexed)
- `params` : Parameters
  - Meshing parameters object
- `boolean_op` : int, optional (default: -1)
  - Boolean operation: -1 (none), 0 (union), 1 (intersection), 2 (difference)
- `skip_simplify` : bool, optional (default: False)
  - Skip preprocessing simplification step

**Returns:**
- `V_out` : ndarray, shape (n_out, 3)
  - Output tetrahedral mesh vertices
- `T_out` : ndarray, shape (m_out, 4)
  - Output tetrahedral mesh elements (vertex indices)

**Raises:**
- `RuntimeError` : If tetrahedralization fails

**Example:**
```python
params = ftetwild.Parameters()
tet_verts, tet_elems = ftetwild.tetrahedralize(
    surface_verts, surface_faces, params
)
```

### Parameters Class

#### `ftetwild.Parameters()`

Container for all meshing parameters.

**Mesh Quality Parameters:**

- `ideal_edge_length_rel` : float (default: 0.05)
  - Ideal edge length as ratio of bounding box diagonal
  - Smaller values = finer mesh, longer computation
  - Range: typically 0.01 to 0.2

- `ideal_edge_length_abs` : float (default: 0.0)
  - Absolute ideal edge length (in world units)
  - Overrides `ideal_edge_length_rel` if > 0

- `eps_rel` : float (default: 1e-3)
  - Envelope epsilon as ratio of bounding box diagonal
  - Controls deviation from input surface
  - Smaller values = tighter fit, better features, slower

- `min_edge_len_rel` : float (default: -1)
  - Minimum edge length as ratio of bbox diagonal
  - If < 0, defaults to `eps_rel`

**Optimization Parameters:**

- `max_its` : int (default: 80)
  - Maximum number of optimization iterations
  - More iterations = better quality, longer time

- `stop_energy` : float (default: 10.0)
  - Stop when maximum element energy falls below this
  - Energy range: [3, +∞), AMIPS conformal energy
  - Lower values = higher quality, longer time
  - Suggested: ≥ 8 for complex inputs

- `stage` : int (default: 1 or 2)
  - Processing stage (for debugging)

**Boolean Flags:**

- `is_quiet` : bool (default: False)
  - Suppress console output

- `smooth_open_boundary` : bool (default: False)
  - Apply Laplacian smoothing to open boundaries
  - Useful for meshes with holes or gaps

- `manifold_surface` : bool (default: False)
  - Force output surface to be manifold

- `coarsen` : bool (default: False)
  - Coarsen output mesh as much as possible

- `disable_filtering` : bool (default: False)
  - Disable filtering of outside elements

- `use_floodfill` : bool (default: False)
  - Use flood-fill to extract interior volume

- `use_general_wn` : bool (default: False)
  - Use generalized winding number

- `use_input_for_wn` : bool (default: False)
  - Use input surface for winding number computation

**Threading:**

- `num_threads` : int (default: max available)
  - Maximum number of threads to use
  - Set to specific value to limit parallelism

**Logging:**

- `log_level` : int (default: 3)
  - Logging verbosity: 0 (most verbose) to 6 (off)

- `log_path` : str (default: "")
  - Path to log file (empty = no file logging)

**Methods:**

- `init(bbox_diag_length)` : bool
  - Initialize computed parameters based on bounding box size
  - Usually called automatically
  - Returns True on success

**Read-only Attributes (after init):**

- `bbox_diag_length` : float - Bounding box diagonal length
- `ideal_edge_length` : float - Computed ideal edge length
- `eps` : float - Computed epsilon value
- `min_edge_length` : float - Computed minimum edge length

**Example:**
```python
params = ftetwild.Parameters()

# Basic settings
params.ideal_edge_length_rel = 0.03  # Fine mesh
params.eps_rel = 5e-4                # Tight envelope
params.max_its = 100                 # More optimization
params.stop_energy = 8.0             # Higher quality

# Optional settings
params.smooth_open_boundary = True
params.num_threads = 8
params.is_quiet = True
```

## Usage Examples

### Basic Usage

```python
import numpy as np
import ftetwild

# Simple cube mesh
vertices = np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
], dtype=np.float64)

faces = np.array([
    [0,1,2], [0,2,3], [4,6,5], [4,7,6],
    [0,5,1], [0,4,5], [2,7,3], [2,6,7],
    [0,3,7], [0,7,4], [1,5,6], [1,6,2],
], dtype=np.int32)

params = ftetwild.Parameters()
tet_v, tet_e = ftetwild.tetrahedralize(vertices, faces, params)
```

### With meshio (File I/O)

```python
import meshio
import ftetwild

# Read surface mesh
mesh = meshio.read("bunny.obj")
vertices = mesh.points
faces = mesh.cells_dict["triangle"]

# Tetrahedralize
params = ftetwild.Parameters()
params.ideal_edge_length_rel = 0.05
tet_v, tet_e = ftetwild.tetrahedralize(vertices, faces, params)

# Save tetrahedral mesh
meshio.write_points_cells(
    "bunny_tet.vtk",
    tet_v,
    [("tetra", tet_e)]
)
```

### High-Quality Mesh

```python
params = ftetwild.Parameters()
params.ideal_edge_length_rel = 0.02   # Fine elements
params.eps_rel = 5e-4                  # Tight fit
params.max_its = 120                   # More optimization
params.stop_energy = 8.0               # Better quality
params.num_threads = 16                # Use 16 cores

tet_v, tet_e = ftetwild.tetrahedralize(vertices, faces, params)
```

### Fast/Coarse Mesh

```python
params = ftetwild.Parameters()
params.ideal_edge_length_rel = 0.1    # Coarse elements
params.eps_rel = 2e-3                  # Relaxed fit
params.max_its = 40                    # Fewer iterations
params.stop_energy = 15.0              # Lower quality OK

tet_v, tet_e = ftetwild.tetrahedralize(vertices, faces, params)
```

### Absolute Edge Length

```python
# Use absolute edge length (e.g., for specific unit requirements)
params = ftetwild.Parameters()
params.ideal_edge_length_abs = 0.5  # 0.5 units
params.eps_rel = 1e-3

tet_v, tet_e = ftetwild.tetrahedralize(vertices, faces, params)
```

## Integration with Python Ecosystem

### NumPy

All inputs and outputs are NumPy arrays with standard dtypes:
- Vertices: `float64`, shape `(n, 3)`
- Elements: `int32` or `int64`, shape `(m, 4)` for tetrahedra

### meshio

Read/write various mesh formats (OBJ, STL, VTK, MSH, etc.):

```python
import meshio
mesh = meshio.read("input.stl")
# ... tetrahedralize ...
meshio.write_points_cells("output.msh", tet_v, [("tetra", tet_e)])
```

### PyVista

3D visualization and analysis:

```python
import pyvista as pv
import numpy as np

# Create PyVista tetrahedral mesh
cells = np.hstack([np.full((len(tet_e), 1), 4), tet_e])
celltypes = np.full(len(tet_e), pv.CellType.TETRA)
mesh = pv.UnstructuredGrid(cells.ravel(), celltypes, tet_v)

# Visualize
mesh.plot(show_edges=True)
```

### SciPy

Integration for FEM and other scientific computing:

```python
from scipy.spatial import Delaunay  # For comparison
# fTetWild provides more robust meshing than Delaunay
```

## Performance Considerations

### Memory Requirements

- Memory usage scales with mesh complexity
- Complex models may require > 32GB RAM
- Monitor memory usage for large inputs

### Parallelization

- fTetWild uses TBB for multi-threading
- Control with `params.num_threads`
- Speedup is roughly linear with cores (up to ~16 cores)

### Quality vs. Speed Trade-offs

| Priority | `ideal_edge_length_rel` | `eps_rel` | `max_its` | `stop_energy` |
|----------|------------------------|-----------|-----------|---------------|
| Speed    | 0.1                    | 2e-3      | 40        | 20.0          |
| Balanced | 0.05                   | 1e-3      | 80        | 10.0          |
| Quality  | 0.02-0.03              | 5e-4      | 100-120   | 8.0           |

## Troubleshooting

### Import Error

```
ImportError: No module named 'ftetwild'
```

**Solution:** Ensure package is installed: `pip install .`

### Build Failures

**Missing GMP:**
```bash
# Conda
conda install -c conda-forge gmp

# Ubuntu/Debian
sudo apt-get install libgmp-dev
```

**Missing Eigen:**
```bash
# Conda
conda install -c conda-forge eigen

# Ubuntu/Debian
sudo apt-get install libeigen3-dev
```

### Runtime Issues

**Crash on complex models:**
- Increase available memory
- Try relaxed parameters (larger `eps_rel`, larger `ideal_edge_length_rel`)

**Poor quality output:**
- Decrease `stop_energy` (but ≥ 8.0 recommended)
- Increase `max_its`
- Decrease `ideal_edge_length_rel` for finer mesh
- Check input mesh orientation

**Slow performance:**
- Increase `ideal_edge_length_rel` for coarser mesh
- Decrease `max_its`
- Increase `stop_energy`
- Check `num_threads` is utilizing available cores

## Citation

If you use fTetWild in your research, please cite:

```bibtex
@article{10.1145/3386569.3392385,
  author = {Hu, Yixin and Schneider, Teseo and Wang, Bolun and Zorin, Denis and Panozzo, Daniele},
  title = {Fast Tetrahedral Meshing in the Wild},
  year = {2020},
  volume = {39},
  number = {4},
  journal = {ACM Trans. Graph.},
  articleno = {117},
}
```

## License

Mozilla Public License 2.0 (MPL-2.0)

## Support

- **GitHub Issues**: https://github.com/wildmeshing/fTetWild/issues
- **Paper**: https://yixin-hu.github.io/ftetwild.pdf
- **Examples**: See `examples/` directory

## See Also

- [Main README](README.md) - C++ interface and general information
- [Examples](examples/README.md) - More Python examples
- [TetWild](https://github.com/Yixin-Hu/TetWild) - Original version
- [TriWild](https://github.com/wildmeshing/TriWild) - 2D version
