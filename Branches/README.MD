# HelmHUD Repository Archive
- main: Despite the name, this is no longer the "main" branch of the repository. The most current code can be found in the WiFi branch, which replaces the entire communication protocol with WiFi rather than Bluetooth or a wired UART.
- blog: Contains all source files used in the maintenance of the project blog.
- GPS: Contains source code for the preliminary implementation of GPS data collection
- Test-I2C-pico-comm: A short-lived branch containing experimental code for cross-microcontroller wired communication using I2C rather than UART or Bluetooth. Immediately superceded by WiFi.
- Wired: Contains the initial implementation of wired sensor hookups to the microcontroller.
- Wired-Refactor: A total refactor of the Wired branch, plus a semi-working Bluetooth communication implementation.
- WiFi: The most up-to-date branch. This branch is a hard-fork of Wired-Refactor, not including libraries, that replaces the Bluetooth-based communication protocol with a WiFi-based one.

## This branch exists purely to allow for quick archiving of the entire Git repository, and is a snapshot of the entire repo and its branches as of December 5th, 2024. No further updates should be made to this branch following the initial commit.