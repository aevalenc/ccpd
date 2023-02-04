load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "thermo_point",
    srcs = ["thermo_point.py"],
    visibility = ["//ccpd:__subpackages__"],
)

py_library(
    name = "inputs",
    srcs = ["inputs.py"],
    visibility = ["//ccpd:__subpackages__"],
)

py_library(
    name = "working_fluid",
    srcs = ["working_fluid.py"],
    visibility = ["//ccpd:__subpackages__"],
)

py_library(
    name = "material",
    srcs = ["material.py"],
    visibility = ["//ccpd:__subpackages__"],
)

py_library(
    name = "centrifugal_compressor",
    srcs = ["centrifugal_compressor.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        ":thermo_point",
        ":three_dimensional_blade",
    ],
)

py_library(
    name = "three_dimensional_blade",
    srcs = ["three_dimensional_blade.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = ["@python_deps_numpy//:pkg"],
)
