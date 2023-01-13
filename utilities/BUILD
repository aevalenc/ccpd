py_library(
    name = "centrifugal_calcs",
    srcs = ["centrifugal_calcs.py"],
    data = ["//ccpd/fluids:fluids.json"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        ":inlet_loop_calcs",
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:inputs",
        "//ccpd/data_types:working_fluid",
    ],
)

py_library(
    name = "inlet_loop_calcs",
    srcs = ["inlet_loop_calcs.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        ":tip_diameter",
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:inputs",
        "//ccpd/data_types:thermo_point",
        "//ccpd/data_types:working_fluid",
    ],
)

py_library(
    name = "tip_diameter",
    srcs = ["tip_diameter.py"],
    visibility = ["//ccpd:__subpackages__"],
    deps = [
        "//ccpd/data_types:centrifugal_compressor",
        "//ccpd/data_types:inputs",
        "//ccpd/data_types:working_fluid",
        "@python_deps_scipy//:pkg",
    ],
)
