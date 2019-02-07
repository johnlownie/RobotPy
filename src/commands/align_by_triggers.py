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

        if self.robot.oi.getJoystickDriver().getStartButtonPressed() or self.robot.oi.getJoystickOperator().getStartButtonPressed():
            print("[AlignByTriggers] start charging pneumatics")
            self.robot.hatchsystem.setState(True)
        elif self.robot.oi.getJoystickDriver().getBackButtonPressed() or self.robot.oi.getJoystickOperator().getBackButtonPressed():
            print("[AlignByTriggers] stop charging pneumatics")
            self.robot.hatchsystem.setState(False)

        # align hatch by triggers
        # speed = right trigger - left trigger
        speed = self.robot.oi.getJoystickOperator().getTriggerAxis(GenericHID.Hand.kRight) - self.robot.oi.getJoystickOperator().getTriggerAxis(GenericHID.Hand.kLeft)

        if abs(speed) <= self.robot.oi.XBOX_DEADZONE_LEFT_JOY:
            speed = 0.0

        self.robot.hatchsystem.setSpeed(speed)

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

        # fire the piston when B button is pressed
        if self.robot.oi.getJoystickOperator().getBButtonPressed():
            self.robot.hatchsystem.deploy()
        elif self.robot.oi.getJoystickOperator().getBButtonReleased():
            self.robot.hatchsystem.retract()

    def isFinished(self):
        return False

    def end(self):
        print("[AlignByTriggers] ending")
        self.robot.hatchsystem.stop()

    def interrupted(self):
        print("[AlignByTriggers] interrupted")
        self.end()
    