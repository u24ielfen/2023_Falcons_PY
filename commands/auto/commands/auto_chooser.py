from commands2 import CommandBase
from wpilib import SmartDashboard
from subsystems.telescopic_arm import TelescopicArm
from subsystems.intake import Intake
from swerve.swerve import Swerve
from wpilib import SendableChooser
from commands.auto.actions.cone.top_cone import TopCone
from commands.auto.actions.cube.top_cube import TopCube
from commands.auto.actions.cone.mid_cone import MidCone
from commands.auto.actions.cube.mid_cube import MidCube
from commands.auto.actions.cone.low_cone import LowCone
from commands.auto.actions.cube.low_cube import LowCube
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

        self.chooser.addOption("NO AUTO", WaitCommand(15))
        self.chooser.addOption("Top Cone", TopCone(arm, intake, swerve, 0))
        self.chooser.addOption("Mid Cone", MidCone(arm, intake, swerve, 0))
        self.chooser.addOption("Low Cone", LowCone(arm, intake, swerve, 0))
        self.chooser.addOption("Top Cube", TopCube(arm, intake, swerve, 0))
        self.chooser.addOption("Mid Cube", MidCube(arm, intake, swerve, 0))
        self.chooser.addOption("Low Cube", LowCube(arm, intake, swerve, 0))
        self.chooser.addOption("Top Cone CHARGE", TopCone(arm, intake, swerve, 3))
        self.chooser.addOption("Mid Cone CHARGE", MidCone(arm, intake, swerve, 3))
        self.chooser.addOption("Low Cone CHARGE", LowCone(arm, intake, swerve, 3))
        self.chooser.addOption("Top Cube CHARGE", TopCube(arm, intake, swerve, 3))
        self.chooser.addOption("Mid Cube CHARGE", MidCube(arm, intake, swerve, 3))
        self.chooser.addOption("Low Cube CHARGE", LowCube(arm, intake, swerve, 3))
        self.chooser.addOption("Top Cone FAR", TopCone(arm, intake, swerve, 4.3))
        self.chooser.addOption("Mid Cone FAR", MidCone(arm, intake, swerve, 4.3))
        self.chooser.addOption("Low Cone FAR", LowCone(arm, intake, swerve, 4.3))
        self.chooser.addOption("Top Cube FAR", TopCube(arm, intake, swerve, 4.3))
        self.chooser.addOption("Mid Cube FAR", MidCube(arm, intake, swerve, 4.3))
        self.chooser.addOption("Low Cube FAR", LowCube(arm, intake, swerve, 4.3))

    def get_chooser_option(self) -> SendableChooser:
        return self.chooser.getSelected()
