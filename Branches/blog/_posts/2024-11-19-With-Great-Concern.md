---
title: "With Great Concern"
description: "In which project updates, concerns, and a rant about Bluetooth all come together in one place."
authors: [Vincent]
date: 2024-11-19
---

Haha.

I believe I finally understand why there seems to be a visceral hatred of Bluetooth in developer circles.

And that's because the interface is a miserable pile of [specification papers and capability IDs](https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Assigned_Numbers/out/en/Assigned_Numbers.pdf), in which it's already plenty confusing just to figure out which "capability" is the correct one to utilize. Add onto that the fact that the libraries available for a client/server-style Bluetooth configuration are poor at best and nonexistent at worst, and that nobody within HelmHUD's project group has any familiarity with wireless communication protocols, and you have a recipe for disaster.

In other words, I have wasted over half a year doing nothing but trying and failing repeatedly to establish a working, stable... **Bluetooth UART**.

All I needed to do was transmit some serial data wirelessly back and forth. I'd already long ago changed the plans from a client/server setup to a point-to-point communication layer for the sake of working around the packet size limits imposed by the Pi Pico W's MicroPython Bluetooth library. It *appeared* to be working for a time. Roughly two weeks, in which we as a group finally began the process of integrating our code branches together.

However. During testing, I noticed that after about a minute of operation, the Bluetooth connection seems to just... *disappear*. For lack of a better term, I can best describe it as a "ghost" connection, in which neither microcontroller acknowledges that the connection has been lost, and in fact they appear to continue sending data without any issue. The trouble comes with their respective interrupt handlers--while the *receiving* handlers continue to operate as expected, the *sending* handlers appear to stop functioning as if they've disappeared entirely. Even in testing, when surrounding their function calls with print statements, after a some indeterminate amount of time between 0 and 5 minutes, it *will* cease to print anything to the terminal without so much as an exception being thrown. And because HelmHUD's method of data transmission relies on a custom plaintext request/response protocol, this unexpected loss in connection without any indication is troubling.

Debugging has been a nightmare, with line-by-line stepping through of code being effectively useless from our experience, and MicroPython, which we had received special permission to use explicitly *because* of the fact that the C libraries for Bluetooth were in an even worse state due to how new they were has only come back to bite us in hindsight. Especially given that it runs within an interpreter, which is itself effectively a virtual machine within the microcontroller, there have been a number of times where we have encountered strange behavior raised by the interpreter ourself. One such piece of unexpected behavior is that, even without the use of a "while-true" loop to utilize a polling-based method of data acquisition, it is common for the microcontroller to become unresponsive when attempting to halt code execution and update a file. The only way of resolving this that we know of for now remains "unplug the microcontroller and plug it back in".

As of last week, we finally made the belated emergency decision to give up on Bluetooth. In its current state, the HelmHUD project has devolved into nothing more than a school project involving sending sensor data from one microcontroller to another over a two-wire UART interface. It is a glorified I2C to UART converter that, aside from code handling the sensors itself, now consists of fewer than 100 lines of code as of the writing of this blog. The Bluetooth communication layer that this wired UART interface supercedes was itself nothing more than example Micropython code pulled from the Micropython repositories and modified to replace direct communication of random numbers with our communication handshaking protocol.

To say that I am concerned with how simple our project has become after being pared down so much due to our own inabilities to understand an interface that lay at the heart of the project is understating things.

I worry that, in a couple of weeks, when Demo Day comes around, we'll see the fruits of more competent teams and their projects. I have heard that one team has been working on a virtual-reality centered project, and another on holographic displays--a topic I myself had pitched at the very beginning of the course last Spring Semester before we had even formed groups. 

I would be lying if I said I didn't regret working on this project.

I have been the sole person working on Bluetooth since May, and now I have next to nothing to show for my efforts.

I wish that I could've brought my own ideas for a holographic display project to the team that's now working on one.

I don't want this project to fall apart more than it already has.

For now at least, I'll try to push through. Get *something* out the door at the very least, even if it's practically nothing in comparison to the projects of other groups. At the very least, I'll finish backporting the communication layer from Bluetooth to wired UART. Maybe add the ability to identify what is connected at any given time to allow for a pseudo-hotswap functionality.

And then, I never want to involve myself with this project or Bluetooth ever again.
