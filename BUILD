package(default_visibility = ["//visibility:public"])

py_binary(
    name = "main",
    srcs = ["main.py"],
    data = [
        "design_parameters.json",
        "inputs.json",
    ],
    deps = ["//ccpd/utilities:centrifugal_calcs"],
)
