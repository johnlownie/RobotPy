import wpilib

from wpilib.command import Command

class ToggleLED(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.hatchsystem)
        self.robot = robot

    def initialize(self):
        print("[ToggleLED] Initialize")
        self.robot.hatchsystem.toggleLED()

    def execute(self):
        pass

    def isFinished(self):
        return True

    def end(self):
        print("[ToggleLED] ending")
        pass

    def interrupted(self):
        print("[ToggleLED] interrupted")
        self.end()
    