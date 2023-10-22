def falcon_to_degress(counts: float, gearRatio: float) -> float:
    return counts * (360.0 / (gearRatio * 2048.0))


def degrees_to_falcon(degrees: float, gearRatio: float) -> float:
    return degrees / (360.0 / (gearRatio * 2048.0))


def falcon_to_rpm(velocityCounts: float, gearRatio: float) -> float:
    motorRPM = velocityCounts * (600 / 2048.0)
    return motorRPM / gearRatio


def rpm_to_falcon(RPM: float, gearRatio: float) -> float:
    motorRPM = RPM


def falcon_to_mps(
    velocityCounts: float, circumference: float, gearRatio: float
) -> float:
    wheelRPM = falcon_to_rpm(velocityCounts, gearRatio)
    return (wheelRPM * circumference) / 60


def mps_to_falcon(velocity: float, circumference: float, gearRatio: float) -> float:
    wheelRPM = (velocity * 60) / circumference
    return rpm_to_falcon(wheelRPM, gearRatio)


def falcon_to_meters(
    falconTicks: float, circumference: float, gearRatio: float
) -> float:
    wheelRevs = falconTicks / (gearRatio * 2048)
    return wheelRevs * circumference
