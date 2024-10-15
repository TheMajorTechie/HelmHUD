---
title: "Communication Implementation"
description: "What is HelmHUD? A miserable pile of workarounds!"
authors: [Vincent]
date: 2024-10-15
---

Alright. *So.*

HelmHUD (finally) has a basic two-way communication link established between a "sender" and "receiver" Pico. Both Picos are able to send each other data in the form of data request commands (receiver Pico sending to sender) or raw data readouts (sender Pico sending to receiver). It's very crude, and without the ability to use switch-case statements due to Micropython not supporting them, it'll likely end up turning into some very nasty spaghetti code if-else chains. 

But it works.

# What next?
Now that we can not only successfully, but somewhat *properly* send data between Picos using what ultimately after multiple months of work and rewriting turned out to be at best a slightly-modified take on the existing Micropython Bluetooth UART code, getting the project as a whole to a *functional* state is what comes next.

In other words, it's time to begin integrating everything back into a singular implementation.

I myself have been working on a branch called "Wired-Refactor" for the past several months. But after some code cleanup it'll be time to merge the branch back into main at last.

At the top of my mind, I believe the next step to work on towards full integration would be ideally to make the "sender" side of the project multithreaded (again). Potentially even the "receiver" side as well. This would allow for the sensors and display to continuously update uninterrupted, with the actual bluetooth code being run on independent threads in both cases. We'll see how that goes, I suppose.
