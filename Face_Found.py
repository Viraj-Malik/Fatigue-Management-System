#!/usr/bin/env python3
from gpiozero import LED
import time
import sys

# GPIO setup - using GPIO 17 (BCM numbering)
LED_PIN = 17

try:
    # Turn on the LED
    led = LED(LED_PIN, active_high=True, initial_value=False)
    led.on()
    # delay
    time.sleep(0.5)
    
    # LED Close
    led.close()
        
except Exception as e:
    print(f"Error in led_on.py: {str(e)}", file=sys.stderr)
    sys.exit(1)
