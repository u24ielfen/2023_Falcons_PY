from commands2 import CommandBase
from subsystems.intake import Intake


class ChinCommand(CommandBase):
    def __init__(self, ticks, m_Intake):
        super().__init__()
        self.ticks = ticks
        self.m_Intake = m_Intake
        self.addRequirements(m_Intake)

    def initialize(self) -> None:
        self.startingPos = self.m_Intake.getChinEncoder()

    def execute(self) -> None:
        self.m_Intake.chinTicksToBam(self.ticks)

    def isFinished(self):
        return abs(self.m_Intake.getChinEncoder() - self.ticks) < 0.2
