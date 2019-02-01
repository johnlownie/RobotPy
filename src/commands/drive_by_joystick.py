import wpilib

from wpilib.command import Command

class DriveByJoystick(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.drivetrain)
        self.robot = robot

    def initialize(self):
        pass

    def execute(self):
        xSpeed = self.robot.oi.getJoystick().getY()
        zRotation = self.robot.oi.getJoystick().getX() * -1

        if abs(xSpeed) <= self.robot.oi.XBOX_DEADZONE_LEFT_JOY:
            xSpeed = 0.0

        if abs(zRotation) <= self.robot.oi.XBOX_DEADZONE_LEFT_JOY:
            zRotation = 0.0

        self.robot.drivetrain.arcadeDrive(xSpeed, zRotation)

    def isFinished(self):
        return False

    def end(self):
        self.robot.drivetrain.stop()

    def interrupted(self):
        self.end()
    