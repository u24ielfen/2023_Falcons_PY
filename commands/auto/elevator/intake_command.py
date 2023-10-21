from commands2 import CommandBase
from wpilib import Timer, SmartDashboard
from subsystems.intake import Intake


class IntakeCommand(CommandBase):
    def __init__(self, intake: Intake, inOut: str, time: float):
        super().__init__()
        self.intake = intake
        self.inOut = inOut
        self.time = time
        self.startingTime = 0

        self.addRequirements(intake)

    def initialize(self):
        self.startingTime = Timer.getFPGATimestamp()

    def execute(self):
        if self.inOut == "In":
            self.intake.moveSpinMotor(0.8)
        elif self.inOut == "Out":
            self.intake.moveSpinMotor(-1)

    def end(self, interrupted):
        self.intake.stopSpinMotor()

    def isFinished(self):
        if self.inOut == "Out":
            return Timer.getFPGATimestamp() - self.startingTime > self.time
        elif self.inOut == "In":
            return SmartDashboard.getBoolean("Limit Switch", False)
        return False
