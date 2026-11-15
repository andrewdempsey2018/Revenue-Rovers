# Import time for short hardware delays during setup and motor run durations
import time
# Import Pin and I2C classes from MicroPython's machine module for hardware communication
from machine import Pin, I2C
# Import math for rounding calculations when setting the PWM frequency
import math

class PCA9685:
    # Registers/etc.
    # Define internal hardware register addresses for the PCA9685 PWM controller chip
    __SUBADR1            = 0x02  # I2C-bus subaddress 1
    __SUBADR2            = 0x03  # I2C-bus subaddress 2
    __SUBADR3            = 0x04  # I2C-bus subaddress 3
    __MODE1              = 0x00  # Mode register 1 (controls sleep, restart, and clock settings)
    __PRESCALE           = 0xFE  # Prescaler register for setting the PWM output frequency
    __LED0_ON_L          = 0x06  # Channel 0 ON time low byte
    __LED0_ON_H          = 0x07  # Channel 0 ON time high byte
    __LED0_OFF_L         = 0x08  # Channel 0 OFF time low byte
    __LED0_OFF_H         = 0x09  # Channel 0 OFF time high byte
    __ALLLED_ON_L        = 0xFA  # Load all channels ON time low byte
    __ALLLED_ON_H        = 0xFB  # Load all channels ON time high byte
    __ALLLED_OFF_L       = 0xFC  # Load all channels OFF time low byte
    __ALLLED_OFF_H       = 0xFD  # Load all channels OFF time high byte

    def __init__(self, address=0x40, debug=False):
        # Initialize I2C bus 0 on GPIO 21 (SCL) and GPIO 20 (SDA) at 100 kHz
        self.i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=100000)
        # Store the I2C device address (default is 0x40)
        self.address = address
        # Store debug flag to enable or disable console logging
        self.debug = debug
        if (self.debug):
            print("Reseting PCA9685") 
        # Write 0x00 to MODE1 register to wake the chip up and set normal mode
        self.write(self.__MODE1, 0x00)
	
    def write(self, cmd, value):
        "Writes an 8-bit value to the specified register/address"
        # Send a single byte to a specific memory register over I2C
        self.i2c.writeto_mem(int(self.address), int(cmd), bytes([int(value)]))
        if (self.debug):
            print("I2C: Write 0x%02X to register 0x%02X" % (value, cmd))
	  
    def read(self, reg):
        "Read an unsigned byte from the I2C device"
        # Read 1 byte from the target register over I2C
        rdate = self.i2c.readfrom_mem(int(self.address), int(reg), 1)
        if (self.debug):
            print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, int(reg), rdate[0]))
        # Return the integer value of the received byte
        return rdate[0]
	
    def setPWMFreq(self, freq):
        "Sets the PWM frequency"
        # Calculate the prescale value using the chip's internal 25 MHz oscillator and 12-bit (4096) resolution
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        if (self.debug):
            print("Setting PWM frequency to %d Hz" % freq)
            print("Estimated pre-scale: %d" % prescaleval)
        # Round the prescale value to the nearest whole number
        prescale = math.floor(prescaleval + 0.5)
        if (self.debug):
            print("Final pre-scale: %d" % prescale)

        # Read the current MODE1 register state
        oldmode = self.read(self.__MODE1)
        #print("oldmode = 0x%02X" %oldmode)
        # Set the sleep bit (bit 4) while keeping existing settings; prescale can only be changed while asleep
        newmode = (oldmode & 0x7F) | 0x10        # sleep
        self.write(self.__MODE1, newmode)        # go to sleep
        # Write the calculated frequency prescale value
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        # Restore the previous mode to wake the oscillator back up
        self.write(self.__MODE1, oldmode)
        # Wait 5 milliseconds for the oscillator to stabilize
        time.sleep(0.005)
        # Set the restart bit (bit 7) to resume PWM output
        self.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        "Sets a single PWM channel"
        # Each channel uses 4 consecutive registers starting at __LED0_ON_L
        # Split the 12-bit 'on' and 'off' tick counts (0–4095) into low and high bytes
        self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
        self.write(self.__LED0_ON_H+4*channel, on >> 8)
        self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
        self.write(self.__LED0_OFF_H+4*channel, off >> 8)
        if (self.debug):
            print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel,on,off))
	  
    def setServoPulse(self, channel, pulse):
        # Convert a percentage speed/pulse (0–100) into a 12-bit PWM duty cycle value (0–4095)
        pulse = pulse * (4095 / 100)
        # Start the pulse at tick 0 and turn it off at the calculated tick count
        self.setPWM(channel, 0, int(pulse))
    
    def setLevel(self, channel, value):
        # Use a PWM channel as a standard digital HIGH (1) or LOW (0) output pin
        if (value == 1):
              # Full 100% duty cycle (always HIGH)
              self.setPWM(channel, 0, 4095)
        else:
              # 0% duty cycle (always LOW)
              self.setPWM(channel, 0, 0)

class MotorDriver():
    def __init__(self, debug=False):
        # Store debug flag
        self.debug = debug
        # Create an instance of the PCA9685 PWM controller
        self.pwm = PCA9685()
        # Set the PWM frequency to 50 Hz
        self.pwm.setPWMFreq(50)       
        # Map each motor name to its 3 PCA9685 channels: [Name, PWM_Speed_Pin, Dir_Pin_A, Dir_Pin_B]
        self.MotorPin = ['MA', 0,1,2, 'MB',3,4,5, 'MC',6,7,8, 'MD',9,10,11]
        # Map direction names to H-bridge logic levels: [Direction, Pin_A_State, Pin_B_State]
        self.MotorDir = ['forward', 0,1, 'backward',1,0]

    def MotorRun(self, motor, mdir, speed, runtime):
        # Ignore commands if speed exceeds 100%
        if speed > 100:
            return
        
        # Look up the starting index for the chosen motor and direction
        mPin = self.MotorPin.index(motor)
        mDir = self.MotorDir.index(mdir)
        
        if (self.debug):
            print("set PWM PIN %d, speed %d" %(self.MotorPin[mPin+1], speed))
            print("set pin A %d , dir %d" %(self.MotorPin[mPin+2], self.MotorDir[mDir+1]))
            print("set pin b %d , dir %d" %(self.MotorPin[mPin+3], self.MotorDir[mDir+2]))

        # Set motor speed on the PWM channel and direction levels on the two control channels
        self.pwm.setServoPulse(self.MotorPin[mPin+1], speed)        
        self.pwm.setLevel(self.MotorPin[mPin+2], self.MotorDir[mDir+1])
        self.pwm.setLevel(self.MotorPin[mPin+3], self.MotorDir[mDir+2])
        
        # Keep the motor running for the specified duration in seconds
        time.sleep(runtime)
        # Stop the motor and reset all three channels back to 0
        self.pwm.setServoPulse(self.MotorPin[mPin+1], 0)
        self.pwm.setLevel(self.MotorPin[mPin+2], 0)
        self.pwm.setLevel(self.MotorPin[mPin+3], 0)

    def MotorStop(self, motor):
        # Find the starting index for the chosen motor
        mPin = self.MotorPin.index(motor)
        # Set the motor's PWM speed channel to 0 to stop it
        self.pwm.setServoPulse(self.MotorPin[mPin+1], 0)
