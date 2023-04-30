load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "tip_diameter_tests",
    srcs = ["tip_diameter_tests.py"],
    deps = ["//ccpd/utilities/inlet:tip_diameter"],
)

py_test(
    name = "inlet_loop_calcs_tests",
    srcs = ["inlet_loop_calcs_tests.py"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor_geometry",
        "//ccpd/data_types:thermo_point",
        "//ccpd/utilities/inlet:inlet_loop_calcs",
    ],
)
