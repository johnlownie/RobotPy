import wpilib

from wpilib import SmartDashboard
from wpilib.buttons import JoystickButton

from commands.actions.align_by_camera import AlignByCamera
from commands.actions.deploy_hatch import DeployHatch
from commands.actions.drop_cargo import DropCargo
from commands.actions.toggle_compressor import ToggleCompressor
from commands.actions.toggle_led import ToggleLED
from commands.actions.turn_by_gyro import TurnByGyro

class OI(object):
    # set constants
    XBOX_DEADZONE_LEFT_JOY = 0.1
    XBOX_DEADZONE_RIGHT_JOY = 0.1
    DRIVEWITHJOYSTICK_ROTATION_LIMITER = 0.95

    def __init__(self, robot):
        # driver mappings
        self.driver_joystick = wpilib.XboxController(0)

        JoystickButton(self.driver_joystick, wpilib.XboxController.Button.kX).whenPressed(TurnByGyro(robot, -90.0))
        JoystickButton(self.driver_joystick, wpilib.XboxController.Button.kY).whenPressed(TurnByGyro(robot,  90.0))
        
        JoystickButton(self.driver_joystick, wpilib.XboxController.Button.kStart).whenPressed(ToggleCompressor(robot))
        
        # operator mappings
        self.operator_joystick = wpilib.XboxController(1)

        JoystickButton(self.operator_joystick, wpilib.XboxController.Button.kA).whenPressed(DeployHatch(robot))
        JoystickButton(self.operator_joystick, wpilib.XboxController.Button.kB).whenPressed(DropCargo(robot))

        JoystickButton(self.operator_joystick, wpilib.XboxController.Button.kY).whenPressed(ToggleLED(robot))
        JoystickButton(self.operator_joystick, wpilib.XboxController.Button.kY).whileHeld(AlignByCamera(robot))
        JoystickButton(self.operator_joystick, wpilib.XboxController.Button.kY).whenReleased(ToggleLED(robot))

        JoystickButton(self.operator_joystick, wpilib.XboxController.Button.kStart).whenPressed(ToggleCompressor(robot))

    def getJoystickDriver(self):
        return self.driver_joystick

    def getJoystickOperator(self):
        return self.operator_joystick
