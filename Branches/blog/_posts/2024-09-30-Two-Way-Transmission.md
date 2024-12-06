---
title: "Two-Way Transmission"
description: "Apparently, it's a known issue with the MicroPython Bluetooth libraries that devices cannot receive more than 20 bytes at a time."
authors: [Vincent]
date: 2024-09-30
---

# Current Progress
We've got Bluetooth finally working! Kind of. Mostly. We're able to send data from the Pico that reads from the sensors, but the "receiving" Pico that's meant to display that data on an OLED display is only able to receive up to 20 bytes in a single transmission. We were not aware of this issue going into this project, but being this late into development the only thing we can do is to work around the issue.

## Proposed solution: Handshake-Based Polling
Originally, we were planning on implementing a handshake layer on top of the Bluetooth UART protocol as a layer of security. However, due to the above issues, we are now attempting to implement this stretch goal as part of the core feature set of HelmHUD. In this way, the sensor and receiver Picos can exchange smaller messages that fit within the 20-byte limit rather than the sensor sending all of its data at once. The process of exchanging data is planned to follow the following steps in order:

- Receiver end ("central") Pico, upon connection, sends a singular message request for an identifier on the sender end ("sensor") Pico.
- Sensor Pico transmits the corresponding identifier and awaits for either a response or a disconnection.
- Central Pico can either proceed directly with the connection, or prompt the end-user on whether or not to connect to the Sensor Pico. At the user's request, this connection can be declined.
- Central Pico requests a list of present sensors
- Sensor Pico returns that list
- Once this initial connection "handshake" is completed, the two devices enter a loop until one or the other is powered off or otherwise disconnected:
  - Central Pico iterates through the list of available sensors that the Sensor Pico has, requesting their values one by one. It waits for a response after each request, but will "time out" and request the next sensor after some set amount of time. At the very end, it may request diagnostic information such as the battery level of the Sensor Pico.
  - Sensor Pico sends the corresponding values after each request is sent.
