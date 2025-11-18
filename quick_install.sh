#!/bin/bash
# Quick installation script for fTetWild Python bindings

set -e

echo "============================================================"
echo "fTetWild Python Bindings - Quick Install Script"
echo "============================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "Error: Please run this script from the fTetWild root directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
echo "Checking Python..."
if ! command_exists python3; then
    echo "  ✗ Python 3 not found. Please install Python 3.6+"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "  ✓ $PYTHON_VERSION"

# Check pip
echo "Checking pip..."
if ! command_exists pip3 && ! python3 -m pip --version >/dev/null 2>&1; then
    echo "  ✗ pip not found. Please install pip"
    exit 1
fi
echo "  ✓ pip found"

# Check CMake
echo "Checking CMake..."
if ! command_exists cmake; then
    echo "  ✗ CMake not found. Please install CMake 3.20+"
    exit 1
fi
CMAKE_VERSION=$(cmake --version | head -n1)
echo "  ✓ $CMAKE_VERSION"

# Check if conda is available
echo ""
if command_exists conda; then
    echo "Conda detected! Recommended: install dependencies with conda"
    echo "  conda install -c conda-forge eigen gmp tbb pybind11 numpy"
    echo ""
    read -p "Install conda dependencies now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Installing conda dependencies..."
        conda install -c conda-forge eigen gmp tbb pybind11 numpy -y
    fi
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
python3 -m pip install pybind11 numpy

# Run diagnostics
echo ""
echo "Running diagnostics..."
python3 diagnose_build.py
DIAG_RESULT=$?

if [ $DIAG_RESULT -ne 0 ]; then
    echo ""
    echo "⚠ Diagnostics found issues. Please resolve them before continuing."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install ftetwild
echo ""
echo "============================================================"
echo "Installing fTetWild..."
echo "============================================================"
echo ""
echo "⏱  This will take 10-30 minutes on first install."
echo "   You'll see compilation progress below."
echo ""
echo "Starting in 3 seconds... (Ctrl+C to cancel)"
sleep 3

echo ""
python3 -m pip install . -v

# Verify installation
echo ""
echo "============================================================"
echo "Verifying installation..."
echo "============================================================"
echo ""

if python3 -c "import ftetwild" 2>/dev/null; then
    echo "✓ fTetWild successfully installed!"
    VERSION=$(python3 -c "import ftetwild; print(ftetwild.__version__)")
    echo "  Version: $VERSION"
    echo ""
    echo "Run a test:"
    echo "  python3 python/test_installation.py"
    echo ""
    echo "Try an example:"
    echo "  python3 examples/basic_example.py"
else
    echo "✗ Installation verification failed"
    echo ""
    echo "Try running: python3 python/test_installation.py"
    exit 1
fi

echo ""
echo "============================================================"
echo "Installation complete!"
echo "============================================================"
