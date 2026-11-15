# Import the time module to allow the program to pause between actions
import time

# Import the MotorDriver class from the PCA9685 library to control the motor controller board
from PCA9685 import MotorDriver

# Create an instance of the MotorDriver to interact with the hardware
m = MotorDriver()

# Helper to set motor direction + speed
def set_motor(motor, direction, speed):
    # Find the starting index of the specified motor (e.g., 'MA') in the MotorPin list
    mPin = m.MotorPin.index(motor)
    # Find the starting index of the specified direction ('forward' or 'backward') in the MotorDir list
    mDir = m.MotorDir.index(direction)
    
    # Set the motor's speed using PWM (Pulse Width Modulation) on the first associated pin
    m.pwm.setServoPulse(m.MotorPin[mPin+1], speed)
    # Set the high/low logic level on the second pin to control rotation direction
    m.pwm.setLevel(m.MotorPin[mPin+2], m.MotorDir[mDir+1])
    # Set the high/low logic level on the third pin to complete the direction configuration
    m.pwm.setLevel(m.MotorPin[mPin+3], m.MotorDir[mDir+2])

# Run all motors
def run_all(direction, speed):
    # Loop through each of the four motor identifiers
    for motor in ['MA', 'MB', 'MC', 'MD']:
        # Apply the chosen direction and speed to the current motor
        set_motor(motor, direction, speed)

# Stop all motors
def stop_all():
    # Loop through each of the four motor identifiers
    for motor in ['MA', 'MB', 'MC', 'MD']:
        # Find the starting index of the current motor in the MotorPin list
        mPin = m.MotorPin.index(motor)
        # Set the PWM speed pulse to 0 to stop the motor
        m.pwm.setServoPulse(m.MotorPin[mPin+1], 0)

# ---- Main sequence ----

# Forward
# Run all four motors forward at 100% speed
run_all('forward', 100)
# Keep the motors running forward for 2 seconds
time.sleep(2)

# Backward
# Run all four motors backward at 100% speed
run_all('backward', 100)
# Keep the motors running backward for 2 seconds
time.sleep(2)

# Stop
# Turn off all motors to end the sequence
stop_all()
