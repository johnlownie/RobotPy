import wpilib

from wpilib.command import Command
from networktables import NetworkTables

# To see messages from networktables, you must setup logging
import logging

class AlignByCamera(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.hatchsystem)
        self.robot = robot

        logging.basicConfig(level=logging.DEBUG)

        NetworkTables.initialize()
        self.sd = NetworkTables.getTable("Shuffleboard/LiveWindow")

    def initialize(self):
        print("[AlignByCamera] Initialize")
        self.robot.hatchsystem.stop()
        self.sd.putNumber("Offset", 0.0)

    def execute(self):
        offset = self.sd.getNumber("Offset", 0)

        if offset > 0:
            self.robot.hatchsystem.setSpeed(1)
        elif offset < 0:
            self.robot.hatchsystem.setSpeed(-1)
        else:
            self.robot.hatchsystem.setSpeed(0)

    def isFinished(self):
        return False

    def end(self):
        print("[AlignByCamera] ending")
        self.robot.hatchsystem.stop()

    def interrupted(self):
        print("[AlignByCamera] interrupted")
        self.end()
    