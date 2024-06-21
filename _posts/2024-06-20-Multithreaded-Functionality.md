---
title: "Multithreaded Functionality"
description: "Read the title again."
authors: [Vincent]
date: 2024-06-20
---

# Where have the updates been?
To put it simply, life got in the way. Competitions, a long-planned vacation followed by helping out family and an emergency hospitalization. All over the course of two months.

And that takes us to now.

To begin, a brief apology for the lateness.

And to begin the *next* part, did you know that the Raspberry Pi Pico has *two* cores?

# Dual cores and (a lack of a) transparent OLED
Originally upon returning to this project, I intended to start things off by trying to interface with the *SSD1309*, a different OLED display than the SSD1306 that we have currently been using. Unlike the '1306, the '1309 is a larger, transparent panel.

And in the chaos of the time between the beginning of May and now, I somehow managed to lose the cable before I'd even tested the thing out for the first time.

![A quick-and-dirty cable hackjob.](../../../assets/images/20240620_155139.jpg)

Suffice to say, it did not work. Not because of a flaw in the wiring, but because I'd unintentionally flipped the polarity of VCC and GND when plugging the wires into the breadboard. Unfortunately, all it does now is get hot and not work. A replacement has already been ordered in the meantime.

***So***, instead, I've started work on implementing multithreaded functionality to the project! The RPi Pico as mentioned before has two independent hardware cores, each one capable of running one thread (unless you're running something that can manage multiple threads per core).

I learnt the hard way that if the second core doesn't fully exit from running, then the Pico really, *really* does not like to behave. I'd thought that both Thonny and VSCode had both abruptly broken on me, but I realized it appeared that even when I halted execution using the "stop" button in either IDE, the second core seemed to continue running. At the time, it had its own while(True) loop that it ran with no way to handle termination. As an experiment, I tried disconnecting the SSD1306 OLED display panel, which caused it to crash before it could enter the loop. Sure enough, suddenly both IDEs became responsive again.

As such, the code that I've recently pushed to the HelmHUD repo is a version that has a (slightly) more graceful shutdown of the second thread. It still acts up however, and for now I would still recommend disconnecting the OLED display as a stopgap measure to prevent the IDEs from freezing up, but at the very least I am receiving visual confirmation in the terminal that the second thread is being stopped and restarted under the control of the main thread.

![IT LIIIIIIIIIIIVES.](../../../assets/20240620_200015.jpg)

It only took two hours to realize that. *Only.*

In any case, this I feel is finally some decent progress. Introducing a multithreaded model should hopefully help the project operate more seamlessly, as I intend for the second thread to take over "backend" operations such as scanning for, connecting to, and disconnecting from Bluetooth devices, while the first thread manages user I/O and determines when to "spin up" the second thread and when to halt it.