load("@rules_cc//cc:defs.bzl", "cc_library")
load("@rules_python//python:defs.bzl", "py_library")
load("@pybind11_bazel//:build_defs.bzl", "pybind_extension")

cc_library(
    name = "constants",
    hdrs = ["constants.h"],
)

pybind_extension(
    name = "_constants",
    srcs = ["_constants.cc"],
    visibility = ["//:__subpackages__"],
    deps = [":constants"],
)

py_library(
    name = "py_constants",
    data = [":_constants.so"],
    visibility = ["//:__subpackages__"],
)
