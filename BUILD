load("@rules_python//python:defs.bzl", "py_binary")

package(default_visibility = ["//visibility:public"])

py_binary(
    name = "main",
    srcs = ["main.py"],
    data = [
        "design_parameters.json",
        "inputs.json",
    ],
    deps = [
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:inputs",
        "//ccpd/utilities:centrifugal_calcs",
        "@python_deps_colorama//:pkg",
    ],
)
