from commands2 import CommandBase
from wpilib import SmartDashboard
from subsystems.telescopic_arm import TelescopicArm


class PivotCommand(CommandBase):
    def __init__(self, ticks: float, maxSpeed: float, arm: TelescopicArm):
        super().__init__()
        self.ticks = ticks
        self.maxSpeed = maxSpeed
        self.arm = arm
        self.addRequirements(arm)

    def execute(self):
        self.arm.pivotToBam(self.ticks, self.maxSpeed)

    def end(self, interrupted):
        self.arm.stopPivot()

    def isFinished(self):
        return abs(self.arm.getPivotEncoder() - self.ticks) < 0.007
