py_library(
    name = "centrifugal_calcs",
    srcs = ["centrifugal_calcs.py"],
    data = ["//ccpd/fluids:fluids.json"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:inputs",
        "//ccpd/data_types:working_fluid",
        "//ccpd/utilities/inlet:inlet_loop_calcs",
        "//ccpd/utilities/inlet:inlet_utils",
        "//ccpd/utilities/outlet:optimize_mass_flow_rate",
        "//ccpd/utilities/outlet:setup_outlet_stage",
        "//ccpd/utilities/vaneless_diffuser",
    ],
)
