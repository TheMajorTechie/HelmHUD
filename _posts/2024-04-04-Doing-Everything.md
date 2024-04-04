---
title: "Doing Everything"
description: "The post in which Vincent does all the things. Also, this blog post is roughly a week late. Got busy working on things for other classes."
authors: [Vincent]
date: 2024-04-04
---

# All the things
__So.__ Yeah. It's me again. What am I doing here? The answer is yes.

In this blog post, I have gone ahead and implemented what I believe should be a working Bluetooth "central" mode on the Pi Pico W that takes sensor data and forwards it to the OLED display that we are still using. A second Pi Pico is also now in use in order to serve as the sensor side of things.

### What was actually done
Using code modified from the [Micropython examples](https://github.com/micropython/micropython-lib/blob/master/micropython/bluetooth/aioble/aioble/central.py), multiple Python classes were written in order to create a basic Bluetooth Central device. A class object "sensor" exists to instantiate and represent connected Bluetooth sensors. There is not yet a way to properly disconnect peripherals without causing the Pico to crash, but this is intended to be addressed in the future. The main() function on execution during startup attempts to instantiate sensors. If one is present, then it enters an infinite while loop in order to continuously display the sensor data on the display. If one is __not__ present, however, then the text being scrolled will instead be "No Devices Found".

The Sensor class is inteded to be reusable across many different types of sensors, and a single device represents both the connection as well as the "characteristic" of the connection, where data can be collected from. Additional sensor types can be added by adding their characteristic UUIDs to the block of environment variables at the very top of the file.

### Pull the code from Github.
First off, pull the code from the [Github repo](https://github.com/TheMajorTechie/HelmHUD). More specifically, the code in src/HelmHUD and src/HelmHUD_sensors/temperature. 

If you have Thonny installed, go into tools>options and under the "general" tab, uncheck "only allow a single Thonny instance". This will allow you to run two Thonny instances at once across two different Pico Ws.

Now, for one Pico, upload all the code from src/HelmHUD. For the other, upload everything from src/HelmHUD_sensors/temperature.

...That's it. That's the tutorial.

## Acknowledgements
