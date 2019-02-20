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
    LED_SOLENOID_ID = 0
    PISTON_SOLENOID_ID = 1
    COMPRESSOR_PIN = 0

    def __init__(self, robot):
        print("[HatchSystem] initializing")

        super().__init__("HatchSystem")
        self.robot = robot

        self.motor = ctre.WPI_TalonSRX(self.SLIDER_MOTOR)
        self.led = wpilib.Solenoid(self.PCM_CAN_ID, self.LED_SOLENOID_ID)
        self.ejector = wpilib.Solenoid(self.PCM_CAN_ID, self.PISTON_SOLENOID_ID)
        self.compressor = wpilib.Compressor(self.COMPRESSOR_PIN)

        wpilib.LiveWindow.addActuator("HatchSystem", "Alignment Motor", self.motor)

        print("[HatchSystem] initialized")

    def setSpeed(self, speed):
        self.motor.set(speed)

    def stop(self):
        self.motor.set(WPI_TalonSRX.ControlMode.PercentOutput, 0)

    def deploy(self):
        self.ejector.set(True)

    def retract(self):
        self.ejector.set(False)

    def toggleCompressor(self):
        self.compressor.setClosedLoopControl(not self.compressor.getClosedLoopControl())

    def toggleLED(self):
        self.led.set(not self.led.get())

    def initDefaultCommand(self):
        print("[HatchSystem] setting default command")
        self.setDefaultCommand(AlignByTriggers(self.robot))
