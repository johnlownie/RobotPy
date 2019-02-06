import wpilib

from wpilib import SmartDashboard
from wpilib.buttons import JoystickButton

from commands.align_by_camera import AlignByCamera
from commands.turn_by_gyro import TurnByGyro

class OI(object):
    # set constants
    XBOX_DEADZONE_LEFT_JOY = 0.1
    XBOX_DEADZONE_RIGHT_JOY = 0.1
    DRIVEWITHJOYSTICK_ROTATION_LIMITER = 0.95

    def __init__(self, robot):
        self.driver_joystick = wpilib.XboxController(0)
        self.operator_joystick = wpilib.XboxController(1)

        JoystickButton(self.driver_joystick, 3).whenPressed(TurnByGyro(robot, -90.0))
        JoystickButton(self.driver_joystick, 4).whenPressed(TurnByGyro(robot,  90.0))
        
        JoystickButton(self.operator_joystick, 4).whileHeld(AlignByCamera(robot))

    def getJoystickDriver(self):
        return self.driver_joystick

    def getJoystickOperator(self):
        return self.operator_joystick
