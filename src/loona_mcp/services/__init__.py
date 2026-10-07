"""Hardware reverse engineering service - ADB bridge, protocol decoders."""


class ADBBridge:
    """Bridge to ADB for Loona's Android OS.

    Only active if LOONA_ADB_PATH is configured and device is connected.
    """

    def __init__(self, adb_path: str = "adb"):
        self.adb_path = adb_path = adb_path

    @property
    def available(self) -> bool:
        return False  # placeholder - check subprocess call to adb devices


class MotorController:
    """Abstract motor controller interface.

    Will be backed by:
    - Phase 1: ADB shell commands to /sys/class/pwm or /dev/i2c
    - Phase 3: RPi GPIO/I2C/PWM via RPi.GPIO or pigpio
    """

    pass
