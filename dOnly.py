import time
from PCA9685 import MotorDriver

m = MotorDriver()

# Helper to set motor direction + speed
def set_motor(motor, direction, speed):
    mPin = m.MotorPin.index(motor)
    mDir = m.MotorDir.index(direction)

    m.pwm.setServoPulse(m.MotorPin[mPin+1], speed)
    m.pwm.setLevel(m.MotorPin[mPin+2], m.MotorDir[mDir+1])
    m.pwm.setLevel(m.MotorPin[mPin+3], m.MotorDir[mDir+2])

# Run all motors
def run_all(direction, speed):
    for motor in ['MD']:
        set_motor(motor, direction, speed)

# Stop all motors
def stop_all():
    for motor in ['MD']:
        mPin = m.MotorPin.index(motor)
        m.pwm.setServoPulse(m.MotorPin[mPin+1], 0)

# ---- Main sequence ----

# Forward
run_all('forward', 100)
time.sleep(2)

# Backward
run_all('backward', 100)
time.sleep(2)

# Stop
stop_all()

