from commands2 import CommandBase
from swerve.swerve import Swerve
from wpilib import Timer
from wpimath.geometry import Translation2d


class DriveXTime(CommandBase):
    def __init__(self, swerve: Swerve, time: float, direction: str) -> None:
        super().__init__()
        self.swerve = swerve
        self.time = time
        self.direction = direction
        self.addRequirements(swerve)

    def initialize(self) -> None:
        self.initial_pos = self.swerve.get_pose().Y()
        self.initial_time = Timer.getFPGATimestamp()

    def execute(self) -> None:
        self.time_now = Timer.getFPGATimestamp()
        if self.direction == "Forward":
            self.swerve.drive(Translation2d(0, 0.3), 0, True, True)
        elif self.direction == "Backwards":
            self.swerve.drive(Translation2d(0, -0.3, 0, True, True))

    def end(self, interrupted: bool) -> None:
        self.swerve.stop()

    def isFinished(self) -> bool:
        return self.time_now - self.initial_time > self.time
