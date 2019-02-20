import wpilib

from wpilib.command import Command
from wpilib.interfaces import GenericHID

class ClimbByJoystick(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.climbsystem)
        self.robot = robot

    def initialize(self):
        print("[ClimbByJoystick] initializing")
        pass

    def execute(self):
        pass

    def isFinished(self):
        return False

    def end(self):
        print("[ClimbByJoystick] ending")
        self.robot.climbsystem.stop()

    def interrupted(self):
        print("[ClimbByJoystick] interrupted")
        self.end()
    