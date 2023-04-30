load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "inlet_loop_calcs",
    srcs = ["inlet_loop_calcs.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        ":tip_diameter",
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:inputs",
        "//ccpd/data_types:thermo_point",
        "//ccpd/data_types:working_fluid",
        "@python_deps_colorama//:pkg",
    ],
)

py_library(
    name = "inlet_utils",
    srcs = ["inlet_utils.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = ["@python_deps_colorama//:pkg"],
)

py_library(
    name = "tip_diameter",
    srcs = ["tip_diameter.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:inputs",
        "//ccpd/data_types:working_fluid",
        "@python_deps_numpy//:pkg",
        "@python_deps_scipy//:pkg",
    ],
)
