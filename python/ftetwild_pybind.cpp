// This file is part of fTetWild, a software for generating tetrahedral meshes.
//
// Copyright (C) 2019 Yixin Hu <yixin.hu@nyu.edu>
// This Source Code Form is subject to the terms of the Mozilla Public License
// v. 2.0. If a copy of the MPL was not distributed with this file, You can
// obtain one at http://mozilla.org/MPL/2.0/.
//

#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>

#include <floattetwild/FloatTetwild.h>
#include <floattetwild/Parameters.h>
#include <floattetwild/Types.hpp>
#include <floattetwild/Logger.hpp>

#include <geogram/mesh/mesh.h>
#include <geogram/basic/common.h>

namespace py = pybind11;

// Helper function to convert NumPy arrays to GEO::Mesh
void numpy_to_geomesh(const Eigen::MatrixXd& V, const Eigen::MatrixXi& F, GEO::Mesh& mesh) {
    mesh.clear();
    mesh.vertices.create_vertices((int)V.rows());
    for (int i = 0; i < (int)V.rows(); ++i) {
        GEO::vec3& p = mesh.vertices.point(i);
        p[0] = V(i, 0);
        p[1] = V(i, 1);
        p[2] = V(i, 2);
    }

    mesh.facets.create_triangles((int)F.rows());
    for (int i = 0; i < (int)F.rows(); ++i) {
        for (int j = 0; j < 3; ++j) {
            mesh.facets.set_vertex(i, j, F(i, j));
        }
    }
}

// Wrapper function that takes NumPy arrays
std::tuple<Eigen::MatrixXd, Eigen::MatrixXi> tetrahedralize_numpy(
    const Eigen::MatrixXd& V,
    const Eigen::MatrixXi& F,
    floatTetWild::Parameters params,
    int boolean_op = -1,
    bool skip_simplify = false)
{
    // Initialize GEO if not already done
    static bool geo_initialized = false;
    if (!geo_initialized) {
        GEO::initialize();
        geo_initialized = true;
    }

    // Convert NumPy arrays to GEO::Mesh
    GEO::Mesh geo_mesh;
    numpy_to_geomesh(V, F, geo_mesh);

    // Output matrices
    Eigen::MatrixXd VO;
    Eigen::MatrixXi TO;

    // Call the actual tetrahedralization function
    int result = floatTetWild::tetrahedralization(
        geo_mesh, params, VO, TO, boolean_op, skip_simplify
    );

    if (result != 0) {
        throw std::runtime_error("Tetrahedralization failed with error code: " + std::to_string(result));
    }

    return std::make_tuple(VO, TO);
}

PYBIND11_MODULE(ftetwild, m) {
    m.doc() = "Python bindings for fTetWild - Fast Tetrahedral Meshing in the Wild";

    // Bind the Parameters class
    py::class_<floatTetWild::Parameters>(m, "Parameters", "Parameters for tetrahedral meshing")
        .def(py::init<>(), "Default constructor")

        // File paths
        .def_readwrite("log_path", &floatTetWild::Parameters::log_path,
            "Path to log file")
        .def_readwrite("input_path", &floatTetWild::Parameters::input_path,
            "Input surface mesh path")
        .def_readwrite("output_path", &floatTetWild::Parameters::output_path,
            "Output tetrahedral mesh path")

        // Mesh quality parameters
        .def_readwrite("ideal_edge_length_rel", &floatTetWild::Parameters::ideal_edge_length_rel,
            "Ideal edge length as ratio of bounding box diagonal (default: 0.05)")
        .def_readwrite("ideal_edge_length_abs", &floatTetWild::Parameters::ideal_edge_length_abs,
            "Absolute ideal edge length (overrides relative if > 0)")
        .def_readwrite("eps_rel", &floatTetWild::Parameters::eps_rel,
            "Envelope epsilon as ratio of bounding box diagonal (default: 1e-3)")
        .def_readwrite("min_edge_len_rel", &floatTetWild::Parameters::min_edge_len_rel,
            "Minimum edge length as ratio of bounding box diagonal")

        // Optimization parameters
        .def_readwrite("max_its", &floatTetWild::Parameters::max_its,
            "Maximum number of optimization iterations (default: 80)")
        .def_readwrite("stop_energy", &floatTetWild::Parameters::stop_energy,
            "Stop optimization when max energy is below this (default: 10)")
        .def_readwrite("stage", &floatTetWild::Parameters::stage,
            "Processing stage (for debugging)")

        // Boolean flags
        .def_readwrite("is_quiet", &floatTetWild::Parameters::is_quiet,
            "Suppress console output")
        .def_readwrite("smooth_open_boundary", &floatTetWild::Parameters::smooth_open_boundary,
            "Apply Laplacian smoothing to open boundaries")
        .def_readwrite("manifold_surface", &floatTetWild::Parameters::manifold_surface,
            "Force output surface to be manifold")
        .def_readwrite("coarsen", &floatTetWild::Parameters::coarsen,
            "Coarsen output mesh as much as possible")
        .def_readwrite("disable_filtering", &floatTetWild::Parameters::disable_filtering,
            "Disable filtering of outside elements")
        .def_readwrite("use_floodfill", &floatTetWild::Parameters::use_floodfill,
            "Use flood-fill to extract interior volume")
        .def_readwrite("use_general_wn", &floatTetWild::Parameters::use_general_wn,
            "Use general winding number")
        .def_readwrite("use_input_for_wn", &floatTetWild::Parameters::use_input_for_wn,
            "Use input surface for winding number computation")
        .def_readwrite("correct_surface_orientation", &floatTetWild::Parameters::correct_surface_orientation,
            "Correct surface orientation (for debugging)")

        // Threading
        .def_readwrite("num_threads", &floatTetWild::Parameters::num_threads,
            "Maximum number of threads to use")

        // Logging
        .def_readwrite("log_level", &floatTetWild::Parameters::log_level,
            "Logging level (0=most verbose, 6=off, default: 3)")

        // Initialization method
        .def("init", &floatTetWild::Parameters::init,
            "Initialize parameters based on bounding box diagonal length",
            py::arg("bbox_diag_length"))

        // Read-only computed parameters (after init)
        .def_readonly("bbox_diag_length", &floatTetWild::Parameters::bbox_diag_length,
            "Bounding box diagonal length (computed)")
        .def_readonly("ideal_edge_length", &floatTetWild::Parameters::ideal_edge_length,
            "Computed ideal edge length")
        .def_readonly("eps", &floatTetWild::Parameters::eps,
            "Computed epsilon value")
        .def_readonly("min_edge_length", &floatTetWild::Parameters::min_edge_length,
            "Computed minimum edge length");

    // Main tetrahedralization function with NumPy interface
    m.def("tetrahedralize", &tetrahedralize_numpy,
        "Generate tetrahedral mesh from triangle surface mesh\n\n"
        "Parameters\n"
        "----------\n"
        "V : array_like, shape (n, 3)\n"
        "    Input vertex positions\n"
        "F : array_like, shape (m, 3)\n"
        "    Input triangle face indices\n"
        "params : Parameters\n"
        "    Meshing parameters\n"
        "boolean_op : int, optional\n"
        "    Boolean operation: -1=none, 0=union, 1=intersection, 2=difference (default: -1)\n"
        "skip_simplify : bool, optional\n"
        "    Skip preprocessing simplification (default: False)\n\n"
        "Returns\n"
        "-------\n"
        "V_out : ndarray, shape (n_out, 3)\n"
        "    Output tetrahedral mesh vertices\n"
        "T_out : ndarray, shape (m_out, 4)\n"
        "    Output tetrahedral mesh elements (vertex indices)\n",
        py::arg("V"),
        py::arg("F"),
        py::arg("params"),
        py::arg("boolean_op") = -1,
        py::arg("skip_simplify") = false
    );

    // Version information
    m.attr("__version__") = "1.0.0";
}
