#!/usr/bin/env python3

import numpy as np
import wpilib

from networktables import NetworkTables
from networktables import NetworkTablesInstance
from wpilib import Timer
from wpilib.shuffleboard import Shuffleboard

from subsystems.oi import OI
from subsystems.slider import Slider

class MyRobot(wpilib.TimedRobot):
    table = NetworkTablesInstance.getDefault().getTable("Shuffleboard/LiveWindow")
    x = 0.0
    y = 0.0

    def robotInit(self):
        # wpilib.CameraServer.launch("vision.py:main")
        self.slider = Slider(self)

        self.oi = OI(self)
 
    def teleopInit(self):
        myEntry = (Shuffleboard.getTab("LiveWindow")
            .add(title="Offsetter", value=0)
            .withWidget("Number Bar")
            .withProperties({"min": -6, "max": 6})
            .getEntry())
        # self.table.add(title="Offset", value=0)
        #     .withWidget("Number Bar")
        # self.table.putNumber("Z", 0.0)

        return super().teleopInit()

    def teleopPeriodic(self):
        self.table.putNumber("X", self.x)
        self.table.putNumber("Y", self.y)
        self.x += 0.05
        self.y += 1.0

        self.log()

        return super().teleopPeriodic()

    def log(self):
        pass

if __name__ == "__main__":
    wpilib.run(MyRobot)