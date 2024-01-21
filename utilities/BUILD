load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "centrifugal_calcs",
    srcs = ["centrifugal_calcs.py"],
    data = ["//ccpd/fluids:fluids.json"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:inputs",
        "//ccpd/data_types:working_fluid",
        "//ccpd/stages/diffuser",
        "//ccpd/stages/inlet:inlet_loop_calcs",
        "//ccpd/stages/inlet:inlet_utils",
        "//ccpd/stages/outlet:optimize_mass_flow_rate",
        "//ccpd/stages/outlet:setup_outlet_stage",
        "//ccpd/stages/vaneless_diffuser",
    ],
)
