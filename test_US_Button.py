
from time import sleep
from Ultrasonic import Ultrasonic


us = Ultrasonic(18, 19)

while True:
    d = us.distance_cm()
    if d is None:
        print("Out of range")
    else:
        print("Distance: {:.1f} cm".format(d))
    time.sleep(0.5)

