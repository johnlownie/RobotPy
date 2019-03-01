import wpilib

from wpilib.command import Command
from wpilib.interfaces import GenericHID

class AlignByTriggers(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.hatchsystem)
        self.robot = robot

    def initialize(self):
        print("[AlignByTriggers] initializing")
        pass

    def execute(self):
        # align hatch by triggers
        # speed = right trigger - left trigger
        speed = self.robot.oi.getJoystickOperator().getTriggerAxis(GenericHID.Hand.kRight) - self.robot.oi.getJoystickOperator().getTriggerAxis(GenericHID.Hand.kLeft)

        if abs(speed) <= self.robot.oi.XBOX_DEADZONE_LEFT_JOY:
            speed = 0.0

        self.robot.hatchsystem.setSpeed(speed)

    def isFinished(self):
        return False

    def end(self):
        print("[AlignByTriggers] ending")
        self.robot.hatchsystem.stop()

    def interrupted(self):
        print("[AlignByTriggers] interrupted")
        self.end()
    