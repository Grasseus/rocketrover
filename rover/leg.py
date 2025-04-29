from .motor import Motor

# The legs are in a drone-like formation:
#          A   B
#           \ /
#           / \
#          B   A
#
# A and B move in the opposite direction when the servo turns the same angle

class Leg:
    def __init__(self, servo_pin, motor: Motor, position: str):
        """
        Initialize the leg.
        Args:
            servo_pin (int): pin of the servo controlling the leg
            motor (Motor): instance of the Motor class
            position (str): the position of the leg. The string MUST be in this form: FRONT_LEFT, FRONT_RIGHT, REAR_LEFT, REAR_RIGHT
        """
        self.servo_pin = servo_pin
        self.motor = motor
        self.position = position

    async def set_angle(self, angle):
        """
        Set the angle of the leg.
        Args:
            angle (int): angle of the leg. Range: [-60, 60] (positive is outwards)
        """
        try:
            print(f"{self.position} Leg is at angle {angle}")
        except Exception as e:
            print(f"Error while setting leg angle: {e}")

    def is_diagonal_a(self):
        """
        Check if the leg either front-left or rear-right
        """
        return self.position in ["FRONT_LEFT", "REAR_RIGHT"]
