---
title: "SSD1306 Library Search and Bluetooth Examples"
description: "Because none of us understand enough in the way of embedded systems to know how to write our own libraries. Also the Bluetooth examples are stored in an unexpected place."
authors: [Vincent, Carter, Hong, Michael]
date: 2024-02-08
---

# The SSD1306 Library Search
Here's another project update! Today, we spent much of our time getting everyone in the group up to speed. As of today, everybody now has the Raspberry Pi Pico SDK installed in their systems, and have gone through the (updated) tutorial from the previous blog post.

We have also begun working with the SSD1306 OLED display. There's no guarantee that it is the final display that we intend to use, but we decided that this would be our "starter" display to familiarize ourselves with the I2C interface, which is what we intend to use going forward for all display technologies within this project.

However, we ran into a minor roadblock in that the SSD1306 did not, at least upon first inspection, appear to have any Pi Pico-compatible libraries. Instead, it appeared that the display only had libraries available for the Arduino IDE and MicroPython. As we intend to code the project in C for code density and performance purposes, and the use of Arduino-based resources is prohibited for this project, we found ourselves at an impasse. We worried that we would need to either find an alternative display, or learn on-the-fly how to write a library from scratch for a display panel that we very likely won't even use in the final version of HelmHUD.

Thankfully, however, we have found the following resources: [Mr Addict & jfoucher's Pi Pico SSD1306 C Library](https://github.com/MR-Addict/Pi-Pico-SSD1306-C-Library), and [a datasheet for the SSD1306 itself](https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf).

For now, we plan on moving forward with using the SSD1306. We will likely start off with using the existing pre-made library, and maybe in the future move on to build a "wrapper" library that we can use as a sort of display driver so that we do not have to rewrite large amounts of display-centric code with every change we make to the display panel or type that we use. Hopefully, with the four of us together, we may find a way to pull this off without sinking too much time into the task.

# Bluetooth examples in... the SDK's libraries folder?
An odd discovery that we came across was that most of the RPi Pico W's examples for Bluetooth appear to be located in the libraries folder rather than the examples folder. We thought at first that the examples simply hadn't been written yet given the relatively recent introduction of the Pi Pico W, but upon further searching we discovered that the files had instead for whatever reason been moved out of their respective examples folders and instead dumped en masse into the libraries folder. More specifically, it was found to be located in the folder ``\pico-sdk\lib\btstack\example``. We are glad for now that there are any examples at all that we were able to find.
