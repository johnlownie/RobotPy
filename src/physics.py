#
# See the notes for the other physics sample
#


from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units


class PhysicsEngine(object):
    """
       Simulates a 4-wheel robot using Tank Drive joystick control
    """

    def __init__(self, physics_controller):
        """
            :param physics_controller: `pyfrc.physics.core.Physics` object
                                       to communicate simulation effects to
        """

        self.physics_controller = physics_controller
        self.position = 0

        self.physics_controller.add_device_gyro_channel("navxmxp_spi_4_angle")

        # Change these parameters to fit your robot!
        bumper_width = 3.25 * units.inch

        # fmt: off
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_CIM,           # motor configuration
            110 * units.lbs,                    # robot mass
            10.71,                              # drivetrain gear ratio
            2,                                  # motors per side
            22 * units.inch,                    # robot wheelbase
            23 * units.inch + bumper_width * 2, # robot width
            32 * units.inch + bumper_width * 2, # robot length
            6 * units.inch,                     # wheel diameter
        )
        # fmt: on

    def update_sim(self, hal_data, now, tm_diff):
        """
            Called when the simulation parameters for the program need to be
            updated.
            
            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        """

        # Simulate the drivetrain
        # lr_motor = hal_data["pwm"][1]["value"]
        # rr_motor = hal_data["pwm"][2]["value"]

        # Not needed because front and rear should be in sync
        # lf_motor = hal_data['pwm'][3]['value']
        # rf_motor = hal_data['pwm'][4]['value']

        lf_motor = hal_data["CAN"][1]
        rf_motor = hal_data["CAN"][3]

        lr_motor = hal_data["CAN"][2]
        rr_motor = hal_data["CAN"][4]

        left_front_speed = int(4096 * 4 * lf_motor["value"] * tm_diff)
        lf_motor["quad_position"] += left_front_speed
        lf_motor["quad_velocity"] = left_front_speed

        left_rear_speed = int(4096 * 4 * lr_motor["value"] * tm_diff)
        lr_motor["quad_position"] += left_rear_speed
        lr_motor["quad_velocity"] = left_rear_speed

        right_front_speed = int(4096 * 4 * rf_motor["value"] * tm_diff)
        rf_motor["quad_position"] += right_front_speed
        rf_motor["quad_velocity"] = right_front_speed

        right_rear_speed = int(4096 * 4 * rr_motor["value"] * tm_diff)
        rr_motor["quad_position"] += right_rear_speed
        rr_motor["quad_velocity"] = right_rear_speed

        x, y, angle = self.drivetrain.get_distance(lf_motor["value"], rf_motor["value"], tm_diff)
        self.physics_controller.distance_drive(x, y, angle)