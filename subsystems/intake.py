import wpilib
from commands2 import SubsystemBase

from wpilib import DutyCycleEncoder, SmartDashboard, DigitalInput
from constants import IntakeConstants
from rev import CANSparkMax, CANSparkMaxLowLevel, RelativeEncoder


class Intake(SubsystemBase):
    spin_motor = CANSparkMax(
        IntakeConstants.motor_id, CANSparkMaxLowLevel.MotorType.kBrushless
    )
    chin_motor = CANSparkMax(
        IntakeConstants.chin_id, CANSparkMaxLowLevel.MotorType.kBrushless
    )
    spin_encoder = spin_motor.getEncoder()
    chin_encoder = chin_motor.getEncoder()
    limit_switch_1 = DigitalInput(1)
    limit_switch_2 = DigitalInput(5)

    def __init__(self) -> None:
        self.config_spin_motor()
        self.config_chin_motor

    def periodic(self) -> None:
        SmartDashboard.putBoolean("Limit Switch 1", self.limit_switch_1.get())
        SmartDashboard.putBoolean("Limit Switch 2", self.limit_switch_2.get())
        if SmartDashboard.getBoolean("Zero Chin", True):
            SmartDashboard.putBoolean("Zero Chin", False)
            self.reset_chin_encoder()

    # Configs
    def config_spin_motor(self) -> None:
        self.spin_motor.restoreFactoryDefaults()
        self.spin_motor.setInverted(True)
        self.spin_motor.setIdleMode(CANSparkMax.IdleMode.kBrake)

    def config_chin_motor(self) -> None:
        self.chin_motor.restoreFactoryDefaults()
        self.chin_motor.setInverted(False)
        self.chin_motor.setIdleMode(CANSparkMax.IdleMode.kBrake)

    # Resets
    def reset_chin_encoder(self) -> None:
        self.chin_encoder.setPosition(0)

    # Set
    def stop_spin_motor(self) -> None:
        self.spin_motor.set(0)

    def stop_chin_motor(self) -> None:
        self.chin_motor.set(0)

    def move_chin_motor_speed(self, speed: float) -> None:
        self.chin_motor.set(speed)

    def move_spin_motor_speed(self, speed: float) -> None:
        self.spin_motor.set(speed)

    def chin_ticks_bang(self, ticks: float) -> None:
        if ticks - self.get_chin_encoder() > 3:
            self.move_chin_motor_speed(0.5)
        elif (
            ticks - self.get_chin_encoder() > 0.2
            and ticks - self.get_chin_encoder() < 3
        ):
            self.move_chin_motor_speed(0.1)
        elif ticks - self.get_chin_encoder() < -3:
            self.move_chin_motor_speed(-0.5)
        elif (
            ticks - self.get_chin_encoder < -0.2
            and ticks - self.get_chin_encoder() > -3
        ):
            self.move_chin_motor_speed(-0.1)

    # Geters
    def get_chin_encoder(self) -> None:
        self.chin_encoder.get()
