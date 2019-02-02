import wpilib

from wpilib.command.subsystem import Subsystem
from commands.align_by_triggers import AlignByTriggers

class Slider(Subsystem):
    def __init__(self, robot):
        print("[Slider] Initialized")
        super().__init__("Slider")
        self.robot = robot

        self.motor = wpilib.Talon(5)
        wpilib.LiveWindow.addActuator("Slider", "Alignment Motor", self.motor)

    def setSpeed(self, speed):
        self.motor.set(speed)

    def stop(self):
        self.motor.set(0)

    def initDefaultCommand(self):
        print("[Slider] setting default command")
        self.setDefaultCommand(AlignByTriggers(self.robot))
