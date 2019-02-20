import wpilib

from wpilib.command import Command

class ToggleCompressor(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.hatchsystem)
        self.robot = robot

    def initialize(self):
        print("[ToggleCompressor] Initialize")
        self.robot.hatchsystem.toggleCompressor()

    def execute(self):
        pass

    def isFinished(self):
        return True

    def end(self):
        print("[ToggleCompressor] ending")
        pass

    def interrupted(self):
        print("[ToggleCompressor] interrupted")
        self.end()
    