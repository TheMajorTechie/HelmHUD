#include <stdio.h>
#include "pico/stdlib.h"
#include <string.h>
#include "pico/cyw43_arch.h"

int main() {
    stdio_init_all();
    if (cyw43_arch_init()) {
        printf("Wi-Fi init failed");
        return -1;
    }
    while(true) {
        printf("\n\nHello, world! This is a very slightly custom project! Please answer the next question:\n\n");
        
        sleep_ms(5000);

        char decision[1];
        printf("Turn on LED? Y/N\n");

        scanf("%1s", &decision);                         //text gets buffered over the serial terminal
        if(!strcmp(decision, "Y")) {
            printf("Turning LED ON!\n");
            printf("You answered: ");
            printf(decision);
            printf("\n");
            cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
        }
        else {
            printf("Turning LED OFF!\n");
            printf("You answered: ");
            printf(decision);
            printf("\n");
            cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
        }
    }
}