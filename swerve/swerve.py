import wpilib
from wpilib import SmartDashboard
from wpilib import Field2d
from commands2 import SubsystemBase
import navx
from swerve.swerve_module import SwerveModule
import constants
from wpimath.estimator import SwerveDrive4PoseEstimator
import commands2
from constants import SwerveConstants
from wpimath.geometry import Rotation2d, Translation2d, Pose2d
from wpimath.kinematics import (
    SwerveModulePosition,
    ChassisSpeeds,
    SwerveDrive4Kinematics,
    SwerveModuleState,
)


class Swerve(SubsystemBase):
    gyro = navx.AHRS.create_spi()
    field = Field2d()

    def __init__(self, robot):
        self.swerve_mods = [
            [SwerveModule(0, constants.Mod0)],
            [SwerveModule(1, constants.Mod1)],
            [SwerveModule(2, constants.Mod2)],
            [SwerveModule(0, constants.Mod3)],
        ]

        self.odometry = SwerveDrive4PoseEstimator(
            SwerveConstants.kinematics,
            self.get_gyro_angle(),
            self.get_module_positions(),
        )

    def periodic(self) -> None:
        self.odometry.update(self.get_gyro_angle(), self.get_module_positions())
        self.field.setRobotPose(self.get_pose())
        SmartDashboard.putNumber("Gyro Disp. X", self.gyro.getDisplacementX())
        SmartDashboard.putNumber("Gyro Disp. Y", self.gyro.getDisplacementY())
        if SmartDashboard.getBoolean("Zero Gyro", True):
            SmartDashboard.putBoolean("Zero Gyro", False)
            self.reset_gyro
            self.reset_chassis_pos

    def drive(
        self,
        translation: Translation2d,
        rotation: float,
        fieldRelative: bool,
        is_open_loop: bool,
    ):
        if fieldRelative:
            swerve_module_states = ChassisSpeeds.fromFieldRelativeSpeeds(
                translation.Y(), translation.X(), rotation, self.get_gyro_angle()
            )
        else:
            swerve_module_states = ChassisSpeeds(
                translation.getY(), translation.getX(), rotation
            )
        SwerveDrive4Kinematics.desaturateWheelSpeeds(
            swerve_module_states, SwerveConstants.swerve_max_speed
        )
        for idx, module in enumerate(self.swerve_mods):
            module.set_desired_state(swerve_module_states[idx], is_open_loop)

    def move_by_chassis_speeds(self, speed: ChassisSpeeds) -> None:
        swerve_module_states = SwerveConstants.kinematics.toSwerveModuleStates(
            ChassisSpeeds.fromFieldRelativeSpeeds(speed, self.get_gyro_angle())
        )
        self.set_module_states(swerve_module_states)

    def set_module_states(self, desired_state: SwerveModuleState) -> None:
        SwerveDrive4Kinematics.desaturateWheelSpeeds(
            desired_state, SwerveConstants.swerve_max_speed
        )
        for idx, module in enumerate(self.swerve_mods):
            module.set_desired_state(desired_state[idx], False)

    # Geters
    def get_gyro_angle(self) -> Rotation2d:
        return Rotation2d.fromDegrees(360 - self.gyro.getYaw)

    def get_module_positions(self) -> tuple:
        return tuple([module.getPosition() for module in self.swerve_mods])

    def get_pose(self):
        return self.odometry.getEstimatedPosition()

    # Resets
    def reset_gyro(self) -> None:
        self.gyro.reset()
        self.gyro.resetDisplacement()

    def reset_chassis_pos_to_pose(self, pose: Pose2d) -> None:
        self.odometry.resetPosition(
            self.get_gyro_angle(), self.get_module_positions(), pose
        )

    def reset_modules(self) -> None:
        for module in self.swerve_mods:
            module.reset_module()

    def reset_chassis_pos(self) -> None:
        self.reset_gyro()
        self.odometry.resetPosition(
            self.get_gyro_angle(),
            self.get_module_positions(),
            Pose2d(self.get_pose().translation(), Rotation2d(0, 0)),
        )

    def stop(self) -> None:
        self.move_by_chassis_speeds(ChassisSpeeds(0, 0, 0))
        # TODO: See if this works ^
