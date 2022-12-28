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
        "//ccpd/utilities:centrifugal_calcs",
        "@python_deps_colorama//:pkg",
    ],
)
