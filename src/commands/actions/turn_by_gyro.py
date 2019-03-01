import wpilib

from wpilib import Timer
from wpilib.command import Command

class TurnByGyro(Command):

    def __init__(self, robot, angle):
        super().__init__()
        self.requires(robot.drivetrain)
        self.robot = robot

        self.angle = angle
        self.timer = Timer()

    def initialize(self):
        print("[TurnByGyro] initializing")
        self.robot.drivetrain.resetGyro()
        self.robot.drivetrain.turnController.setSetpoint(self.angle)

        self.timer.reset()
        self.timer.start()   

    def execute(self):
        self.robot.drivetrain.turn()

    def isFinished(self):
        if self.timer.get() > 5.0:
            print("[TurnByGyro] timed out")
            return True

        # if self.robot.drivetrain.reachedAngle(self.angle):
            # print("[TurnByGyro] reached target")
            # return True

        return False

    def end(self):
        print ("[TurnByGyro] ending")
        self.robot.drivetrain.resetDrive()

    def interrupted(self):
        print ("[ClimbByGyro] interrupted")
        self.end()
