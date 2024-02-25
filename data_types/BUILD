load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_package")

py_library(
    name = "thermo_point",
    srcs = ["thermo_point.py"],
    visibility = ["//ccpd:__subpackages__"],
)

py_library(
    name = "inputs",
    srcs = ["inputs.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = ["@python_deps_attrs//:pkg"],
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
    visibility = ["//:__subpackages__"],
    deps = [
        ":centrifugal_compressor_geometry",
        ":thermo_point",
        ":three_dimensional_blade",
    ],
)

py_library(
    name = "three_dimensional_blade",
    srcs = ["three_dimensional_blade.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        ":centrifugal_compressor_geometry",
        "@python_deps_numpy//:pkg",
    ],
)

py_library(
    name = "centrifugal_compressor_geometry",
    srcs = ["centrifugal_compressor_geometry.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        "@python_deps_attrs//:pkg",
        "@python_deps_numpy//:pkg",
    ],
)

py_library(
    name = "test_utils",
    srcs = ["test_utils.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        ":inputs",
        ":working_fluid",
    ],
)

py_package(
    # A unique name for this target.
    name = "ccpd_data_types",
    packages = ["ccpd.data_types"],
    visibility = ["//ccpd:__pkg__"],
    deps = [":thermo_point"],
)
