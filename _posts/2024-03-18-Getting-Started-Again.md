---
title: "Getting Started (again)"
description: "After deciding to make the switch from C/C++ to MicroPython, I'm here once again to make a writeup on getting things set up and ready. The example code here is more or less the beginnings of the full project itself."
authors: [Vincent]
date: 2024-03-18
---

# The Beginning
Right off the bat, [download the UF2 file for the Pico W here](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html). This is a UF2 file and as such is precompiled. Drop it on the Pico W while it's in programming mode.

Next, install [Thonny](https://thonny.org/). This is the IDE that is officially mentioned by the Raspberry Pi Foundation. For this tutorial, I will be once again displaying to the SSD1306 OLED display over I2C using [this](https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html) guide off the micropython docs, but the library used is an updated version taken from [https://randomnerdtutorials.com/micropython-ssd1306-oled-scroll-shapes-esp32-esp8266/](RandomNerdTutorials). It is included in our GitHub repo.

After that, pull the code from our [GitHub page](https://github.com/TheMajorTechie/HelmHUD/tree/main). You'll want to use the code in folder "test_3".

Open all of the files in that folder in Thonny. Then, save all of them to the Pi Pico. If this is not possible, go to Run->Configure Interpreter in Thonny and check to see if your Pico is detected or not. Also take the time to ensure that the interpreter is set to MicroPython (Raspberry Pi Pico). You should see something along the lines of "Board CDC @ (some serial port)" if your board is detected properly.

If not, Thonny has a convenient little "Install or update MicroPython" link in the bottom right that will automatically reinstall MicroPython on your Pico so long as it's in programming mode.

And... that's it! Thankfully, setup in MicroPython is far, _far_ simpler than it is in C. The next blog post will likely be focusing on actual development, building off of the example code I have written for this post.

Below are some acknowledgements of the tutorials I used to put the example code together. I'm a little rusty on my Python having not used it in high school, but these were able to get me up to speed with MicroPython on the Pico.

## Acknowledgements
https://www.raspberrypi.com/news/getting-to-grips-with-bluetooth-on-pico-w/
https://www.freecodecamp.org/news/python-global-variables-examples/
https://randomnerdtutorials.com/micropython-ssd1306-oled-scroll-shapes-esp32-esp8266/
https://electrocredible.com/raspberry-pi-pico-temperature-sensor-tutorial/
