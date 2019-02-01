import wpilib

from wpilib.command import Command
from wpilib.interfaces import GenericHID

class DriveByTriggers(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.drivetrain)
        self.robot = robot

    def initialize(self):
        self.directionMultiplier = 1
        self.speedMultiplier = 1

    def execute(self):
        # Deal with reversing and slow mode
        if self.robot.oi.getJoystickDriver().getXButtonReleased():
            self.directionMultiplier = 1
        else:
            self.directionMultiplier = -1

        if self.robot.oi.getJoystickDriver().getBumper(GenericHID.Hand.kRight):
            self.speedMultiplier = 0.6
        else:
            self.speedMultiplier = 1

        # speed = right trigger - left trigger
        speed = self.robot.oi.getJoystickDriver().getTriggerAxis(GenericHID.Hand.kRight) - self.robot.oi.getJoystickDriver().getTriggerAxis(GenericHID.Hand.kLeft)
        rotation = self.robot.oi.getJoystickDriver().getX(GenericHID.Hand.kLeft)
	
        # scale each value with it's multiplier
        speed *= self.speedMultiplier * self.directionMultiplier
        rotation *= self.speedMultiplier * self.robot.oi.DRIVEWITHJOYSTICK_ROTATION_LIMITER

        if abs(rotation) <= self.robot.oi.XBOX_DEADZONE_LEFT_JOY:
            rotation = 0.0

        self.robot.drivetrain.arcadeDrive(speed, rotation)

    def isFinished(self):
        return False

    def end(self):
        self.robot.drivetrain.stop()

    def interrupted(self):
        self.end()
    