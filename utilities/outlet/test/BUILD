load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "optimize_mass_flow_tests",
    srcs = ["optimize_mass_flow_tests.py"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:centrifugal_compressor_geometry",
        "//ccpd/data_types:test_utils",
        "//ccpd/data_types:thermo_point",
        "//ccpd/utilities/outlet:optimize_mass_flow_rate",
        "//ccpd/utilities/outlet:setup_outlet_stage",
    ],
)
