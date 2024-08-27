---
title: "Bluetooth Annoyances (again)"
description: "I forgot how big of a pain Bluetooth is to work with."
authors: [Vincent]
date: 2024-08-27
---

# Current Progress
As the project currently stands, HelmHUD is now capable of transmitting sensor data over Bluetooth to a serial terminal app running on an Android device. Michael is working on defining a physical form factor for the project without the need for any custom PCBs, Carter is attempting to bring GPS functionality to full working order, and Hong is working on display hookups.

Bluetooth in its current implementation is based on the "Bluetooth UART" example code provided in the MicroPython repository. However, this code does not appear to document a way to connect two Pi Picos to each other over Bluetooth. As such, some minor revision will be needed to migrate the current implementation to being based instead on the Bluetooth-Central and and Bluetooth-Peripheral example code.
