import wpilib

from wpilib.command.subsystem import Subsystem

class CargoSystem(Subsystem):
    # set constants
    PCM_CAN_ID = 11
    FLAP_FORWARD_ID = 5
    FLAP_REVERSE_ID = 6

    def __init__(self, robot):
        print("[CargoSystem] initializing")

        super().__init__("CargoSystem")
        self.robot = robot

        self.flap = wpilib.DoubleSolenoid(self.PCM_CAN_ID, self.FLAP_FORWARD_ID, self.FLAP_REVERSE_ID)

    def deploy(self):
        self.flap.set(wpilib.DoubleSolenoid.Value.kForward)

    def retract(self):
        self.flap.set(wpilib.DoubleSolenoid.Value.kReverse)

    def release(self):
        self.flap.set(wpilib.DoubleSolenoid.Value.kOff)

    def initDefaultCommand(self):
        pass