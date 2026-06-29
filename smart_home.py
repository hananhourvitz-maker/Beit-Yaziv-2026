import time
from machine import TouchPad, Pin
from BeamSensor import BeamSensor
from Ultrasonic import Ultrasonic

# 1. Initialize Sensors
beam_sensor = BeamSensor(signal_pin=12)
Distance_Sensor1 = Ultrasonic(18, 19)

# Initialize the capacitive touch sensor on GPIO 32
touch_sensor = TouchPad(Pin(32))
TOUCH_THRESHOLD = 300

# 2. Alarm State Variables (True = Safe / No Intrusion, False = Intrusion)
laser_ok = True
us_ok = True
touch_ok = True

# 3. Intrusion Counters for Each Sensor
laser_break_counter = 0
us_break_counter = 0
touch_break_counter = 0

# 4. Helper Variables to Track State Transitions
prev_laser_ok = True
prev_us_ok = True
prev_touch_ok = True

# Debounce counter for the ultrasonic sensor
us_debounce_counter = 0

print("System initialized. Monitoring Laser, Ultrasonic, and Touch sensors...")

while True:
    
    # --------------------------------------------
    # 1. Ultrasonic Sensor Logic (with Debounce)
    # --------------------------------------------
    d = Distance_Sensor1.distance_cm()
    if d > 2:
        if d < 20:
            if us_debounce_counter < 3:
                us_debounce_counter += 1
        else:
            if us_debounce_counter > 0:
                us_debounce_counter -= 1

        if us_debounce_counter >= 3:
            us_ok = False 
        elif us_debounce_counter == 0:
            us_ok = True  
            
    # --------------------------------------------
    # 2. Laser/Beam Sensor Logic
    # --------------------------------------------
    if beam_sensor.is_beam_hitting():
        laser_ok = True
    else:
        laser_ok = False
        
    # --------------------------------------------
    # 3. Touch Sensor Logic
    # --------------------------------------------
    touch_val = touch_sensor.read()
    
    # If the reading drops below the threshold, a touch is detected
    if touch_val < TOUCH_THRESHOLD:
        touch_ok = False # Touch detected (Intrusion)
    else:
        touch_ok = True  # No touch (Safe)
        
    # --------------------------------------------
    # 4. State Transition and Source Detection
    # --------------------------------------------
    
    # Detect exact moment the LASER beam is broken
    if prev_laser_ok == True and laser_ok == False:
        laser_break_counter += 1
        print("INTRUSION DETECTED! Source: [LASER SENSOR] | Total Laser Breaks:", laser_break_counter)
        
    # Detect exact moment the DISTANCE threshold is crossed
    if prev_us_ok == True and us_ok == False:
        us_break_counter += 1
        print("INTRUSION DETECTED! Source: [DISTANCE SENSOR] | Total Distance Breaks:", us_break_counter)
        
    # Detect exact moment the TOUCH sensor is pressed (Transition from True to False)
    if prev_touch_ok == True and touch_ok == False:
        touch_break_counter += 1
        print("INTRUSION DETECTED! Source: [TOUCH SENSOR] | Total Touch Breaks:", touch_break_counter)
        
    # --------------------------------------------
    # 5. Save Current States for Next Iteration
    # --------------------------------------------
    prev_laser_ok = laser_ok
    prev_us_ok = us_ok
    prev_touch_ok = touch_ok
    
    time.sleep(0.05) # Short delay to balance responsiveness and CPU load