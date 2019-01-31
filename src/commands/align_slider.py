import wpilib

from wpilib.command import Command

class AlignSlider(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.slider)
        self.robot = robot

    def initialize(self):
        pass

    def execute(self):
        pass

    def isFinished(self):
        return False

    def end(self):
        self.robot.slider.stop()

    def interrupted(self):
        self.end()
    