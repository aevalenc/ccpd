load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "diffuser",
    srcs = ["diffuser_calculations.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:thermo_point",
        "//ccpd/data_types:three_dimensional_blade",
        "@python_deps_colorama//:pkg",
        "@python_deps_numpy//:pkg",
    ],
)
