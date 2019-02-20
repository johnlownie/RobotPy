import wpilib

from wpilib.command import Command

class DropCargo(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.cargosystem)
        self.robot = robot

    def initialize(self):
        print("[DropCargo] Initialize")
        self.robot.cargosystem.deploy()

    def execute(self):
        pass

    def isFinished(self):
        return True

    def end(self):
        print("[DropCargo] ending")
        self.robot.cargosystem.retract()
        self.robot.cargosystem.release()

    def interrupted(self):
        print("[DropCargo] interrupted")
        self.end()
    