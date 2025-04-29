import asyncio
from .leg import Leg

MAX_LEG_ANGLE = 60
ROTATION_FACTOR = 0.25
MAX_SPEED = 100
REVERSE_BRAKE_THRESHOLD = 10
BRAKE_DURATION = 0.1

FRONT_LEFT = "FRONT_LEFT"
FRONT_RIGHT = "FRONT_RIGHT"
REAR_LEFT = "REAR_LEFT"
REAR_RIGHT = "REAR_RIGHT"


class Rover:
    def __init__(
        self,
        leg_front_left: Leg,
        leg_front_right: Leg,
        leg_rear_left: Leg,
        leg_rear_right: Leg,
    ):
        """Initialize the rover with four legs and their motors.

        Args:
            leg_front_left (Leg)
            leg_front_right (Leg)
            leg_rear_left (Leg)
            leg_rear_right (Leg)
        """
        self.legs = {
            FRONT_LEFT: leg_front_left,  # Front-left
            FRONT_RIGHT: leg_front_right,  # Front-right
            REAR_LEFT: leg_rear_left,  # Rear-left
            REAR_RIGHT: leg_rear_right,  # Rear-right
        }

        self.calibration_factors = {
            FRONT_LEFT: 1.0,  # Front-left
            FRONT_RIGHT: 1.0,  # Front-right
            REAR_LEFT: 1.0,  # Rear-left
            REAR_RIGHT: 1.0,  # Rear-right
        }

        self.previous_speeds = {
            FRONT_LEFT: 0,
            FRONT_RIGHT: 0,
            REAR_LEFT: 0,
            REAR_RIGHT: 0,
        }

    async def move(self, speed, rotation=0):
        """
        Move the rover by setting the speed of each leg's motor.

        Args:
            speed (int): Forward/backward speed. Range: [-100, 100].
            rotation (int): Rotational speed. Positive values turn right. Range: [-100, 100].
        """

        speeds = self._calculate_motor_speeds(speed, rotation)

        reversed_detected = any(
            self._is_motor_reversed(self.previous_speeds[pos], speeds[pos])
            for pos in speeds
        )

        if reversed_detected:
            async with asyncio.TaskGroup() as tg:
                for leg in self.legs.values():
                    tg.create_task(leg.motor.brake())
            await asyncio.sleep(BRAKE_DURATION)

        # Store the current speeds for checking motor reversal the next time
        self.previous_speeds = speeds

        # Set motor speeds
        async with asyncio.TaskGroup() as tg:
            for position in self.legs:
                tg.create_task(self.legs[position].motor.set_speed(speeds[position]))

    async def calibrate(self, leg_left_position: str, leg_right_position: str, amount):
        """
        Calibrate the rover's motors to ensure straight movement.


        Args:
            leg_left_position (str): String of the Leg position (e.g., FRONT_LEFT)
            leg_right_position (str): String of the Leg position (e.g., REAR_RIGHT)
            amount (int): The amount to adjust the calibration. Positive values make the rover lean to the right. Range: [-100, 100]

        Note:
            Two motors can be calibrated at a time. To achieve a full calibration, 3 iterations are needed:
                - front
                - diagonal
                - rear
        """

        # Move the unused legs out of the way
        await self._set_legs_while_calibrating(leg_left_position, leg_right_position)

        # Adjust the calibration factor
        if amount > 0:
            self.calibration_factors[leg_right_position] *= (100 - amount) / 100
        elif amount < 0:
            self.calibration_factors[leg_left_position] *= (100 + amount) / 100

        # Normalize the calibration factors
        largest_calibration_factor = max(self.calibration_factors.values())
        if 0 < largest_calibration_factor < 1:
            for factor in self.calibration_factors:
                # Prevents getting greater than 1 because of division inaccuracies
                self.calibration_factors[factor] = min(
                    self.calibration_factors[factor] / largest_calibration_factor, 1.0
                )
  
    async def set_legs_angle(self, angle):
        """
        Set the angles of the legs.

        Args:
            angle (int): The angle to set the legs to. Positive values move the legs outward. Range: [-60, 60]

        Note:
            Diagonal legs have the same angle, due to the geometry of the rover.
        """
        for leg in self.legs.values():
            if leg.is_diagonal_a():
                await leg.set_angle(-angle)
            else:
                await leg.set_angle(angle)

    def _is_motor_reversed(self, previous_speed, speed):
        """
        Check if a motor was reversed.

        Args:
            previous_speed (int): Value of previous speed
            speed (int): Value of current speed
        """
        return (
            abs(previous_speed) > REVERSE_BRAKE_THRESHOLD
            and (previous_speed * speed < 0)
            and abs(speed) > REVERSE_BRAKE_THRESHOLD
        )

    async def _set_legs_while_calibrating(self, leg_left_position, leg_right_position):
        """
        Set the angles of the legs while calibrating.

        Args:
            leg_left_position (str): String of the Leg position (e.g., FRONT_LEFT)
            leg_right_position (str): String of the Leg position (e.g., REAR_RIGHT)        
        """
        for leg in self.legs.values():
            if leg.position == leg_left_position or leg.position == leg_right_position:
                await leg.set_angle(0)
            elif leg.is_diagonal_a():
                await leg.set_angle(-MAX_LEG_ANGLE)
            else:
                await leg.set_angle(MAX_LEG_ANGLE)

    def _calculate_motor_speeds(self, speed, rotation):
        """
        Calculate the speed of each motor using the calibration data.
        
        Args:
            speed (int): Forward/backward speed. Range: [-100, 100].
            rotation (int): Rotational speed. Positive values turn right. Range: [-100, 100].
        """
        left_speed = speed + ROTATION_FACTOR * rotation
        right_speed = speed - ROTATION_FACTOR * rotation

        fl_speed = left_speed * self.calibration_factors[FRONT_LEFT]
        fr_speed = right_speed * self.calibration_factors[FRONT_RIGHT]
        rl_speed = left_speed * self.calibration_factors[REAR_LEFT]
        rr_speed = right_speed * self.calibration_factors[REAR_RIGHT]

        # Ensure none of the motor speeds exceed 100
        max_speed = max(abs(fl_speed), abs(fr_speed), abs(rl_speed), abs(rr_speed))
        if max_speed > MAX_SPEED:
            normalization_factor = MAX_SPEED / max_speed
            fl_speed *= normalization_factor
            fr_speed *= normalization_factor
            rl_speed *= normalization_factor
            rr_speed *= normalization_factor
        
        return {
            FRONT_LEFT: fl_speed,
            FRONT_RIGHT: fr_speed,
            REAR_LEFT: rl_speed,
            REAR_RIGHT: rr_speed,
        }
