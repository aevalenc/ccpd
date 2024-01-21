load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "friction_coefficient",
    srcs = ["friction_coefficient.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        "@python_deps_colorama//:pkg",
        "@python_deps_numpy//:pkg",
    ],
)

py_library(
    name = "setup_outlet_stage",
    srcs = ["setup_outlet_stage.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:inputs",
        "//ccpd/data_types:thermo_point",
        "//ccpd/data_types:three_dimensional_blade",
        "//ccpd/data_types:working_fluid",
        "@python_deps_colorama//:pkg",
    ],
)

py_library(
    name = "optimize_mass_flow_rate",
    srcs = ["optimize_mass_flow_rate.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        ":friction_coefficient",
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:inputs",
        "//ccpd/data_types:thermo_point",
        "//ccpd/data_types:three_dimensional_blade",
        "//ccpd/data_types:working_fluid",
        "//ccpd/stages/inlet:inlet_loop_calcs",
        "//ccpd/stages/inlet:inlet_utils",
        "@python_deps_colorama//:pkg",
        "@python_deps_numpy//:pkg",
    ],
)
