import wpilib


class SwerveModuleConstants:
    driveMotorID: int
    angleMotorID: int
    cancoderID: int
    angleOffset: float

    def __init__(
        self, driveMotor: int, angleMotorID: int, cancoderID: int, angleOffset: float
    ) -> None:
        self.driveMotorID = driveMotor
        self.angleMotorID = angleMotorID
        self.cancoderID = cancoderID
        self.angleOffset = angleOffset
