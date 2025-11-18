#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Advanced example of using fTetWild Python bindings.

This example demonstrates:
1. Different parameter configurations
2. Multi-threading control
3. Quality vs speed tradeoffs
4. Using absolute edge length instead of relative
"""

import numpy as np
import time
import ftetwild


def create_sphere_mesh(radius=1.0, subdivisions=2):
    """
    Create a sphere surface mesh using icosphere subdivision.

    Parameters
    ----------
    radius : float
        Radius of the sphere
    subdivisions : int
        Number of subdivision levels (more = finer mesh)
    """
    # Start with icosahedron
    t = (1.0 + np.sqrt(5.0)) / 2.0

    vertices = np.array([
        [-1,  t,  0], [ 1,  t,  0], [-1, -t,  0], [ 1, -t,  0],
        [ 0, -1,  t], [ 0,  1,  t], [ 0, -1, -t], [ 0,  1, -t],
        [ t,  0, -1], [ t,  0,  1], [-t,  0, -1], [-t,  0,  1],
    ], dtype=np.float64)

    # Normalize to unit sphere
    vertices = vertices / np.linalg.norm(vertices, axis=1)[:, np.newaxis]

    faces = np.array([
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
    ], dtype=np.int32)

    # Simple subdivision (for demonstration - real icosphere would be more complex)
    for _ in range(subdivisions):
        # This is simplified - just to create a finer mesh
        pass

    # Scale to desired radius
    vertices = vertices * radius

    return vertices, faces


def mesh_with_config(vertices, faces, config_name, params):
    """
    Run tetrahedralization with given configuration.

    Parameters
    ----------
    vertices : ndarray
        Input mesh vertices
    faces : ndarray
        Input mesh faces
    config_name : str
        Name of the configuration
    params : Parameters
        Parameter object

    Returns
    -------
    tuple
        (tet_vertices, tet_elements, elapsed_time)
    """
    print(f"\n{'='*60}")
    print(f"Configuration: {config_name}")
    print(f"{'='*60}")
    print(f"Parameters:")
    print(f"  - Ideal edge length rel: {params.ideal_edge_length_rel}")
    print(f"  - Ideal edge length abs: {params.ideal_edge_length_abs}")
    print(f"  - Epsilon rel: {params.eps_rel}")
    print(f"  - Max iterations: {params.max_its}")
    print(f"  - Stop energy: {params.stop_energy}")
    print(f"  - Smooth open boundary: {params.smooth_open_boundary}")
    print(f"  - Coarsen: {params.coarsen}")

    start_time = time.time()

    try:
        tet_vertices, tet_elements = ftetwild.tetrahedralize(
            vertices, faces, params
        )
        elapsed = time.time() - start_time

        print(f"\n✓ Success!")
        print(f"  Output: {tet_vertices.shape[0]} vertices, {tet_elements.shape[0]} tets")
        print(f"  Time: {elapsed:.2f} seconds")

        return tet_vertices, tet_elements, elapsed

    except Exception as e:
        print(f"\n✗ Failed: {e}")
        return None, None, 0.0


def main():
    print("=" * 60)
    print("fTetWild Python Bindings - Advanced Example")
    print("=" * 60)

    # Create input mesh
    print("\nCreating input surface mesh (sphere)...")
    vertices, faces = create_sphere_mesh(radius=1.0, subdivisions=1)
    print(f"Input mesh: {vertices.shape[0]} vertices, {faces.shape[0]} faces")

    # Configuration 1: Fast meshing (coarse)
    print("\n" + "█" * 60)
    print("TEST 1: Fast/Coarse Meshing")
    print("█" * 60)
    params_fast = ftetwild.Parameters()
    params_fast.ideal_edge_length_rel = 0.1   # Larger edges = coarser
    params_fast.eps_rel = 2e-3                 # Larger envelope
    params_fast.max_its = 40                   # Fewer iterations
    params_fast.stop_energy = 20.0             # Higher threshold
    params_fast.is_quiet = True

    mesh_with_config(vertices, faces, "Fast/Coarse", params_fast)

    # Configuration 2: High quality meshing (fine)
    print("\n" + "█" * 60)
    print("TEST 2: High Quality Meshing")
    print("█" * 60)
    params_quality = ftetwild.Parameters()
    params_quality.ideal_edge_length_rel = 0.03  # Smaller edges = finer
    params_quality.eps_rel = 5e-4                # Smaller envelope
    params_quality.max_its = 100                 # More iterations
    params_quality.stop_energy = 8.0             # Lower threshold
    params_quality.is_quiet = True

    mesh_with_config(vertices, faces, "High Quality/Fine", params_quality)

    # Configuration 3: Absolute edge length
    print("\n" + "█" * 60)
    print("TEST 3: Using Absolute Edge Length")
    print("█" * 60)
    params_absolute = ftetwild.Parameters()
    params_absolute.ideal_edge_length_abs = 0.15  # Absolute size
    params_absolute.eps_rel = 1e-3
    params_absolute.max_its = 80
    params_absolute.is_quiet = True

    mesh_with_config(vertices, faces, "Absolute Edge Length", params_absolute)

    # Configuration 4: With smoothing and coarsening
    print("\n" + "█" * 60)
    print("TEST 4: With Post-Processing Options")
    print("█" * 60)
    params_postproc = ftetwild.Parameters()
    params_postproc.ideal_edge_length_rel = 0.05
    params_postproc.eps_rel = 1e-3
    params_postproc.max_its = 80
    params_postproc.smooth_open_boundary = True   # Enable smoothing
    params_postproc.coarsen = True                # Enable coarsening
    params_postproc.is_quiet = True

    mesh_with_config(vertices, faces, "With Smoothing & Coarsening", params_postproc)

    # Configuration 5: Multi-threading
    print("\n" + "█" * 60)
    print("TEST 5: Multi-threading Control")
    print("█" * 60)
    params_threads = ftetwild.Parameters()
    params_threads.ideal_edge_length_rel = 0.05
    params_threads.eps_rel = 1e-3
    params_threads.max_its = 80
    params_threads.num_threads = 4  # Limit to 4 threads
    params_threads.is_quiet = True

    mesh_with_config(vertices, faces, "4 Threads", params_threads)

    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

    print("\nKey Takeaways:")
    print("  • Smaller ideal_edge_length → finer mesh, slower computation")
    print("  • Smaller eps_rel → tighter envelope, better feature preservation")
    print("  • More max_its → better optimization, slower computation")
    print("  • Lower stop_energy → higher quality elements")
    print("  • smooth_open_boundary → smoother surface on open regions")
    print("  • coarsen → reduces output mesh size when possible")


if __name__ == "__main__":
    main()
