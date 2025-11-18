#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple test to verify fTetWild Python bindings are working correctly.
Run this after installing the package to ensure everything is set up properly.
"""

import sys


def test_import():
    """Test that the module can be imported."""
    print("Testing import...", end=" ")
    try:
        import ftetwild
        print("✓ OK")
        return True
    except ImportError as e:
        print(f"✗ FAILED: {e}")
        return False


def test_version():
    """Test that version is accessible."""
    print("Testing version...", end=" ")
    try:
        import ftetwild
        version = ftetwild.__version__
        print(f"✓ OK (version: {version})")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_parameters():
    """Test Parameters class creation."""
    print("Testing Parameters class...", end=" ")
    try:
        import ftetwild
        params = ftetwild.Parameters()

        # Check some default values
        assert hasattr(params, 'ideal_edge_length_rel')
        assert hasattr(params, 'eps_rel')
        assert hasattr(params, 'max_its')

        # Try setting values
        params.ideal_edge_length_rel = 0.05
        params.eps_rel = 1e-3
        params.max_its = 80

        print("✓ OK")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_tetrahedralize_function():
    """Test that tetrahedralize function exists and has correct signature."""
    print("Testing tetrahedralize function...", end=" ")
    try:
        import ftetwild
        import inspect

        # Check function exists
        assert hasattr(ftetwild, 'tetrahedralize')
        assert callable(ftetwild.tetrahedralize)

        # Check signature
        sig = inspect.signature(ftetwild.tetrahedralize)
        params = list(sig.parameters.keys())
        assert 'V' in params
        assert 'F' in params
        assert 'params' in params

        print("✓ OK")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_simple_mesh():
    """Test tetrahedralization with a simple cube mesh."""
    print("Testing simple tetrahedralization...", end=" ")
    try:
        import ftetwild
        import numpy as np

        # Simple cube mesh
        vertices = np.array([
            [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0],
        ], dtype=np.float64)

        faces = np.array([
            [0, 1, 2], [0, 2, 3], [4, 6, 5], [4, 7, 6],
            [0, 5, 1], [0, 4, 5], [2, 7, 3], [2, 6, 7],
            [0, 3, 7], [0, 7, 4], [1, 5, 6], [1, 6, 2],
        ], dtype=np.int32)

        params = ftetwild.Parameters()
        params.is_quiet = True  # Suppress output during test

        tet_v, tet_e = ftetwild.tetrahedralize(vertices, faces, params)

        # Check output
        assert tet_v.shape[1] == 3, "Output vertices should be Nx3"
        assert tet_e.shape[1] == 4, "Output elements should be Mx4"
        assert len(tet_v) > 0, "Should have output vertices"
        assert len(tet_e) > 0, "Should have output elements"

        print(f"✓ OK ({len(tet_v)} verts, {len(tet_e)} tets)")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("fTetWild Python Bindings Installation Test")
    print("=" * 60)
    print()

    tests = [
        test_import,
        test_version,
        test_parameters,
        test_tetrahedralize_function,
        test_simple_mesh,
    ]

    results = []
    for test in tests:
        results.append(test())

    print()
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"✓ All tests passed ({passed}/{total})")
        print("=" * 60)
        return 0
    else:
        print(f"✗ Some tests failed ({passed}/{total} passed)")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
