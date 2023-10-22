import wpilib
import wpilib.drive
import robotcontainer
import commands2
from commands2 import CommandScheduler
import typing


class MyRobot(commands2.TimedCommandRobot):
    autonomousCommand: typing.Optional[commands2.Command] = None

    def robotInit(self):
        self.scheduler = commands2.CommandScheduler.getInstance()
        self.container = robotcontainer.RobotContainer()
        self.auto_command = self.container.get_autonomous_command()

    # def disabledInit(self):
    # def disabledPeriodic(self) -> None:

    def autonomousInit(self):
        if self.auto_command:
            self.auto_command.schedule()

    # def autonomousPeriodic(self) -> None:
    def teleopInit(self) -> None:
        if self.auto_command:
            self.auto_command.cancel()

    def robotPeriodic(self) -> None:
        CommandScheduler.getInstance().run()


if __name__ == "__main__":
    wpilib.run(MyRobot)
