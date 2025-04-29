from .motor import Motor
from .leg import Leg
from .movement import Rover

# Front left leg config
MOTOR_FL_FW_PIN = 1
MOTOR_FL_BW_PIN = 2
LEG_FL_SERVO_PIN = 3

# Front right leg config
MOTOR_FR_FW_PIN = 4
MOTOR_FR_BW_PIN = 5
LEG_FR_SERVO_PIN = 6

# Rear left leg config
MOTOR_RL_FW_PIN = 7
MOTOR_RL_BW_PIN = 8
LEG_RL_SERVO_PIN = 9

# Rear right leg config
MOTOR_RR_FW_PIN = 10
MOTOR_RR_BW_PIN = 11
LEG_RR_SERVO_PIN = 12

def create_rover():
    """
    Create the rover object.
    """
    motor_fl = Motor(MOTOR_FL_FW_PIN, MOTOR_FL_BW_PIN)
    leg_fl = Leg(LEG_FL_SERVO_PIN, motor_fl, "FRONT_LEFT")

    motor_fr = Motor(MOTOR_FR_FW_PIN, MOTOR_FR_BW_PIN)
    leg_fr = Leg(LEG_FR_SERVO_PIN, motor_fr, "FRONT_RIGHT")

    motor_rl = Motor(MOTOR_RL_FW_PIN, MOTOR_RL_BW_PIN)
    leg_rl = Leg(LEG_RL_SERVO_PIN, motor_rl, "REAR_LEFT")

    motor_rr = Motor(MOTOR_RR_FW_PIN, MOTOR_RR_BW_PIN)
    leg_rr = Leg(LEG_RR_SERVO_PIN, motor_rr, "REAR_RIGHT")

    return Rover(leg_fl, leg_fr, leg_rl, leg_rr)
