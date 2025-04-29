class Motor:
    def __init__(self, fw_pin, bw_pin, pwm_freq=50.0):
        """
        Initialize the motor with forward and backward pins and sets the PWM frequency.

        Args:
            fw_pin (int): Pin number for forward direction.
            bw_pin (int): Pin number for backward direction.
            pwm_freq (float): PWM frequency for motor control (default: 50.0).
        """
        self.fw_pin = fw_pin
        self.bw_pin = bw_pin
        self._set_pwm_freq(pwm_freq)

    async def set_speed(self, speed):
        """
        Set the speed and direction of the motor.

        Args:
            speed (int): controls the speed of the motor. Range [-100, 100] (positive is forward)
        """
        try:
            if 0 <= speed <= 100:
                print(
                    f"Motor is spinning forward at {speed} percent using pin {self.fw_pin}"
                )
            elif -100 <= speed < 0:
                print(
                    f"Motor is spinning backward at {-speed} percent using pin {self.bw_pin}"
                )
            else:
                print("Please provide valid speed input")
        except Exception as e:
            print(f"Error while setting speed of motor: {e}")

    async def brake(self):
        """
        Stop the motor.
        """
        try:
            print("Motor is braking")
        except Exception as e:
            print(f"Error while braking: {e}")

    def _set_pwm_freq(self, pwm_freq):
        """
        Set the PWM frequency of the motor. Please make sure to use an adequate frequency (50-100Hz for small motors)
        Args:
            pwm_freq (float): Frequency for PWM control
        """
        print(
            f"Motor uses a PWM Frequency of {pwm_freq:.2f} for pins {self.fw_pin} and {self.bw_pin}"
        )
