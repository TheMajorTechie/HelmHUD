---
title: "Refactoring and I2C Strangeness"
description: "Why do environmental sensors that sit on one I2C channel affect the functionality of an I2C OLED display on a completely independent second I2C channel???"
authors: [Vincent]
date: 2024-08-02
---

Woo, it's been a hot moment since I've written an update!

So.

# What's happened in the past month
In the past month, the HelmHUD crew's finally found a consistent meeting schedule to work with, and as a result, we've been making some actual progress!

To begin, we've started work on expanding sensor functionality, adding both heart-rate monitoring and environmental sensors to the project. The latter of these is centered around a WaveShare development board that places a number of useful sensors on a single PCB, while the former is its own independent board.

And it genuinely looked like we were making some good progress, too.

Too bad we've run into one of the strangest bugs we've seen yet.

So, to begin, we've written a "wrapper" of sorts that takes all the environmental sensors, save for the heartbeat sensor, and compiles them into a handful of functions that can be called to return simple integer values. Independently, these work perfectly fine. It's now possible to read out all the values from every sensor at once via the serial console.

But, the moment you add the I2C display back into the mix, everything just... *breaks*. For reasons we've yet to discover. It seems that our BME sensor, which measures atmospheric pressure and humidity, seems to for whatever reason conflict so badly with the I2C display that it's able to impact the display's functionality despite being on a wholly separate and independent I2C channel from it. I don't know how or why this is happening, but if it comes to it, we may need to temporarily drop the functionality from the project.

# So, what next?
We're currently diagnosing the issue (or in other words, banging our heads trying to figure out why we can only have either the display or the BME sensor working, but never both). I plan on rewriting the environmental sensors wrapper from scratch a second time to try and figure out exactly what it is that might be causing these strange issues, and if there's a way to fix it. If not, then it may be necessary for us to return to a two-Pico setup where the first device acts purely as a sensor data collator that streams the recorded data over Bluetooth to a second Pico, which then handles the display and user inputs. This option to me might be the best one to use moving forward, as it'd allow the project to address the conflicting I2C device issue by re-adding functionality that was previously lost due to being a time sink. Now that we're able to collect useful data from all our sensors so long as we don't have the I2C display attached, we have the opportunity to start work once more on our original wireless functionality that we envisioned.
