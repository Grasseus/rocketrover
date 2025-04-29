from pydantic import BaseModel


class MoveCommand(BaseModel):
    speed: int
    rotation: int


class CalibrateCommand(BaseModel):
    leg_left_position: str
    leg_right_position: str
    amount: int


class SetLegsAngleCommand(BaseModel):
    angle: int


def get_command_map(rover):
    """
    Returns a command map for the rover functions.
    
    Args:
        rover (Rover): The rover object.
    """
    return {
        "move": {
            "handler": rover.move,
            "args": MoveCommand,
        },
        "calibrate": {
            "handler": rover.calibrate,
            "args": CalibrateCommand,
        },
        "set_legs_angle": {
            "handler": rover.set_legs_angle,
            "args": SetLegsAngleCommand,
        },
    }
