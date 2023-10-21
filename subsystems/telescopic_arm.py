from rev import CANSparkMax, RelativeEncoder, CANSparkMaxLowLevel
from wpilib import DutyCycleEncoder, XboxController, SmartDashboard
from commands2 import SubsystemBase
from constants import ElevatorConstants


class TelescopicArm(SubsystemBase):
    pivot_encoder_1 = DutyCycleEncoder(0)
    # pivot_encoder_2 = DutyCycleEncoder(6)
    controller = XboxController(3)

    pivot_motor_1 = CANSparkMax(
        ElevatorConstants.pivot_motor_id_1, CANSparkMaxLowLevel.MotorType.kBrushless
    )
    pivot_motor_2 = CANSparkMax(
        ElevatorConstants.pivot_motor_id_2, CANSparkMaxLowLevel.MotorType.kBrushless
    )
    extend_motor = CANSparkMax(
        ElevatorConstants.extend_motor_id, CANSparkMaxLowLevel.MotorType.kBrushless
    )

    extend_encoder = extend_motor.getEncoder()

    def __init__(self) -> None:
        self.config_extend_motor()
        self.config_pivot_motors()
        SmartDashboard.putBoolean("No Limit", False)

    def periodic(self) -> None:
        if SmartDashboard.getBoolean("Zero Pivot", True):
            SmartDashboard.getBoolean("Zero Pivot", False)
            self.zero_pivot()
        if SmartDashboard.getBoolean("Zero Arm", True):
            SmartDashboard.putBoolean("Zero Arm", False)
            self.zero_extend()
        self.extend_arm_speed(self.controller.getLeftY())
        self.pivot_arm_speed(self.controller.getRightY())

    # Configs

    def config_extend_motor(self) -> None:
        self.extend_motor.setInverted(False)
        self.extend_motor.restoreFactoryDefaults()
        self.extend_motor.setSmartCurrentLimit(40)
        self.extend_motor.setIdleMode(CANSparkMax.IdleMode.kBrake)

    def config_pivot_motors(self) -> None:
        self.pivot_motor_1.setInverted(False)
        self.pivot_motor_1.setIdleMode(CANSparkMax.IdleMode.kBrake)
        self.pivot_motor_1.restoreFactoryDefaults()
        self.pivot_motor_1.setSmartCurrentLimit(40)

        self.pivot_motor_2.setInverted(False)
        self.pivot_motor_2.setIdleMode(CANSparkMax.IdleMode.kBrake)
        self.pivot_motor_2.restoreFactoryDefaults()
        self.pivot_motor_2.setSmartCurrentLimit(40)

    def config_pivot_encoders(self) -> None:
        self.pivot_encoder_1.setPositionOffset(0.16)

    # Resets
    def zero_pivot(self) -> None:
        self.pivot_encoder_1.reset()

    def zero_extend(self) -> None:
        self.extend_encoder.setPosition(0.0)

    def extend_arm_speed(self, speed: float):
        self.extend_motor.set(speed)

    def pivot_arm_speed(self, speed: float):
        if abs(speed) <= 0.1:
            speed = 0
        self.pivot_motor_1(speed)
        self.pivot_motor_2(speed)

    # Move To X
    def extend_to_tick(self, ticks: float, max_speed: float):
        if self.get_extend_encoder() < (ticks - 0.2):
            self.extend_arm_speed(max_speed)
        elif (
            self.get_extend_encoder() > (ticks - 0.2)
            and self.get_extend_encoder() < ticks
        ):
            self.extend_arm_speed(0.2)
        elif self.get_extend_encoder() > ticks + 0.2:
            self.extend_arm_speed(-max_speed)
        elif (
            self.get_extend_encoder() < ticks + 0.2
            and self.get_extend_encoder() > ticks
        ):
            self.extend_arm_speed(-0.2)

    def pivot_to_tick(self, ticks: float, maxSpeed: float):
        if self.get_pivot_encoder() < ticks - 0.008:
            self.pivot_arm_speed(-maxSpeed)
        elif (
            self.get_pivot_encoder() > ticks - 0.008
            and self.get_pivot_encoder() < ticks
        ):
            self.pivot_arm_speed(-0.1)
        elif self.get_pivot_encoder() > ticks + 0.008:
            self.pivot_arm_speed(maxSpeed)
        elif self.get_pivot_encoder() < ticks + 0.008:
            self.pivot_arm_speed(0.1)

    # Geters
    def get_extend_encoder(self) -> float:
        return self.extend_encoder.getPosition()

    def get_pivot_encoder(self) -> float:
        return self.pivot_encoder_1.getAbsolutePosition()

    # Stop
    def stop_pivot(self) -> None:
        self.pivot_motor_1.set(0)
        self.pivot_motor_2.set(0)

    def stop_extending(self) -> None:
        self.extend_motor.set(0)
