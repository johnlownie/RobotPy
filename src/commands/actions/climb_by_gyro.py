import wpilib
import math

from wpilib import Timer
from wpilib.command import Command

class ClimbByGyro(Command):

    def __init__(self, robot):
        super().__init__()
        self.requires(robot.climbsystem)
        self.requires(robot.drivetrain)
        self.robot = robot

        self.logCount = 0

    def initialize(self):
        print ("[ClimbByGyro] initializing")
        # start the arm motors at a constant rate
        # the leg motor should adjust to keep the robot level
        self.robot.climbsystem.moveArms(0.65)

    def execute(self):
        # adjust the leg motor speed to keep the robot level
        pitchAngleDegrees = self.robot.drivetrain.ahrs.getPitch()
        pitchAngleRadians = pitchAngleDegrees * (math.pi / 180.0)
        xAxisRate = math.sin(pitchAngleRadians) * -1

        # move the leg according to the pitch rate
        self.robot.climbsystem.moveLeg(xAxisRate)

        self.logCount += 1
        if (self.logCount > 10):
            self.log(xAxisRate)
            self.logCount = 0

    def isFinished(self):
        return self.robot.climbsystem.leg_bottom_hall_effect.get()

    def end(self):
        print ("[ClimbByGyro] ending")
        self.robot.climbsystem.stop()

    def interrupted(self):
        print ("[ClimbByGyro] interrupted")
        self.end()

    def log(self, xAxisRate):
        print ("[ClimbByGyro] xAxisRate: ", xAxisRate, " - Bottom Hall Effect: ", self.robot.climbsystem.leg_bottom_hall_effect.get())
