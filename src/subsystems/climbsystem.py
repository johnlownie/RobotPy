import wpilib
import ctre

from wpilib.command.subsystem import Subsystem
from wpilib.drive import DifferentialDrive
from wpilib.analoginput import AnalogInput
from ctre import WPI_TalonSRX
from ctre.basemotorcontroller import BaseMotorController
from navx import AHRS

from commands.climb_by_joystick import ClimbByJoystick

class ClimbSystem(Subsystem):
    # set constants
    LEFT_ARM_MOTOR_ID = 5
    RIGHT_ARM_MOTOR_ID  = 6

    LEFT_CRAWL_MOTOR_ID = 20
    RIGHT_CRAWL_MOTOR_ID = 21

    CLIMB_LEG_MOTOR_ID = 8
    CLIMB_ULTRASONIC_ID = 1

    LEG_TOP_HALL_EFFECT_ID = 1
    LEG_MIDDLE_HALL_EFFECT_ID = 5
    LEG_BOTTOM_HALL_EFFECT_ID = 6

    def __init__(self, robot):
        print("[ClimbSystem] initializing")
 
        super().__init__("ClimbSystem")
        self.robot = robot
 
        left_arm_motor = ctre.WPI_TalonSRX(self.LEFT_ARM_MOTOR_ID)
        left_arm_motor.setInverted(False)
        left_arm_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        left_arm_motor.setSafetyEnabled(False)
        left_arm_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0.0)
        self.left_arm_motor = left_arm_motor

        right_arm_motor = ctre.WPI_TalonSRX(self.RIGHT_ARM_MOTOR_ID)
        right_arm_motor.setInverted(True)
        right_arm_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        right_arm_motor.setSafetyEnabled(False)
        right_arm_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0.0)
        right_arm_motor.follow(left_arm_motor)
        self.right_arm_motor = right_arm_motor

        leg_motor = ctre.WPI_TalonSRX(self.CLIMB_LEG_MOTOR_ID)
        leg_motor.setInverted(False)
        leg_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        leg_motor.setSafetyEnabled(False)
        leg_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0.0)
        self.leg_motor = leg_motor

        left_crawl_motor = ctre.WPI_TalonSRX(self.LEFT_CRAWL_MOTOR_ID)
        left_crawl_motor.setInverted(False)
        left_crawl_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        left_crawl_motor.setSafetyEnabled(False)
        left_crawl_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0.0)

        right_crawl_motor = ctre.WPI_TalonSRX(self.RIGHT_CRAWL_MOTOR_ID)
        right_crawl_motor.setInverted(True)
        right_crawl_motor.setNeutralMode(BaseMotorController.NeutralMode.Brake)
        right_crawl_motor.setSafetyEnabled(False)
        right_crawl_motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0.0)

        self.drive = wpilib.drive.DifferentialDrive(left_crawl_motor, right_crawl_motor)
        self.drive.setSafetyEnabled(False)

        self.ultrasonic = wpilib.AnalogInput(self.CLIMB_ULTRASONIC_ID)

        self.leg_top_hall_effect = wpilib.DigitalInput(self.LEG_TOP_HALL_EFFECT_ID)
        self.leg_middle_hall_effect = wpilib.DigitalInput(self.LEG_MIDDLE_HALL_EFFECT_ID)
        self.leg_bottom_hall_effect = wpilib.DigitalInput(self.LEG_BOTTOM_HALL_EFFECT_ID)

    def moveArms(self, speed):
        self.left_arm_motor.set(speed)

    def moveLeg(self, speed):
        self.leg_motor.set(speed)

    def stop(self):
        self.moveArms(0.0)
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

