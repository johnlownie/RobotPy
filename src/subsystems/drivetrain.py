import wpilib

from wpilib.command.subsystem import Subsystem
from wpilib.drive import DifferentialDrive

class DriveTrain(Subsystem):
    def __init__(self, robot):
        self.left_front_motor = wpilib.Talon(1)
        self.left_rear_motor  = wpilib.Talon(2)
        self.left = wpilib.SpeedControllerGroup(self.left_front_motor, self.left_rear_motor)
        self.left.setInverted(False)

        self.right_front_motor = wpilib.Talon(3)
        self.right_rear_motor  = wpilib.Talon(4)
        self.right = wpilib.SpeedControllerGroup(self.right_front_motor, self.right_rear_motor)
        self.right.setInverted(True)

        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.drive.setSafetyEnabled(False)

    def arcadeDrive(self, speed, rotation):
        self.drive.arcadeDrive(speed, rotation)

    def stop(self):
        self.drive.arcadeDrive(0, 0)

    def initDefaultCommand(self):
        self.setDefaultCommand(DriveByJoystick(self.robot))