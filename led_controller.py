import RPi.GPIO as GPIO
from config import YELLOW_LED_PIN, GREEN_LED_PIN, RED_LED_PIN

class LEDController:
    def __init__(self):
        self.YELLOW_LED_PIN = YELLOW_LED_PIN
        self.GREEN_LED_PIN = GREEN_LED_PIN
        self.RED_LED_PIN = RED_LED_PIN
        
        GPIO.setup(self.YELLOW_LED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_LED_PIN, GPIO.OUT)
        GPIO.setup(self.RED_LED_PIN, GPIO.OUT)
        
    def turn_on_yellow(self):
        GPIO.output(self.YELLOW_LED_PIN, GPIO.HIGH)
        
    def turn_off_yellow(self):
        GPIO.output(self.YELLOW_LED_PIN, GPIO.LOW)
        
    def turn_on_green(self):
        GPIO.output(self.GREEN_LED_PIN, GPIO.HIGH)
        
    def turn_off_green(self):
        GPIO.output(self.GREEN_LED_PIN, GPIO.LOW)
        
    def turn_on_red(self):
        GPIO.output(self.RED_LED_PIN, GPIO.HIGH)
        
    def turn_off_red(self):
        GPIO.output(self.RED_LED_PIN, GPIO.LOW)
        
    def turn_off_all(self):
        self.turn_off_yellow()
        self.turn_off_green()
        self.turn_off_red()