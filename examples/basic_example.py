#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic example of using fTetWild Python bindings.

This example demonstrates how to:
1. Create a simple triangle mesh (or load from file)
2. Set meshing parameters
3. Generate tetrahedral mesh
4. Access and use the results
"""

import numpy as np
import ftetwild


def create_cube_mesh():
    """Create a simple cube surface mesh for testing."""
    # Vertices of a unit cube
    vertices = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0],
    ], dtype=np.float64)

    # Triangle faces (each face of cube has 2 triangles)
    faces = np.array([
        # Bottom face (z=0)
        [0, 1, 2], [0, 2, 3],
        # Top face (z=1)
        [4, 6, 5], [4, 7, 6],
        # Front face (y=0)
        [0, 5, 1], [0, 4, 5],
        # Back face (y=1)
        [2, 7, 3], [2, 6, 7],
        # Left face (x=0)
        [0, 3, 7], [0, 7, 4],
        # Right face (x=1)
        [1, 5, 6], [1, 6, 2],
    ], dtype=np.int32)

    return vertices, faces


def main():
    print("=" * 60)
    print("fTetWild Python Bindings - Basic Example")
    print("=" * 60)

    # Create or load input mesh
    print("\n1. Creating input surface mesh (cube)...")
    vertices, faces = create_cube_mesh()
    print(f"   Input mesh: {vertices.shape[0]} vertices, {faces.shape[0]} faces")

    # Create parameters object
    print("\n2. Setting up meshing parameters...")
    params = ftetwild.Parameters()

    # Set custom parameters (optional - these are the defaults)
    params.ideal_edge_length_rel = 0.05  # 5% of bounding box diagonal
    params.eps_rel = 1e-3                # Envelope size: 0.1% of bbox diagonal
    params.max_its = 80                  # Maximum optimization iterations
    params.stop_energy = 10.0            # Stop when energy below this value
    params.is_quiet = False              # Show output

    print(f"   - Ideal edge length (relative): {params.ideal_edge_length_rel}")
    print(f"   - Epsilon (relative): {params.eps_rel}")
    print(f"   - Max iterations: {params.max_its}")
    print(f"   - Stop energy: {params.stop_energy}")

    # Generate tetrahedral mesh
    print("\n3. Running tetrahedralization...")
    print("-" * 60)
    try:
        tet_vertices, tet_elements = ftetwild.tetrahedralize(
            vertices,
            faces,
            params
        )
        print("-" * 60)
        print("   ✓ Tetrahedralization successful!")
    except Exception as e:
        print(f"   ✗ Error during tetrahedralization: {e}")
        return

    # Display results
    print("\n4. Results:")
    print(f"   Output mesh: {tet_vertices.shape[0]} vertices, {tet_elements.shape[0]} tetrahedra")
    print(f"   Vertex array shape: {tet_vertices.shape}")
    print(f"   Element array shape: {tet_elements.shape}")

    # Basic statistics
    print("\n5. Basic statistics:")
    bbox_min = tet_vertices.min(axis=0)
    bbox_max = tet_vertices.max(axis=0)
    bbox_size = bbox_max - bbox_min
    print(f"   Bounding box: [{bbox_min[0]:.3f}, {bbox_min[1]:.3f}, {bbox_min[2]:.3f}] to "
          f"[{bbox_max[0]:.3f}, {bbox_max[1]:.3f}, {bbox_max[2]:.3f}]")
    print(f"   Bounding box size: [{bbox_size[0]:.3f}, {bbox_size[1]:.3f}, {bbox_size[2]:.3f}]")

    # Calculate volumes of tetrahedra
    def tet_volume(v0, v1, v2, v3):
        """Calculate volume of a tetrahedron."""
        return np.abs(np.dot(v1 - v0, np.cross(v2 - v0, v3 - v0))) / 6.0

    volumes = []
    for tet in tet_elements[:min(100, len(tet_elements))]:  # Sample first 100 tets
        v0, v1, v2, v3 = tet_vertices[tet]
        volumes.append(tet_volume(v0, v1, v2, v3))

    volumes = np.array(volumes)
    print(f"   Average tet volume (sample): {volumes.mean():.6f}")
    print(f"   Min tet volume (sample): {volumes.min():.6f}")
    print(f"   Max tet volume (sample): {volumes.max():.6f}")

    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)

    # Note about saving
    print("\nNote: To save the mesh, you can use your own mesh I/O methods.")
    print("The output arrays are NumPy arrays that can be easily saved or")
    print("used with other Python libraries (meshio, PyVista, etc.).")


if __name__ == "__main__":
    main()
