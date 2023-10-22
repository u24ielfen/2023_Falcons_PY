import wpilib
from wpimath.controller import SimpleMotorFeedforwardMeters
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModulePosition, SwerveModuleState
from robot import MyRobot
import ctre
from ctre.sensors import (
    CANCoder,
    CANCoderConfiguration,
    SensorInitializationStrategy,
    SensorTimeBase,
)
from ctre import (
    TalonFX,
    ControlMode,
    SupplyCurrentLimitConfiguration,
    TalonFXConfiguration,
    DemandType,
    NeutralMode,
)
import typing
import math
from constants import SwerveConstants
from lib.util.swerve_module_constants import SwerveModuleConstants
from lib.util import ctre_module_states
from lib.math import conversions


class SwerveModule:
    module_number: int
    angle_offset: float
    angle_motor: ctre.TalonFX
    drive_motor: ctre.TalonFX
    angle_encoder: CANCoder
    last_angle: float

    def __init__(
        self, module_number: int, moduleConstants: SwerveModuleConstants
    ) -> None:
        self.feedforward = SimpleMotorFeedforwardMeters(
            SwerveConstants.drivekS, SwerveConstants.drivekV, SwerveConstants.drivekA
        )
        self.module_number = module_number
        self.angle_motor = TalonFX(moduleConstants.angleMotorID)
        self.drive_motor = TalonFX(moduleConstants.driveMotorID)
        self.angle_encoder = CANCoder(moduleConstants.canCoderId, "carnivore")
        self.angle_offset = moduleConstants.angleOffset
        self.config_angle_encoder()

        self.last_angle = self.get_state().angle.degrees()

    def set_desired_state(
        self, desired_state: SwerveModuleState, is_open_loop: bool
    ) -> None:
        self.invert_motors()
        desired_state = ctre_module_states.optimize(
            desired_state, self.get_can_coder_rotation2D()
        )
        self.set_speed(desired_state, is_open_loop)
        self.set_angle(desired_state)

    def set_speed(self, desired_state: SwerveModuleState, is_open_loop: bool) -> None:
        if is_open_loop:
            percent_output = desired_state.speed / SwerveConstants.swerve_max_speed
            self.drive_motor.set(ControlMode.PercentOutput, percent_output)
        else:
            velocity = conversions.mps_to_falcon(
                desired_state.speed,
                SwerveConstants.swerve_wheel_circumference,
                SwerveConstants.swerve_drive_gear_ratio,
            )
            self.drive_motor.set(
                ControlMode.Velocity,
                velocity,
                DemandType.ArbitraryFeedForward,
                self.feedforward.calculate(desired_state.speed),
            )

    def set_angle(self, desired_state: SwerveModuleState) -> None:
        if abs(desired_state.speed) <= SwerveConstants.swerve_max_speed * 0.01:
            angle = self.last_angle
        else:
            angle = desired_state.angle.degrees()
        self.angle_motor.set(
            ControlMode.Position,
            conversions.degrees_to_falcon(angle, SwerveConstants.angle_gear_ratio),
        )
        self.last_angle = angle

    # Configs
    def config_angle_encoder(self) -> None:
        self.angle_encoder.configFactoryDefault()
        swerve_can_coder_config = CANCoderConfiguration()
        swerve_can_coder_config.sensorDirection = False
        swerve_can_coder_config.initializationStrategy = (
            SensorInitializationStrategy.BootToAbsolutePosition
        )
        swerve_can_coder_config.sensorTimeBase = SensorTimeBase.PerSecond
        self.angle_encoder.configAllSettings(swerve_can_coder_config)

    def config_angle_motor(self) -> None:
        swerve_angle_motor_configs = TalonFXConfiguration()
        swerve_angle_motor_configs.slot0.kP = SwerveConstants.angle_kp
        swerve_angle_motor_configs.slot0.kI = SwerveConstants.angle_ki
        swerve_angle_motor_configs.slot0.kD = SwerveConstants.angle_kd
        swerve_angle_motor_configs.slot0.kF = SwerveConstants.angle_kf
        swerve_angle_motor_configs.supplyCurrLimit = SupplyCurrentLimitConfiguration(
            True, 25, 40, 0.1
        )
        self.angle_motor.configAllSettings(swerve_angle_motor_configs)

        self.angle_motor.setInverted(False)
        self.angle_motor.setNeutralMode(NeutralMode.Brake)
        self.reset_to_absolute()

    def config_drive_motor(self) -> None:
        swerve_drive_motor_configs = TalonFXConfiguration()
        swerve_drive_motor_configs.slot0.kP = SwerveConstants.drive_kp
        swerve_drive_motor_configs.slot0.kI = SwerveConstants.drive_ki
        swerve_drive_motor_configs.slot0.kD = SwerveConstants.drive_kd
        swerve_drive_motor_configs.slot0.kF = SwerveConstants.drive_kf
        swerve_drive_motor_configs.supplyCurrLimit = SupplyCurrentLimitConfiguration(
            True, 25, 40, 0.1
        )
        self.drive_motor.configAllSettings(swerve_drive_motor_configs)

    # Resets
    def reset_to_absolute(self) -> None:
        absolute_position = conversions.degrees_to_falcon(
            self.get_can_coder_rotation2D() - self.angle_offset,
            SwerveConstants.angle_gear_ratio,
        )
        self.angle_motor.setSelectedSensorPosition(absolute_position)

    def reset_module(self) -> None:
        self.angle_motor.setSelectedSensorPosition(0)

    # Geters
    def get_can_coder_rotation2D(self) -> Rotation2d:
        return Rotation2d.fromDegrees(self.angle_encoder.getAbsolutePosition())

    def get_state(self) -> SwerveModuleState:
        velocity = conversions.falcon_to_mps(
            self.drive_motor.getSelectedSensorVelocity(),
            SwerveConstants.swerve_wheel_circumference,
            SwerveConstants.swerve_drive_gear_ratio,
        )

        return SwerveModuleState(velocity, self.get_angle())

    def get_position(self) -> SwerveModulePosition:
        return SwerveModulePosition(
            conversions.falcon_to_meters(
                self.drive_motor.getSelectedSensorPosition(),
                SwerveConstants.swerve_wheel_circumference,
                SwerveConstants.angle_gear_ratio,
            ),
            self.get_angle(),
        )

    def get_angle(self) -> Rotation2d:
        return Rotation2d.fromDegrees(
            conversions.falcon_to_degress(
                self.angle_motor.getSelectedSensorPosition(),
                SwerveConstants.angle_gear_ratio,
            )
        )

    # Mode
    def invert_motors(self) -> None:
        if self.drive_motor.getDeviceID() == 2 or self.drive_motor.getDeviceID() == 4:
            self.drive_motor.setInverted(True)
        else:
            self.drive_motor.setInverted(False)
