import wpilib
import wpilib.drive
from robotcontainer import RobotContainer
import commands2


class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self):
        self.container = RobotContainer()

    # def disabledInit(self):
    # def disabledPeriodic(self) -> None:

    def autonomousInit(self):
        self.auto_command = self.container.get_autonomous_command()
        if self.auto_command:
            self.auto_command.schedule()

    # def autonomousPeriodic(self) -> None:
    def teleopInit(self) -> None:
        if self.auto_command:
            self.auto_command.cancel()

    def teleopPeriodic(self):
        self.drive.arcadeDrive(self.stick.getY(), self.stick.getX())


if __name__ == "__main__":
    wpilib.run(MyRobot)
