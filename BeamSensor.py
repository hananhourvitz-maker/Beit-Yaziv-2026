from machine import Pin

class BeamSensor:
    def __init__(self, signal_pin):
        """
        Constructor for the beam/encoder sensor.
        Sets the pin as an input with an internal pull-up resistor for stability.
        """
        self.sensor_pin = Pin(signal_pin, Pin.IN, Pin.PULL_UP)
        
    def is_beam_hitting(self):
        """
        Returns True if the beam is hitting the receiver (unblocked).
        Returns False if the beam is blocked.
        Note: Standard slot sensors output 0 when unblocked and 1 when blocked.
        """
        if self.sensor_pin.value() == 0:
            return True
        else:
            return False