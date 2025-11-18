#!/bin/bash
# Script to test build and capture detailed error output

set -e

echo "Testing manual CMake build to see detailed errors..."
echo ""

# Clean any old build
rm -rf /tmp/ftetwild_debug_build
mkdir -p /tmp/ftetwild_debug_build
cd /tmp/ftetwild_debug_build

echo "Running CMake configuration..."
cmake /home/user/fTetWild \
    -DFLOAT_TETWILD_WITH_PYTHON=ON \
    -DFLOAT_TETWILD_TOPLEVEL_PROJECT=OFF \
    -DCMAKE_BUILD_TYPE=Release \
    2>&1 | tee cmake_config.log

echo ""
echo "Building ftetwild target..."
echo "This will show the actual compilation error..."
echo ""

cmake --build . --target ftetwild -j2 2>&1 | tee cmake_build.log

echo ""
echo "Build logs saved to:"
echo "  /tmp/ftetwild_debug_build/cmake_config.log"
echo "  /tmp/ftetwild_debug_build/cmake_build.log"
