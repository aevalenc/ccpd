load("@rules_cc//cc:defs.bzl", "cc_library")
load("@rules_python//python:defs.bzl", "py_library")
load("@pybind11_bazel//:build_defs.bzl", "pybind_extension")
load("@rules_python//python:packaging.bzl", "py_package")

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
    srcs = ["constants.py"],
    data = [":_constants.so"],
    visibility = ["//:__subpackages__"],
)

py_package(
    # A unique name for this target.
    name = "pybind_constants",
    packages = ["ccpd.cc_libraries"],
    visibility = ["//ccpd:__pkg__"],
    deps = [":py_constants"],
)
