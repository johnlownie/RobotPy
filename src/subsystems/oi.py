import wpilib

from wpilib import SmartDashboard
from wpilib.buttons import JoystickButton

from commands.align import Align
from commands.set_alignment_speed import SetAlignmentSpeed

from subsystems.hatchaligner import HatchAligner

class OI(object):

    def __init__(self, robot):
        self.joystick = wpilib.Joystick(0)
        JoystickButton(self.joystick, 4).whenPressed(Align(robot))

        SmartDashboard.putData("Move Left" , SetAlignmentSpeed(robot, HatchAligner.LEFT ))
        SmartDashboard.putData("Stop"      , SetAlignmentSpeed(robot, HatchAligner.STOP ))
        SmartDashboard.putData("Move Right", SetAlignmentSpeed(robot, HatchAligner.RIGHT))

    def getJoystick(self):
        return self.joystick
