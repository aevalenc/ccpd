load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "tip_diameter_tests",
    srcs = ["tip_diameter_tests.py"],
    deps = ["//ccpd/stages/inlet:tip_diameter"],
)

py_test(
    name = "inlet_loop_calcs_tests",
    srcs = ["inlet_loop_calcs_tests.py"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor_geometry",
        "//ccpd/data_types:thermo_point",
        "//ccpd/stages/inlet:inlet_loop_calcs",
    ],
)

py_test(
    name = "inlet_utils_tests",
    srcs = ["inlet_utils_tests.py"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:centrifugal_compressor_geometry",
        "//ccpd/data_types:thermo_point",
        "//ccpd/stages/inlet:inlet_utils",
    ],
)
