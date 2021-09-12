import logging
import subprocess

LOGGER: logging.Logger = logging.getLogger(__name__)


def bash(bash_str: str) -> str:
    """Run the bash command and return the result"""
    bash_output: str = subprocess.Popen(bash_str, stdout=subprocess.PIPE, shell=True).communicate()[0].decode()
    LOGGER.debug("bash:{} output:{}".format(bash_str, bash_output))
    return bash_output
