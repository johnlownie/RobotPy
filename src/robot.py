#!/usr/bin/env python3

import numpy as np
import wpilib

from networktables import NetworkTables
from networktables import NetworkTablesInstance
from wpilib import Timer
from wpilib.command import Scheduler
from wpilib.shuffleboard import Shuffleboard

from subsystems.oi import OI
from subsystems.drivetrain import DriveTrain
from subsystems.slider import Slider

class MyRobot(wpilib.TimedRobot):
    table = NetworkTablesInstance.getDefault().getTable("Shuffleboard/LiveWindow")
    x = 0.0
    y = 0.0

    def robotInit(self):
        # wpilib.CameraServer.launch("vision.py:main")
        print("[Robot] Initialized")
        self.drivetrain = DriveTrain(self)
        self.slider = Slider(self)

        self.oi = OI(self)
 
        # wpilib.SmartDashboard.putData(self.drivetrain)

    def teleopInit(self):
        return super().teleopInit()

    def teleopPeriodic(self):
        Scheduler.getInstance().run()

    def log(self):
        self.drivetrain.log()

if __name__ == "__main__":
    wpilib.run(MyRobot)