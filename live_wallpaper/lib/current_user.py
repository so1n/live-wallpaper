import getpass
import os
import pwd


def get_current_user() -> str:
    """get user from current processor"""
    try:
        # pwd is unix only
        return pwd.getpwuid(os.getuid())[0]
    except ImportError:
        return getpass.getuser()
