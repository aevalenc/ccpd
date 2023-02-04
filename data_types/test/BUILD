load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "velocity_triangle_tests",
    srcs = ["velocity_triangle_tests.py"],
    deps = [
        "//ccpd/data_types:velocity_triangle",
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
