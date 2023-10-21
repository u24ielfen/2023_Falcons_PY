from commands2 import CommandBase
from subsystems.telescopic_arm import TelescopicArm


class ExtendCommand(CommandBase):
    def __init__(self, ticks, maxSpeed, m_Arm) -> None:
        super().__init__()
        self.ticks = ticks
        self.m_Arm = m_Arm
        self.maxSpeed = maxSpeed

    def execute(self) -> None:
        self.m_Arm.winchToBam(self.ticks, self.maxSpeed)

    def isFinished(self) -> None:
        return abs(self.m_Arm.getWinchEncoder() - self.ticks) < 1
