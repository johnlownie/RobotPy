#!/usr/bin/env python3

import logging
import numpy as np
import wpilib

from networktables import NetworkTables, NetworkTablesInstance
from wpilib import SendableChooser
from wpilib import Timer
from wpilib.command import Scheduler
from wpilib.shuffleboard import Shuffleboard

from subsystems.oi import OI
from subsystems.drivetrain import DriveTrain
from subsystems.climbsystem import ClimbSystem
from subsystems.hatchsystem import HatchSystem

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        print("[Robot] Initializing")
        logging.basicConfig(level=logging.DEBUG)

        print("[Robot] Starting network tables server")
        NetworkTables.initialize()

        print("[Robot] Setting up systems")
        self.drivetrain = DriveTrain(self)
        self.hatchsystem = HatchSystem(self)
        self.climbsystem = ClimbSystem(self)

        self.oi = OI(self)

        # setup autonomous type
        print("[Robot] Setting up autonomous")
        scAutonomousType = wpilib.SendableChooser()
        scAutonomousType.setDefaultOption("1. Driver Controlled", 100)
        scAutonomousType.addOption       ("2. Timed Just Drive Forward", 200)
        scAutonomousType.addOption       ("3. Motion Profile Just Drive Forward", 300)
        scAutonomousType.addOption       ("4. Total Autonomous", 400)
        wpilib.SmartDashboard.putData    ("Anonomous Type", scAutonomousType)   

        # setup robot positions
        scRobotPosition = wpilib.SendableChooser()
        scRobotPosition.setDefaultOption("1. Upper Left" , 1)
        scRobotPosition.addOption       ("2. Lower Left" , 2)
        scRobotPosition.addOption       ("3. Centre"     , 3)
        scRobotPosition.addOption       ("4. Upper Right", 4)
        scRobotPosition.addOption       ("5. Lower Right", 5)
        wpilib.SmartDashboard.putData   ("Robot Position", scRobotPosition)

        # setup hatch positions
        scHatchPosition = wpilib.SendableChooser()
        scHatchPosition.setDefaultOption("1. Back"       , 10)
        scHatchPosition.addOption       ("2. Middle"     , 20)
        scHatchPosition.addOption       ("3. Front"      , 30)
        wpilib.SmartDashboard.putData   ("Hatch Position", scHatchPosition)

        # wpilib.CameraServer.launch("d:\\jet\\projects\\python\\RobotPy\\src\\vision.py:main")
        # wpilib.SmartDashboard.putData(self.drivetrain)
        wpilib.SmartDashboard.putNumber("H-Lower", 0)
        wpilib.SmartDashboard.putNumber("H-Upper", 180)
        wpilib.SmartDashboard.putNumber("S-Lower", 0)
        wpilib.SmartDashboard.putNumber("S-Upper", 255)
        wpilib.SmartDashboard.putNumber("V-Lower", 0)
        wpilib.SmartDashboard.putNumber("V-Upper", 255)

        # add HSV bounds to dashboard

    def teleopInit(self):
        return super().teleopInit()

    def teleopPeriodic(self):
        Scheduler.getInstance().run()

    def log(self):
        self.drivetrain.log()

if __name__ == "__main__":
    wpilib.run(MyRobot)