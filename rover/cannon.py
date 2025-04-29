from .motor import Motor


class Cannon:
    def __init__(
        self,
        camera_angle_servo,
        gun_angle_servo,
        gun_trigger_servo,
        reload_motor,
        reload_switch_pin: Motor,
    ):
        self.camera_angle_servo = camera_angle_servo
        self.gun_angle_servo = gun_angle_servo
        self.gun_trigger_servo = gun_trigger_servo
        self.reload_motor = reload_motor
        self.reload_switch_pin = reload_switch_pin
