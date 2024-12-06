---
title: "Bluetooth Troubles"
description: "In which we agree that trying to program the Pi Pico in C with little prior experience is likely a bad idea."
authors: [Vincent, Carter, Hong, Michael]
date: 2024-02-22
---

# Progress

In terms of progress... we've made no progress. Our main trouble remains getting Bluetooth to work at all--we were able to get the Pi Pico W to at least _connect_ to a Bluetooth host device, but we were unable to perform any kind of debugging at all due to an issue with our CMake configuration files. We are unsure what the issue even is to begin with, as we attempted to reconstruct a custom file based on existing examples.

As such, we plan to make a full migration from programming in C to programming in MicroPython, which should hopefully abstract away enough complexities to make the project as a whole more manageable by the team. We acknowledge that the increased ease of programming will come with the downside of increased memory usage and decreased execution speed due to the interpreted nature of Python, but we do not expect it to be an issue moving forward.