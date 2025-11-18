#!/usr/bin/env python3
"""
Diagnostic script to test fTetWild Python build dependencies and process.
Run this before attempting pip install to identify potential issues.
"""

import sys
import subprocess
import os


def check_command(cmd, name):
    """Check if a command is available."""
    print(f"Checking {name}...", end=" ")
    try:
        result = subprocess.run([cmd, '--version'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ {version}")
            return True
        else:
            print(f"✗ Not found")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print(f"✗ Not found")
        return False


def check_python_package(package):
    """Check if a Python package is installed."""
    print(f"Checking Python package '{package}'...", end=" ")
    try:
        __import__(package)
        print("✓ Installed")
        return True
    except ImportError:
        print("✗ Not installed")
        return False


def check_library(lib_name, header_paths):
    """Check if a C++ library is available."""
    print(f"Checking {lib_name}...", end=" ")
    for path in header_paths:
        if os.path.exists(path):
            print(f"✓ Found at {path}")
            return True
    print("✗ Not found")
    return False


def test_cmake_configure():
    """Test CMake configuration in a temporary directory."""
    print("\nTesting CMake configuration...")
    print("-" * 60)

    test_dir = "/tmp/ftetwild_test_build"
    source_dir = "/home/user/fTetWild"

    # Clean up old test directory
    subprocess.run(['rm', '-rf', test_dir], capture_output=True)
    os.makedirs(test_dir, exist_ok=True)

    cmake_args = [
        'cmake',
        source_dir,
        '-DFLOAT_TETWILD_WITH_PYTHON=ON',
        '-DFLOAT_TETWILD_TOPLEVEL_PROJECT=OFF',
        '-DCMAKE_BUILD_TYPE=Release'
    ]

    print("Running CMake configuration...")
    print("Command:", ' '.join(cmake_args))
    print()

    try:
        result = subprocess.run(
            cmake_args,
            cwd=test_dir,
            timeout=120,
            capture_output=False  # Show output in real-time
        )

        if result.returncode == 0:
            print("\n✓ CMake configuration succeeded")
            return True
        else:
            print(f"\n✗ CMake configuration failed with code {result.returncode}")
            return False
    except subprocess.TimeoutExpired:
        print("\n✗ CMake configuration timed out after 120 seconds")
        return False
    except Exception as e:
        print(f"\n✗ CMake configuration failed: {e}")
        return False


def main():
    print("=" * 60)
    print("fTetWild Python Build Diagnostics")
    print("=" * 60)
    print()

    issues = []

    # Check basic tools
    print("1. Checking build tools:")
    print("-" * 60)
    if not check_command('cmake', 'CMake'):
        issues.append("CMake is required but not found")
    if not check_command('g++', 'G++ compiler'):
        if not check_command('clang++', 'Clang++ compiler'):
            issues.append("C++ compiler (g++ or clang++) is required")
    if not check_command('make', 'Make'):
        issues.append("Make is required but not found")

    # Check Python packages
    print("\n2. Checking Python packages:")
    print("-" * 60)
    if not check_python_package('pybind11'):
        issues.append("pybind11 is not installed (pip install pybind11)")
    if not check_python_package('numpy'):
        issues.append("numpy is not installed (pip install numpy)")

    # Check C++ libraries
    print("\n3. Checking C++ libraries:")
    print("-" * 60)
    if not check_library('Eigen3', [
        '/usr/include/eigen3',
        '/usr/local/include/eigen3',
        '/opt/homebrew/include/eigen3'
    ]):
        issues.append("Eigen3 not found (conda install eigen or apt install libeigen3-dev)")

    if not check_library('GMP', [
        '/usr/include/gmp.h',
        '/usr/local/include/gmp.h',
        '/opt/homebrew/include/gmp.h'
    ]):
        issues.append("GMP not found (conda install gmp or apt install libgmp-dev)")

    # Test CMake configuration
    print("\n4. Testing CMake configuration:")
    print("-" * 60)
    if not test_cmake_configure():
        issues.append("CMake configuration failed - check errors above")

    # Summary
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)

    if issues:
        print("\n✗ Issues found:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print("\nPlease resolve these issues before running 'pip install .'")
        return 1
    else:
        print("\n✓ All checks passed!")
        print("\nYou can now try installing with:")
        print("  pip install . -v")
        print("\nNote: The build may still take 5-10 minutes depending on your system.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
