import wpilib

from wpilib.command import Command
from wpilib.interfaces import GenericHID

class AlignByTriggers(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.climbsystem)
        self.requires(robot.hatchsystem)
        self.robot = robot

    def initialize(self):
        pass

    def execute(self):
        # turn compressor on or off

        if self.robot.oi.getJoystickDriver.getStartButtonReleased or self.robot.oi.getJoystickOperator.getStartButtonReleased:
            self.robot.hatchsystem.setState(True)
        elif self.robot.oi.getJoystickDriver.getBackButtonReleased or self.robot.oi.getJoystickOperator.getBackButtonReleased:
            self.robot.hatchsystem.setState(False)

        # align hatch by triggers
        # speed = right trigger - left trigger
        speed = self.robot.oi.getJoystickOperator().getTriggerAxis(GenericHID.Hand.kRight) - self.robot.oi.getJoystickOperator().getTriggerAxis(GenericHID.Hand.kLeft)

        if abs(speed) <= self.robot.oi.XBOX_DEADZONE_LEFT_JOY:
            speed = 0.0

        self.robot.hatchsystem.setSpeed(speed)

        # deploy the arm when X button is pressed
        if self.robot.oi.getJoystickOperator.getXButtonPressed():
            self.robot.hatchsystem.moveArm(1.0)
        elif self.robot.oi.getJoystickOperator.getXButtonRelease():
            self.robot.hatchsystem.moveArm(0.0)

    def isFinished(self):
        return False

    def end(self):
        print("[AlignByTriggers] ending")
        self.robot.hatchsystem.stop()

    def interrupted(self):
        print("[AlignByTriggers] interrupted")
        self.end()
    