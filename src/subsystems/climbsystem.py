import wpilib
import ctre

from wpilib.command.subsystem import Subsystem
from wpilib.drive import DifferentialDrive
from wpilib.analoginput import AnalogInput
from ctre import WPI_TalonSRX
from ctre.basemotorcontroller import BaseMotorController

from commands.climb_by_joystick import ClimbByJoystick

class ClimbSystem(Subsystem):
    # set constants
    LEFT_ARM_MOTOR = 5
    RIGHT_ARM_MOTOR  = 6
    LEFT_CRAWL_MOTOR = 20
    RIGHT_CRAWL_MOTOR = 21
    CLIMB_LEG_MOTOR = 8
    CLIMB_ULTRASONIC = 1

    def __init__(self, robot):
        print("[ClimbSystem] initializing")
 
        super().__init__("ClimbSystem")
        self.robot = robot
 
        left_arm_motor = ctre.WPI_TalonSRX(self.LEFT_ARM_MOTOR)
        left_arm_motor.setInverted(False)
        left_arm_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        left_arm_motor.setSafetyEnabled(False)
        left_arm_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0.0)
        self.left_arm_motor = left_arm_motor

        right_arm_motor = ctre.WPI_TalonSRX(self.RIGHT_ARM_MOTOR)
        right_arm_motor.setInverted(True)
        right_arm_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        right_arm_motor.setSafetyEnabled(False)
        right_arm_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0.0)
        right_arm_motor.follow(left_arm_motor)
        self.right_arm_motor = right_arm_motor

        leg_motor = ctre.WPI_TalonSRX(self.CLIMB_LEG_MOTOR)
        leg_motor.setInverted(False)
        leg_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        leg_motor.setSafetyEnabled(False)
        leg_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0.0)
        self.leg_motor = leg_motor

        left_crawl_motor = ctre.WPI_TalonSRX(self.LEFT_CRAWL_MOTOR)
        left_crawl_motor.setInverted(False)
        left_crawl_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        left_crawl_motor.setSafetyEnabled(False)
        left_crawl_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0.0)

        right_crawl_motor = ctre.WPI_TalonSRX(self.RIGHT_CRAWL_MOTOR)
        right_crawl_motor.setInverted(True)
        right_crawl_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        right_crawl_motor.setSafetyEnabled(False)
        right_crawl_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0.0)

        self.drive = wpilib.drive.DifferentialDrive(left_crawl_motor, right_crawl_motor)
        self.drive.setSafetyEnabled(False)

        self.ultrasonic = wpilib.AnalogInput(self.CLIMB_ULTRASONIC)

        print("[ClimbSystem] initialized")

    def moveArm(self, speed):
        self.left_arm_motor.set(speed)

    def moveLeg(self, speed):
        self.leg_motor.set(speed)

    def stop(self):
        self.moveArm(0.0)
        self.moveLeg(0.0)
        self.arcadeDrive(0.0, 0.0)

    def arcadeDrive(self, speed, rotation):
        self.drive.arcadeDrive(speed, rotation)

    def getDistanceFromFloor(self):
        return self.ultrasonic.getValue() * 0.125

    def initDefaultCommand(self):
        pass
        # print("[ClimbSystem] setting default command")
        # self.setDefaultCommand(ClimbByJoystick(self.robot))

