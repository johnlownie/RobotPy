import math
import wpilib
import ctre

from wpilib.command.subsystem import Subsystem
from wpilib.drive import DifferentialDrive
from navx import AHRS
from ctre.basemotorcontroller import BaseMotorController
from commands.drive_by_joystick import DriveByJoystick
from commands.drive_by_triggers import DriveByTriggers

class DriveTrain(Subsystem):
    # set constants
    WHEEL_DIAMETER = 0.625
    ENCODER_PULSE_PER_REV = 4096
    SLOTIDX = 0
    PIDLOOPIDX = 0
    TIMEOUT_MS = 100
    ENCODER_CONSTANT = (1 / ENCODER_PULSE_PER_REV) * WHEEL_DIAMETER * math.pi

    kToleranceDegrees = 2.0

    def __init__(self, robot):
        print("[DriveTrain] Initialized")
        super().__init__()
        self.robot = robot

        # set PIDF values
        if robot.isReal():
            self.kP = 0.03
            self.kI = 0.00
            self.kD = 0.00
            self.kF = 0.00
        else:
            self.kP = 0.02
            self.kI = 0.00
            self.kD = 0.00
            self.kF = 0.00

        left_front_motor = ctre.WPI_TalonSRX(1)
        left_front_motor.setInverted(False)
        left_front_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        self.left_front_motor = left_front_motor

        left_rear_motor = ctre.WPI_TalonSRX(2)
        left_rear_motor.setInverted(False)
        left_rear_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        left_rear_motor.follow(left_front_motor)
        self.left_rear_motor = left_rear_motor

        right_front_motor = ctre.WPI_TalonSRX(3)
        right_front_motor.setInverted(True)
        right_front_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        self.right_front_motor = right_front_motor
       
        right_rear_motor  = ctre.WPI_TalonSRX(4)
        right_rear_motor.setInverted(True)
        right_rear_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        right_rear_motor.follow(right_front_motor)
        self.right_rear_motor = right_rear_motor

        self.left = wpilib.SpeedControllerGroup(left_front_motor, left_rear_motor)
        self.right = wpilib.SpeedControllerGroup(right_front_motor, right_rear_motor)

        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.drive.setDeadband(0)
        self.drive.setSafetyEnabled(False)
        
        # setup NavX and turn controller
        self.ahrs = AHRS.create_spi

        # turnController = wpilib.PIDController(self.kP, self.kI, self.kD, self.kF, output=self)
        # turnController.setInputRange(-180.0, 180.0)
        # turnController.setOutputRange(-1.0, 1.0)
        # turnController.setAbsoluteTolerance(self.kToleranceDegrees)
        # turnController.setContinuous(True)

        # self.turnController = turnController
        self.rotateToAngleRate = 0

        # setup LiveWindow
        wpilib.LiveWindow.addActuator("DriveTrain", "Front Left Motor", self.left_front_motor)
        wpilib.LiveWindow.addActuator("DriveTrain", "Rear Left Motor", self.left_rear_motor)
        wpilib.LiveWindow.addActuator("DriveTrain", "Front Right Motor", self.right_front_motor)
        wpilib.LiveWindow.addActuator("DriveTrain", "Rear Right Motor", self.right_rear_motor)

        # wpilib.LiveWindow.addSensor("DriveTrain", "Left Encoder", self.left_encoder)
        # wpilib.LiveWindow.addSensor("DriveTrain", "Right Encoder", self.right_encoder)
        # wpilib.LiveWindow.addSensor("DriveTrain", "Gyro", self.ahrs)

    def initAutonomousMode(self):
        self.left_front_motor.configSelectedFeedbackSensor( WPI_TalonSRX.FeedbackDevice.CTRE_MagEncoder_Relative, self.PIDLOOPIDX, self.TIMEOUT_MS )

    def arcadeDrive(self, speed, rotation):
        self.drive.arcadeDrive(speed, rotation * -1)

    def tankDrive(self, speed, rotation):
        self.drive.tankDrive(speed, speed)

    def resetDrive(self):
        self.left_front_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
        self.left_rear_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
        self.right_front_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)
        self.right_rear_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)

        self.left_rear_motor.follow(self.left_front_motor)
        self.left_front_motor.setInverted(False)
        self.left_rear_motor.setInverted(False)

        self.right_rear_motor.follow(self.right_front_motor)
        self.right_front_motor.setInverted(True)
        self.right_rear_motor.setInverted(True)

        # self.turnController.disable()

    def resetEncoders(self):
        self.left_front_motor.setSelectedSensorPosition(0, PIDLOOPIDX, TIMEOUT_MS)
        self.right_front_motor.setSelectedSensorPosition(0, PIDLOOPIDX, TIMEOUT_MS)

    def stop(self):
        self.drive.arcadeDrive(0, 0)

    def initDefaultCommand(self):
        print("[DriveTrain] setting default command")
        self.setDefaultCommand(DriveByTriggers(self.robot))

    def log(self):
        pass
        # wpilib.SmartDashboard.putNumber("Left Speed" , self.left_encoder.getRate())
        # wpilib.SmartDashboard.putNumber("Right Speed", self.right_encoder.getRate())
        # wpilib.SmartDashboard.putNumber("Gyro"       , self.ahrs.getAngle())