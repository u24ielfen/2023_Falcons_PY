from commands2 import CommandBase
from wpilib import SmartDashboard
from subsystems.telescopic_arm import TelescopicArm
from subsystems.intake import Intake
from swerve.swerve import Swerve
from wpilib import SendableChooser
from auto.actions.cone.top_cone import TopCone
from auto.actions.cube.top_cube import TopCube
from auto.actions.cone.mid_cone import MidCone
from auto.actions.cube.mid_cube import MidCube
from auto.actions.cone.low_cone import LowCone
from auto.actions.cube.low_cube import LowCube
from commands2 import WaitCommand


class AutoChooser(CommandBase):
    def __init__(self, arm: TelescopicArm, intake: Intake, swerve: Swerve) -> None:
        super().__init__()
        self.swerve = swerve
        self.arm = arm
        self.intake = intake
        self.addRequirements(arm, intake, swerve)
        self.distance = 2.7
        self.chooser = SendableChooser()

        manualOptions = [
            ("NO AUTO", WaitCommand(15)),
            ("Top Cone", TopCone(arm, intake, swerve, 0)),
            ("Mid Cone", MidCone(arm, intake, swerve, 0)),
            ("Low Cone", LowCone(arm, intake, swerve, 0)),
            ("Top Cube", TopCube(arm, intake, swerve, 0)),
            ("Mid Cube", MidCube(arm, intake, swerve, 0)),
            ("Low Cube", LowCube(arm, intake, swerve, 0)),
            ("Top Cone CHARGE", TopCone(arm, intake, swerve, 3)),
            ("Mid Cone CHARGE", MidCone(arm, intake, swerve, 3)),
            ("Low Cone CHARGE", LowCone(arm, intake, swerve, 3)),
            ("Top Cube CHARGE", TopCube(arm, intake, swerve, 3)),
            ("Mid Cube CHARGE", MidCube(arm, intake, swerve, 3)),
            ("Low Cube CHARGE", LowCube(arm, intake, swerve, 3)),
            ("Top Cone FAR", TopCone(arm, intake, swerve, 4.3)),
            ("Mid Cone FAR", MidCone(arm, intake, swerve, 4.3)),
            ("Low Cone FAR", LowCone(arm, intake, swerve, 4.3)),
            ("Top Cube FAR", TopCube(arm, intake, swerve, 4.3)),
            ("Mid Cube FAR", MidCube(arm, intake, swerve, 4.3)),
            ("Low Cube FAR", LowCube(arm, intake, swerve, 4.3)),
        ]

        for option in self.chooser:
            self.chooser.addOption(option[0], option[1])

    def get_chooser_option(self) -> SendableChooser:
        return self.chooser.getSelected()
