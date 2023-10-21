from commands2 import CommandBase
from swerve.swerve import Swerve
from wpilib import XboxController, SmartDashboard
from wpimath.geometry import Translation2d


class TeleopSwerve(CommandBase):
    def __init__(
        self, swerve: Swerve, controller: XboxController, field_relative: bool
    ):
        super().__init__()

        self.swerve = swerve
        self.controller = controller
        self.field_relative = field_relative
        self.addRequirements(swerve)

    def execute(self) -> None:
        if self.field_relative:
            SmartDashboard.putBoolean("Field Relative", True)
        else:
            SmartDashboard.putBoolean("Field Relative", False)
        self.yAxis = -self.controller.getLeftY()
        self.xAxis = -self.controller.getLeftX()
        self.rAxis = -self.controller.getRightX()
        # TODO: Make controls better: https://github.com/CtrlZ-FRC4096/Robot-2023-Public/blob/d27d9ec620a521f5b9575ca9b4bec8e30b3b229c/robot/oi.py#L77

        self.translation = Translation2d(self.xAxis, self.yAxis)
        self.swerve.drive(self.translation, self.rotation, self.field_relative)
