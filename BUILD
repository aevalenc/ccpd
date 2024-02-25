load("@rules_python//python:defs.bzl", "py_binary")
load("@rules_python//python:packaging.bzl", "py_wheel")

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

py_wheel(
    name = "ccpd_wheel",
    distribution = "ccpd",
    python_tag = "py3",
    version = "0.0.1",
    deps = [
        "//ccpd/cc_libraries:pybind_constants",
        "//ccpd/data_types:ccpd_data_types",
    ],
)
