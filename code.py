import board
import time
import pwmio
import adafruit_scd30
from adafruit_motor import servo

i2c = board.STEMMA_I2C()
# i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

# note, we're using a 25kg servo (DS3225), your values may vary
# servo: https://a.co/d/30IFoco
# using an Adafruit QT Py ESP32-S2 board, your pin may vary
servo = servo.Servo(pwmio.PWMOut(board.TX, duty_cycle=0, frequency=50), min_pulse=400, max_pulse=2400)

# adjust these values to match your gauge and servo
SERVO_DIVISOR = 5.55555
ANGLE_MOD = 270

# simple range mapper, like Arduino map() - thanks to todbot  https://github.com/todbot/circuitpython-tricks?tab=readme-ov-file#map-an-input-range-to-an-output-range
def map_range(s, a1, a2, b1, b2):
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def setGaugeToValue(servo, co2=500):
    # keep value between 500 and 1500 as this matches the gauge markings
    co2 = min(max(co2, 500), 1500)
    # map the co2 value to an angle between 0 and 180
    angle = map_range(co2, 500, 1500, 180, 0)

    # angle = round(abs((co2 / SERVO_DIVISOR) - ANGLE_MOD))
    print(f"setting to angle {angle}, co2 value is {co2}")
    servo.angle = angle

# test values to see if we're hitting the markings on gauge correctly
def testValuesToMarkings():
    setGaugeToValue(servo, 500)
    time.sleep(3)
    setGaugeToValue(servo, 750)
    time.sleep(3)
    setGaugeToValue(servo, 1000)
    time.sleep(3)
    setGaugeToValue(servo, 1250)
    time.sleep(3)
    setGaugeToValue(servo, 1500)
    time.sleep(3)

while True:
    # this call is not strictly necessary, but it will help if the sleep time is short (< 2secs) and on first read
    if scd.data_available:
        co2 = scd.CO2
        setGaugeToValue(servo, co2)
        print(f"CO2: {co2} PPM")

    # sleep for 30 seconds
    time.sleep(30)
