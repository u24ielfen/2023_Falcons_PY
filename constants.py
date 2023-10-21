import wpilib
from lib.util.swerve_module_constants import SwerveModuleConstants
import math
from wpimath.kinematics import SwerveDrive4Kinematics
from wpimath.geometry import Translation2d


class Constants:
    motor = 1


class SwerveConstants:
    # Drive Motor Characterization Values
    drivekS = 0.667 / 12
    drivekV = 2.44 / 12
    drivekA = 0.27 / 12
    # Angle Motor PID Values
    angle_kp = 0.6
    angle_ki = 0.0
    angle_kd = 12.0
    angle_kf = 0.0
    # Drive Motor PID Values
    drive_kp = 0.1
    drive_ki = 0.0
    drive_kd = 0.0
    drive_kf = 0.0

    angle_gear_ratio = 12.8
    wheel_base = 0.517
    track_width = 0.517
    swerve_max_speed = 1.0
    swerve_drive_gear_ratio = 8.14
    angle_gear_ratio = 12.8
    swerve_wheel_circumference = 0.1016 * math.pi

    kinematics = SwerveDrive4Kinematics(
        Translation2d(wheel_base / 2.0, track_width / 2.0),
        Translation2d(wheel_base / 2.0, -track_width / 2.0),
        Translation2d(-wheel_base / 2.0, track_width / 2.0),
        Translation2d(-wheel_base / 2.0, -track_width / 2.0),
    )


class IntakeConstants:
    motor_id = 29
    chin_id = 28


class Mod0:
    driveMotorID = 4
    angleMotorID = 5
    canCoderId = 6
    angleOffset = 22
    constants = SwerveModuleConstants(
        driveMotorID, angleMotorID, canCoderId, angleOffset
    )


class Mod1:
    driveMotorID = 2
    angleMotorID = 1
    canCoderId = 3
    angleOffset = -8
    constants = SwerveModuleConstants(
        driveMotorID, angleMotorID, canCoderId, angleOffset
    )


class Mod2:
    driveMotorID = 7
    angleMotorID = 8
    canCoderId = 12
    angleOffset = 40.07811
    constants = SwerveModuleConstants(
        driveMotorID, angleMotorID, canCoderId, angleOffset
    )


class Mod3:
    driveMotorID = 9
    angleMotorID = 10
    canCoderId = 11
    angleOffset = -36
    constants = SwerveModuleConstants(
        driveMotorID, angleMotorID, canCoderId, angleOffset
    )


class ElevatorConstants:
    pivot_motor_id_1 = 23
    pivot_motor_id_2 = 24


class ButtonMappings:
    A = 1
    B = 2
    X = 3
    Y = 4
    LEFT_BUMPER = 5
    RIGHT_BUMPER = 6
    LOGO_LEFT = 7
    LOGO_RIGHT = 8
    LEFT_STICK_BUTTON = 9
    RIGHT_STICK_BUTTON = 10
