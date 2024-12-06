---
title: "Meeting Log #1"
description: "Our first(ish) official meeting as a project team! Discussion topics include further talk about viable microcontrollers and the setting of project milestones."
authors: [Vincent, Carter, Hong, Michael]
date: 2024-02-01
---
# Meeting Log #1

Well, here we go! Our first kinda-official meeting! There was a good amount of stuff that we discussed today.

First up, some tentative milestones!

## Milestones
* Pick a microcontroller
* Successfully pair with and read data from a Bluetooth device
* Determine what display technology will be suitable for the project
* **Integration phase 1:** Output the read data from the microcontroller to the chosen display
* Power circuitry design (battery & associated charging/monitoring circuits)
* **Integration phase 2:** Physical product design - lens, packaging, and any other external bits!
* Final optimization (Now that everything's working, shrink things down and make them as responsive as possible!)
* **Stretch goal 1:** App pairing!
* **Stretch goal 2:** Miniaturize the device enough that it can be mounted on the arms of a pair of glasses rather than a helmet

We're not 100% certain that these will be the end-all, be-all milestones to aim for as of yet, but at current we are already progressing towards meeting the goal of milestone 1 in choosing a suitable microcontroller. Though it was earlier stated that we were interested in the ESP32 line of microcontrollers, we are still heavily considering the Raspberry Pi Pico W for the reason of its ease-of-use, given its support for drag-and-drop firmware flashing.

As for the display, we are thinking of, at least for now, using a basic I2C character display. Ideally, moving forward toward the final design, we can continue using the I2C interface to avoid the need to rewrite any display-driving code that we may produce. We plan for the final product to instead use a projection-based display rather than an LCD, but if complexity becomes too great of a concern then we may simply stay with using an LCD or OLED display.

Parts acquisition should be relatively simple, as the project itself mostly deals in small components such as microcontrollers that are in good supply. Beyond this, 3D-printed parts and basic helmets acquired via retail chains such as Walmart are likely to be sufficient for the prototyping phase, and potentially even the final product.

And of course, being that we're at the very beginning of a project none of us have much experience in, there is indeed some risk involved:
* Not all of us have much experience in embedded systems design, so working with a microcontroller will be a learning curve
* Safety will be a primary concern regardless of what display technology is used due to the proximity of the device to an end user's face
   * If we continue to use an LCD or OLED panel through to the final product, then it must be kept at a safe distance from a user's eyes, and ideally have safeguards in place to address the scenario where a user may fall head-first. Without such safeguards, it is easy for pieces of plastic or glass to injure their face--or worse yet, their eyes.
   * If we switch to using a projection-based system, the above issue will become less of a concern due to the projection being shone onto the visor of a compatible helmet, but a maximum brightness setting will need to be set to reduce eye strain. This also goes for OLED displays.
   * Depending on the mounting location, the device may need to be padded either to further protect the user's head from exposed wires and PCBs or to protect the device itself from physical damage. Potentially both.
      * With added padding, would heat dissipation become an issue? Battery safety will also be a large concern given the dangers of damaged battery cells... right next to a user's head.
* Because we will be working with Bluetooth communication, user privacy may be a concern. This could potentially be addressed by introducing some sequence of hardware-based pairing involving button-press combinations to make up for the lack of a keyboard in pairing devices together.

And that's about it for now!
