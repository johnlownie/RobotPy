import wpilib

from wpilib.command import Command

class DeployHatch(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.hatchsystem)
        self.robot = robot

    def initialize(self):
        print("[DeployHatch] Initialize")
        self.robot.hatchsystem.deploy()

    def execute(self):
        pass

    def isFinished(self):
        return True

    def end(self):
        print("[DeployHatch] ending")
        self.robot.hatchsystem.retract()

    def interrupted(self):
        print("[DeployHatch] interrupted")
        self.end()
    