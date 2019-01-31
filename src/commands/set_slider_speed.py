import wpilib

from wpilib.command import Command

class SetSliderSpeed(Command):

    def __init__(self, robot, speed):
        super().__init__()
        self.requires(robot.slider)
        self.speed = speed
        self.robot = robot

    def initialize(self):
        self.robot.logger.info("[SetSliderSpeed] Initialize")
        self.robot.slider.setSpeed(self.speed)

    def execute(self):
        pass

    def isFinished(self):
        self.robot.logger.info("[SetSliderSpeed] finished")
        return True

    def end(self):
        self.robot.logger.info("[SetSliderSpeed] ended")

    def interrupted(self):
        self.robot.logger.info("[SetSliderSpeed] interrupted")
