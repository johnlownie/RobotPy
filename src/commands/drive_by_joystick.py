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
        self.robot.drivetrain.arcadeDrive(self.robot.oi.getJoystick().getX(), self.robot.oi.getJoystick().getY())

    def isFinished(self):
        return False

    def end(self):
        self.robot.drivetrain.stop()

    def interrupted(self):
        self.end()
    