---
title: "Getting started with the Raspberry Pi Pico W"
description: "Hoo boy. Time to dip my toes into the world of Pico!"
authors: [Vincent]
date: 2024-02-03
---

Alrighty now. This post is partly for the purpose of logging, and partly for the purpose of "how the heck do I do this?". Because I've never worked with a Pi Pico before.

Anyway, I'm gonna keep this concise and go with a bullet-pointed list of steps to get things up and running on Windows:

# Getting started with blinking an LED on the Pico W

* Download the Pi Pico SDK installer from here: https://www.raspberrypi.com/news/raspberry-pi-pico-windows-installer/
* Once it's installed, because we're working with the Pico W, you'll need to go into the CMakeLists.txt file and add "set(PICO_BOARD pico_w)" (without quotes) into the file, preferably right beneath the other two "set" statements. 
   * Not doing this will make VS Code complain and refuse to compile!
* Try compiling and running the "blink" example for the Pico W. Make sure you're not using the regular "blink" for the Pico, as that uses GPIO pins from the RP2040 chip! The built-in LED on the Pico W uses a GPIO pin on the wifi/bluetooth chip rather than directly from the RP2040 itself.
* Go into the CMAKE tab on the left and configure the kit to use (Pico ARM GCC), and set "build", "debug", and "launch" to "picow_blink"
* Go into the Project Outline below that and select "blink" from the directory tree. Right click and select "build". Assuming you left everything at default values when installing the SDK package, you should find your compiled .uf2 file in %userdir%\Documents\Pico-v1.5.1\pico-examples\build\pico_w\wifi\blink
   * Drag and drop that UF2 file onto the Pico! Hold down the Bootsel button as you plug it into USB and it'll show up as a flash drive. Once the UF2 file is uploaded, it will automatically reboot itself and start running.

# Making a new project from scratch

The SDK includes the following text in its readme:

## Creating a new project

The commands below are for PowerShell, and will need to be adjusted
slightly if you're using Command Prompt instead.

1.  Copy pico_sdk_import.cmake from the SDK into your project directory:

    ``` powershell
    copy ${env:PICO_SDK_PATH}\external\pico_sdk_import.cmake .
    ```

2.  Copy VS Code configuration from the SDK examples into your project
    directory:

    ``` powershell
    copy ${env:PICO_EXAMPLES_PATH}\.vscode . -recurse
    ```

3.  Setup a `CMakeLists.txt` like:

    ``` cmake
    cmake_minimum_required(VERSION 3.13)

    # initialize the SDK based on PICO_SDK_PATH
    # note: this must happen before project()
    include(pico_sdk_import.cmake)

    project(my_project)

    # initialize the Raspberry Pi Pico SDK
    pico_sdk_init()

    # rest of your project
    ```

4.  Write your code (see
    [pico-examples](https://github.com/raspberrypi/pico-examples) or the
    [Raspberry Pi Pico C/C++ SDK](https://rptl.io/pico-c-sdk)
    documentation for more information)

    About the simplest you can do is a single source file (e.g.
    hello_world.c)

    ``` c
    #include <stdio.h>
    #include "pico/stdlib.h"

    int main() {
        setup_default_uart();
        printf("Hello, world!\n");
        return 0;
    }
    ```

    And add the following to your `CMakeLists.txt`:

    ``` cmake
    add_executable(hello_world
        hello_world.c
    )

    # Add pico_stdlib library which aggregates commonly used features
    target_link_libraries(hello_world pico_stdlib)

    # create map/bin/hex/uf2 file in addition to ELF.
    pico_add_extra_outputs(hello_world)
    ```

    Note this example uses the default UART for *stdout*; if you want to
    use the default USB see the
    [hello-usb](https://github.com/raspberrypi/pico-examples/tree/master/hello_world/usb)
    example.

5.  Launch VS Code from the *Pico - Visual Studio Code* shortcut in the
    Start Menu, and then open your new project folder.

6.  Configure the project by running the *CMake: Configure* command from
    VS Code's command palette.

7.  Build and debug the project as described in previous sections.

# Moving forward and closing notes

I haven't actually followed the steps to create a new project yet as of writing, but if there is anything else that comes up unexpectedly that needs to be written down, they will be listed below. 

* You'll need to add the two following environment variables if they aren't already present in order to use the above instructions:
   * ``PICO_SDK_PATH`` = ``C:\Program Files\Raspberry Pi\Pico SDK v1.5.1\pico-sdk``
   * ``PICO_EXAMPLES_PATH`` = ``%userprofile%\Documents\Pico-v1.5.1\pico-examples``
