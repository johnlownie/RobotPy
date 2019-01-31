import math
import wpilib

from wpilib.command.subsystem import Subsystem
from wpilib.drive import DifferentialDrive
from navx import AHRS

class DriveTrain(Subsystem):
    if robot.isReal():
        kP = 0.03
        kI = 0.00
        kD = 0.00
        kF = 0.00
    else:
        kP = 0.02
        kI = 0.00
        kD = 0.00
        kF = 0.00

    kToleranceDegrees = 2.0

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

        self.left_encoder  = wpilib.Encoder(1, 2)
        self.right_encoder = wpilib.Encoder(3, 4)

        if robot.isReal():
            self.left_encoder.setDistancePerPulse(0.042)
            self.right_encoder.setDistancePerPulse(0.042)
        else:
            self.left_encoder.setDistancePerPulse((7.5 / 12.0 * math.pi) / 360.0)
            self.right_encoder.setDistancePerPulse((7.5 / 12.0 * math.pi) / 360.0)

        self.ahrs = AHRS.create_spi

        turnController = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, self.ahrs, output=self)
        turnController.setInputRange(-180.0, 180.0)
        turnController.setOutputRange(-1.0, 1.0)
        turnController.setAbsoluteTolerance(self.kToleranceDegrees)
        turnController.setContinuous(True)

        self.turnController = turnController
        self.rotateToAngleRate = 0

        wpilib.LiveWindow.addActuator("DriveTrain", "Front Left Motor", self.left_front_motor)
        wpilib.LiveWindow.addActuator("DriveTrain", "Rear Left Motor", self.left_rear_motor)
        wpilib.LiveWindow.addActuator("DriveTrain", "Front Right Motor", self.right_front_motor)
        wpilib.LiveWindow.addActuator("DriveTrain", "Rear Right Motor", self.right_rear_motor)

        wpilib.LiveWindow.addSensor("DriveTrain", "Left Encoder", self.left_encoder)
        wpilib.LiveWindow.addSensor("DriveTrain", "Right Encoder", self.right_encoder)
        wpilib.LiveWindow.addSensor("DriveTrain", "Gyro", self.ahrs)

    def arcadeDrive(self, speed, rotation):
        self.drive.arcadeDrive(speed, rotation)

    def reset(self):
        self.left_encoder.reset()
        self.right_encoder.reset()
        self.ahrs.reset()
        
    def stop(self):
        self.drive.arcadeDrive(0, 0)

    def initDefaultCommand(self):
        self.setDefaultCommand(DriveByJoystick(self.robot))

    def log(self):
        wpilib.SmartDashboard.putNumber("Left Speed" , self.left_encoder.getRate())
        wpilib.SmartDashboard.putNumber("Right Speed", self.right_encoder.getRate())
        wpilib.SmartDashboard.putNumber("Gyro"       , self.ahrs.getAngle())