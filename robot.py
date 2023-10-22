import wpilib
import wpilib.drive
import robotcontainer
import commands2
from commands2 import CommandScheduler


class MyRobot(commands2.TimedCommandRobot):
    def robotInit(self):
        self.container = robotcontainer.RobotContainer()

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

    def robotPeriodic(self) -> None:
        CommandScheduler.getInstance().run()


if __name__ == "__main__":
    wpilib.run(MyRobot)
