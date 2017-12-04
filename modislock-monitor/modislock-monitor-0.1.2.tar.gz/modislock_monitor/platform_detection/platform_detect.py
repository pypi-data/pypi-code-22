
import platform
import re

# Platform identification constants.
UNKNOWN = 0
RASPBERRY_PI = 1
BEAGLEBONE_BLACK = 2

isBeagleBoneBlack = False
isRaspberryPi = False


def platform_detect():
    """Detect if running on the Raspberry Pi or Beaglebone Black

    Will return RASPBERRY_PI, BEAGLEBONE_BLACK, or UNKNOWN.

    :returns: RASBERRY_PI, BEAGLEBONE_BLACK, UNKNOWN

    """
    # Handle Raspberry Pi
    pi = pi_version()

    if pi is not None:
        return RASPBERRY_PI

    # Handle Beaglebone Black
    # TODO: Check the Beaglebone Black /proc/cpuinfo value instead of reading
    # the platform.
    plat = platform.platform()

    if plat.lower().find('armv7l-with-debian') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-ubuntu') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-glibc2.4') > -1:
        return BEAGLEBONE_BLACK

    # Couldn't figure out the platform, just return unknown.
    return UNKNOWN


def pi_revision():
    """Detect the revision number

    Useful for changing functionality like default I2C bus based on revision.

    :returns: cpu type

    """
    # Revision list available at: http://elinux.org/RPi_HardwareHistory#Board_Revision_History
    with open('/proc/cpuinfo', 'r') as infile:
        for line in infile:
            # Match a line of the form "Revision : 0002" while ignoring extra
            # info in front of the revsion (like 1000 when the Pi was over-volted).
            match = re.match('Revision\s+:\s+.*(\w{4})$', line, flags=re.IGNORECASE)
            if match and match.group(1) in ['0000', '0002', '0003']:
                # Return revision 1 if revision ends with 0000, 0002 or 0003.
                return 1
            elif match:
                # Assume revision 2 if revision ends with any other 4 chars.
                return 2
        # Couldn't find the revision, throw an exception.
        raise RuntimeError('Could not determine Raspberry Pi revision.')


def pi_version():
    """Detect the version of the Raspberry Pi.

    Returns either 1, 2 or
    None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
    Raspberry Pi 2 (model B+), or not a Raspberry Pi.

    Check /proc/cpuinfo for the Hardware field value.
    2708 is pi 1
    2709 is pi 2
    Anything else is not a pi.
    cpuinfo = ''

    :returns: version number

    """
    try:
        with open('/proc/cpuinfo', 'r') as infile:
            cpuinfo = infile.read()
    except FileNotFoundError:
        return None
    # Match a line like 'Hardware   : BCM2709'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo, flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        # Couldn't find the hardware, assume it isn't a pi.
        return None
    if match.group(1) == 'BCM2708':
        # Pi 1
        return 1
    elif match.group(1) == 'BCM2709':
        # Pi 2
        return 2
    elif match.group(1) == "BCM2835":
        # Pi 3
        return 1
    elif match.group(1) == "BCM2836":
        # Pi 2
        return 2
    elif match.group(1) == "BCM2837":
        # Pi 3
        return 3
    else:
        # Something else, not a pi.
        return None


is_platform = platform_detect()
isBeagleBoneBlack = is_platform == BEAGLEBONE_BLACK
isRaspberryPi = is_platform == RASPBERRY_PI
