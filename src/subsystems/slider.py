import wpilib

from wpilib.command.subsystem import Subsystem

class Slider(Subsystem):
    LEFT  =  1
    STOP  =  0
    RIGHT = -1

    def __init__(self, robot):
        self.motor = wpilib.Talon(5)
        wpilib.LiveWindow.addActuator("Slider", "Alignment Motor", self.motor)

        super().__init__("Slider")

    def setSpeed(self, speed):
        self.motor.set(speed)

    def stop(self):
        self.motor.set(0)

    def initDefaultCommand(self):
        pass