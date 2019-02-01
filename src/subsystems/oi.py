import wpilib

from wpilib import SmartDashboard
from wpilib.buttons import JoystickButton

from commands.align_slider import AlignSlider
from commands.set_slider_speed import SetSliderSpeed

from subsystems.slider import Slider

class OI(object):
    # set constants
    XBOX_DEADZONE_LEFT_JOY = 0.1
    XBOX_DEADZONE_RIGHT_JOY = 0.1
    DRIVEWITHJOYSTICK_ROTATION_LIMITER = 0.95

    def __init__(self, robot):
        self.driver_joystick = wpilib.XboxController(0)
        self.operator_joystick = wpilib.XboxController(1)

        # JoystickButton(self.joystick, 4).whenPressed(AlignSlider(robot))

        # SmartDashboard.putData("Move Left" , SetSliderSpeed(robot, Slider.LEFT ))
        # SmartDashboard.putData("Stop"      , SetSliderSpeed(robot, Slider.STOP ))
        # SmartDashboard.putData("Move Right", SetSliderSpeed(robot, Slider.RIGHT))

    def getJoystickDriver(self):
        return self.driver_joystick

    def getJoystickOperator(self):
        return self.operator_joystick
