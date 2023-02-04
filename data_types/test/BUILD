load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "three_dimensional_blade_tests",
    srcs = ["three_dimensional_blade_tests.py"],
    deps = [
        "//ccpd/data_types:three_dimensional_blade",
        "@python_deps_numpy//:pkg",
    ],
)

py_test(
    name = "centrifugal_compressor_tests",
    srcs = ["centrifugal_compressor_tests.py"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor",
        "@python_deps_numpy//:pkg",
    ],
)
