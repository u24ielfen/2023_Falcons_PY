from subsystems.telescopic_arm import TelescopicArm
from subsystems.intake import Intake
from swerve.swerve import Swerve
from commands.auto.elevator.chin_command import ChinCommand
from commands.auto.elevator.extend_command import ExtendCommand
from commands.auto.elevator.intake_command import IntakeCommand
from commands.auto.elevator.pivot_command import PivotCommand
from commands2 import CommandBase
import commands2
from commands.auto.actions.drive_x_time import DriveXTime


class MidCone(CommandBase):
    def __init__(
        self, arm: TelescopicArm, intake: Intake, swerve: Swerve, time: float
    ) -> None:
        super().__init__()
        self.arm = arm
        self.swerve = swerve
        self.intake = intake
        self.time = time
        self.addRequirements(arm, intake, swerve)

    def execute(self) -> None:
        self.get_command().schedule()

    def get_command(self) -> commands2.Command:
        commands2.SequentialCommandGroup(
            PivotCommand(0.201, 0.5, self.arm).andThen(
                ExtendCommand(-63.9, 0.6, self.arm).andThen(
                    IntakeCommand(self.intake, "Out", 2.5).andThen(
                        ExtendCommand(-4, 0.6, self.arm).andThen(
                            DriveXTime(self.swerve, self.time, "Forward")
                        )
                    )
                )
            )
        )

    def isFinished(self) -> bool:
        return False
