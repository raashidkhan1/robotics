import sys
import time
from .gpio import GPIO

usleep = lambda x: time.sleep(x / 1000000.0)

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

class GroveUltrasonicRanger(object):
    def __init__(self, pin):
        """A class to fetch distances measured by the ultrasonic ranger.
        
        Code sourced from: https://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/
        """
        self.dio = GPIO(pin)

    def _get_distance(self):
        """Try to read the distance using the US sensor. May return None."""
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)

        self.dio.dir(GPIO.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None

        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None

        distance = ((t2 - t1) * 1000000 / 29 / 2)    # cm

        return distance

    def get_distance(self):
        """Attempts to read the distance from the US sensor until a non-None
        measurement is made. Result is in centimeters."""
        while True:
            dist = self._get_distance()
            if dist:
                return dist
