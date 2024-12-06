---
title: "Last Minute Bugs"
description: "Or, 'what do you mean, reading sensor values silently screws up the Bluetooth connection until the Pico stops sending data?!"
authors: [Vincent]
date: 2024-10-24
---

Hey, it's ya boi. Tired Bluetooth man.

So. _Apparently_, reading values over I2C from a handful of environment sensors on a separate thread from the one running the Bluetooth code causes said Bluetooth code to, for whatever reason, randomly crash and stop receiving data. The code that does this reading out of values is incredibly simple, being a function that calls a collection of helper functions one after another to read and process the data in a way where the output is a single floating-point value. The variables that are used are only instantiated once (supposedly), and are modified on every iteration of the loop rather than being recreated.

But for whatever reason, when this second thread to read out data is enabled, the Bluetooth side of things will arbitrarily stop reading values after a random amount of time. Sometimes, it's about half a minute. Other times, it may be 2, even 3 minutes.

I'm not entirely sure what is happening or why it's happening, but I do not look forward to the debugging.

# Slightly more positive news
The rest of the team has been making good progress. Michael has completed a number of physical prototypes for the final product's enclosure, Carter is just about finished with the GPS code, and Hong is working together with Michael on the compass code. I am the one largely responsible for Bluetooth, so I hope that I am able to figure out what is going wrong in time for everyone to bring their separate parts together.
