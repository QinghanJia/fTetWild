# fTetWild Python Examples

This directory contains example scripts demonstrating how to use the fTetWild Python bindings.

## Examples

### 1. `basic_example.py`
A simple introduction to using fTetWild from Python.

**What it demonstrates:**
- Creating a simple input mesh (cube)
- Setting basic parameters
- Running tetrahedralization
- Accessing results
- Computing basic statistics

**Usage:**
```bash
python basic_example.py
```

### 2. `advanced_example.py`
Advanced usage showing different parameter configurations and their effects.

**What it demonstrates:**
- Fast/coarse meshing configuration
- High-quality/fine meshing configuration
- Using absolute edge length vs. relative
- Post-processing options (smoothing, coarsening)
- Multi-threading control
- Performance comparisons

**Usage:**
```bash
python advanced_example.py
```

## Requirements

All examples require:
- `ftetwild` package installed
- `numpy`

Optional for file I/O:
- `meshio` - for reading/writing various mesh formats

## Installation

First, install the fTetWild Python package:

```bash
# From the repository root
pip install .

# Or in development mode
pip install -e .
```

For examples with file I/O:
```bash
pip install meshio
```

## Parameter Guide

### Key Parameters

| Parameter | Description | Default | Notes |
|-----------|-------------|---------|-------|
| `ideal_edge_length_rel` | Target edge length as fraction of bbox diagonal | 0.05 | Smaller = finer mesh |
| `ideal_edge_length_abs` | Absolute target edge length | 0.0 | Overrides relative if > 0 |
| `eps_rel` | Envelope size as fraction of bbox diagonal | 1e-3 | Smaller = tighter fit |
| `max_its` | Maximum optimization iterations | 80 | More = better quality |
| `stop_energy` | Energy threshold to stop optimization | 10.0 | Lower = better quality |
| `smooth_open_boundary` | Smooth open boundaries | False | For open meshes |
| `coarsen` | Coarsen output mesh | False | Reduces output size |
| `manifold_surface` | Force manifold output | False | Post-processing |
| `num_threads` | Max number of threads | auto | Control parallelism |

### Quality vs. Speed Trade-offs

**Fast meshing (coarse):**
```python
params.ideal_edge_length_rel = 0.1    # Larger edges
params.eps_rel = 2e-3                  # Larger envelope
params.max_its = 40                    # Fewer iterations
params.stop_energy = 20.0              # Higher threshold
```

**High-quality meshing (fine):**
```python
params.ideal_edge_length_rel = 0.03   # Smaller edges
params.eps_rel = 5e-4                  # Smaller envelope
params.max_its = 100                   # More iterations
params.stop_energy = 8.0               # Lower threshold
```

## Integration with Other Libraries

### Using with meshio

```python
import meshio
import ftetwild
import numpy as np

# Read input mesh
mesh = meshio.read("input.obj")
vertices = mesh.points
faces = mesh.cells_dict["triangle"]

# Generate tet mesh
params = ftetwild.Parameters()
tet_vertices, tet_elements = ftetwild.tetrahedralize(vertices, faces, params)

# Save output
meshio.write_points_cells(
    "output.vtk",
    tet_vertices,
    [("tetra", tet_elements)]
)
```

### Using with PyVista

```python
import pyvista as pv
import ftetwild
import numpy as np

# Read input
surface_mesh = pv.read("input.stl")
vertices = surface_mesh.points
faces = surface_mesh.faces.reshape(-1, 4)[:, 1:]  # Remove count column

# Generate tet mesh
params = ftetwild.Parameters()
tet_vertices, tet_elements = ftetwild.tetrahedralize(vertices, faces, params)

# Create PyVista mesh
cells = np.hstack([np.full((len(tet_elements), 1), 4), tet_elements])
celltypes = np.full(len(tet_elements), pv.CellType.TETRA)
tet_mesh = pv.UnstructuredGrid(cells.ravel(), celltypes, tet_vertices)

# Visualize
tet_mesh.plot(show_edges=True)
```

## Tips

1. **Start with default parameters** and adjust based on results
2. **Use relative edge length** unless you have specific size requirements
3. **Monitor memory usage** for complex models (may need >32GB for very large inputs)
4. **Input orientation matters** - ensure your input mesh normals are consistent
5. **For debugging**, set `params.is_quiet = False` to see detailed output

## Support

For questions or issues:
- GitHub Issues: https://github.com/wildmeshing/fTetWild/issues
- Paper: https://yixin-hu.github.io/ftetwild.pdf
