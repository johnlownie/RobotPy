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
        # deploy the arm when X button is pressed
        if self.robot.oi.getJoystickOperator().getXButtonPressed():
            self.robot.climbsystem.moveArm(1.0)
        elif self.robot.oi.getJoystickOperator().getXButtonReleased():
            self.robot.climbsystem.moveArm(0.0)

        # deploy the leg when A button is pressed
        if self.robot.oi.getJoystickOperator().getAButtonPressed():
            self.robot.climbsystem.moveLeg(1.0)
        elif self.robot.oi.getJoystickOperator().getAButtonReleased():
            self.robot.climbsystem.moveLeg(0.0)

    def isFinished(self):
        return False

    def end(self):
        print("[ClimbByJoystick] ending")
        self.robot.climbsystem.stop()

    def interrupted(self):
        print("[ClimbByJoystick] interrupted")
        self.end()
    