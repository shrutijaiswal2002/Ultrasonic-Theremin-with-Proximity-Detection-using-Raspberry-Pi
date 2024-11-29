from gpiozero import DistanceSensor, TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
import time
import RPi.GPIO as GPIO

# Set up the distance sensor and buzzer
uds = DistanceSensor(trigger=27, echo=17)
buzzer = TonalBuzzer(21, octaves=3)

# Define the threshold distance (in meters, adjust as needed)
threshold_distance = 0.2  # For example, 20 cm

# Function to map the distance to a corresponding tone
def distance_to_tone(distance_value):
    min_tone = buzzer.min_tone.midi
    max_tone = buzzer.max_tone.midi
    tone_range = max_tone - min_tone
    return min_tone + int(tone_range * distance_value)

# Main loop to detect distance and control the buzzer
while True:
    distance_value = uds.distance  # Get the distance reading from the sensor
    if distance_value <= threshold_distance:
        # Otherwise, stop the buzzer
        GPIO.setmode(GPIO.BCM)
        # Define buzzer pin
        buzzer_pin = 21
        # Set pin as output
        GPIO.setup(buzzer_pin, GPIO.OUT)
        # Turn off the buzzer
        GPIO.output(buzzer_pin, GPIO.HIGH) 
        # Optional: Add a delay to ensure the buzzer is fully off
        time.sleep(0.1) 
        # Clean up GPIO
        GPIO.cleanup()
    else:
        # If the object is at or closer than the threshold distance, keep the buzzer on
        # Use the middle C tone (midi=60) as a constant sound
        buzzer.play(Tone(midi=60))  # Constant tone for proximity
    sleep(0.1)  # Delay to avoid too rapid polling
