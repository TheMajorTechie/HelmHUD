copy ${env:PICO_SDK_PATH}\external\pico_sdk_import.cmake .
copy ${env:PICO_EXAMPLES_PATH}\.vscode . -recurse

$CMakeLists = "cmake_minimum_required(VERSION 3.13)

# initialize the SDK based on PICO_SDK_PATH
# note: this must happen before project()
include(pico_sdk_import.cmake)

project(my_project)

# initialize the Raspberry Pi Pico SDK
pico_sdk_init()

# rest of your project"

echo $CMakeLists > CMakeLists.txt