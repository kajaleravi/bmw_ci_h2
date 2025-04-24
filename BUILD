# BUILD
load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")

py_binary(
    name = "main",
    srcs = ["main.py"],
    deps = [
        ":communication_channel",
        "@bmw_pip_deps//pyyaml",  # Updated from @pip_deps
    ],
    data = ["logging_config.yaml"],
)

py_library(
    name = "message_handler",
    srcs = ["message_handler.py"],
    deps = ["@bmw_pip_deps//pyyaml"],  # Updated from @pip_deps
    data = ["logging_config.yaml"],
)

py_library(
    name = "communication_channel",
    srcs = ["communication_channel.py"],
    deps = [
        ":message_handler",
        "@bmw_pip_deps//pyyaml",  # Updated from @pip_deps
    ],
    data = ["logging_config.yaml"],
)

py_test(
    name = "test_communication",
    srcs = ["tests/test_communication.py"],
    deps = [
        ":communication_channel",
        ":message_handler",
        "@bmw_pip_deps//pyyaml",  # Updated from @pip_deps
    ],
)