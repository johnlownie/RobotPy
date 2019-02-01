import wpilib

from wpilib.command import Command
from wpilib.interfaces import GenericHID

class DriveByJoystick(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.drivetrain)
        self.robot = robot

    def initialize(self):
        pass

    def execute(self):
        speed = self.robot.oi.getJoystickDriver().getY()
        rotation = self.robot.oi.getJoystickDriver().getX(GenericHID.Hand.kLeft)

        if abs(speed) <= self.robot.oi.XBOX_DEADZONE_LEFT_JOY:
            speed = 0.0

        if abs(rotation) <= self.robot.oi.XBOX_DEADZONE_LEFT_JOY:
            rotation = 0.0

        self.robot.drivetrain.arcadeDrive(speed, rotation)

    def isFinished(self):
        return False

    def end(self):
        self.robot.drivetrain.stop()

    def interrupted(self):
        self.end()
    