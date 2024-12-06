---
title: "Wait what? Wifi?"
description: "We were stuck in the pit for so long that we didn't realize the sky was above us."
authors: [Vincent]
date: 2024-11-26
---

So.

I suppose that while I was working mostly burnt-out following the previous blogs' Bluetooth escapades on purely wired communication, Michael realized that using a _different_ wireless protocol--that is, wifi--is apparently far, _far_ simpler to implement than Bluetooth. I was afraid to even consider implementing Wifi, as it would mean a switch to the _third_ physical communication interface that this project has had... just a little over one week away from demo day.

If it works then it works, and so be it. Michael says that the main issue that he has been having with wifi communication is that it only appears to connect to one device at a time in a configuration where the "server" is the formerly "receiving" Pico, and the "sending" Picos from the Bluetooth/UART era are instead constantly sending data to the server. I'll try to help out where I can if possible, but I'm not feeling very confident about this project anymore after two development resets, and because Michael's wifi communication layer uses a communication protocol that he implemented that doesn't appear to require feedback being sent to the sensor Picos, this means that yet again, all of my efforts have been in vain. I'm tired of this.
