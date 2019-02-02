import wpilib

from ctre import WPI_TalonSRX
from wpilib import Timer
from wpilib.command import Command
from wpilib.interfaces import GenericHID
from autonomous.profiles.pfl_just_drive_forward import PFLJustDriveForward

class CMDJustDriveForward(Command):
    def __init__(self, robot):
        super().__init__()
        self.requires(robot.drivetrain)
        self.robot = robot

        self.pMotionProfiler = PFLJustDriveForward(robot)
        self.pTimer = Timer()

    def initialize(self):
        print("[CMDJustDriveForward] initialized")
        self.robot.drivetrain.initMotionProfilingMode()

        self.pTimer.reset()
        self.pTimer.start()

    def execute(self):
        self.pMotionProfiler.control()
        self.pMotionProfiler.periodicTask()

        setOutput = self.pMotionProfiler.getSetValue()

        self.robot.drivetrain.left_front_motor.set(WPI_TalonSRX.ControlMode.MotionProfile, setOutput)
        self.robot.drivetrain.right_front_motor.set(WPI_TalonSRX.ControlMode.MotionProfile, setOutput)

        self.pMotionProfiler.start()

    def isFinished(self):
        if self.pMotionProfiler.isFinished():
            print("[CMDJustDriveForward] motion profile finished")
            return True

        return False

    def end(self):
        self.robot.drivetrain.resetDrive()

    def interrupted(self):
        self.end()
    