from wpilib import XboxController
import commands2
import commands2.button
from constants import ButtonMappings
from subsystems.intake import Intake
from subsystems.telescopic_arm import TelescopicArm
from swerve.swerve import Swerve
from commands.teleop_swerve import TeleopSwerve
from commands2 import button
from commands.auto.commands.auto_chooser import AutoChooser


class RobotContainer:
    def __init__(self) -> None:
        self.driver_controller = XboxController(1)
        self.co_driver_controller = XboxController(3)
        self.intake = Intake()
        self.swerve = Swerve()
        self.telescopic_arm = TelescopicArm()
        self.swerve.setDefaultCommand(
            TeleopSwerve(
                self.swerve,
                self.driver_controller,
                self.driver_controller.getLeftBumper(),
            )
        )
        self.auto_chooser = AutoChooser(self.telescopic_arm, self.intake, self.swerve)
        self.configure_button_bindings()

    def configure_button_bindings(self) -> None:
        button.JoystickButton(self.driver_controller, ButtonMappings.A).onTrue(
            commands2.RunCommand(self.swerve.reset_gyro).andThen(
                commands2.RunCommand(lambda: self.swerve.reset_chassis_pos())
            )
        )

    def get_autonomous_command(self) -> commands2.Command:
        self.auto_chooser.get_chooser_option()
