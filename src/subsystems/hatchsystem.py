import wpilib
import ctre

from wpilib.command.subsystem import Subsystem
from ctre import WPI_TalonSRX
from wpilib import Compressor

from commands.align_by_triggers import AlignByTriggers

class HatchSystem(Subsystem):
    # set constants
    SLIDER_MOTOR = 7
    PCM_CAN_ID = 11
    PISTON_ID = 1
    COMPRESSOR_PIN = 0

    def __init__(self, robot):
        print("[Slider] Initialized")
        super().__init__("Slider")
        self.robot = robot

        self.motor = ctre.WPI_TalonSRX(self.SLIDER_MOTOR)
        self.solenoid = wpilib.Solenoid(self.PCM_CAN_ID, self.PISTON_ID)
        self.compressor = wpilib.Compressor(self.COMPRESSOR_PIN)

        wpilib.LiveWindow.addActuator("Slider", "Alignment Motor", self.motor)

    def setSpeed(self, speed):
        self.motor.set(speed)

    def stop(self):
        self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)

    def deploy(self):
        self.solenoid.set(True)

    def retract(self):
        self.solenoid.set(False)

    def setState(self, enabled):
        self.compressor.setClosedLoopControl(enabled)

    def initDefaultCommand(self):
        print("[Slider] setting default command")
        self.setDefaultCommand(AlignByTriggers(self.robot))
