import logging
import os
import shutil
import subprocess
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union

from little_cheesemonger._errors import LittleCheesemongerError
from little_cheesemonger._loader import get_platform


LOGGER = logging.getLogger(__name__)


def run(configuration: dict):
    
    platform = get_platform()
    
    # _set_environment_variables
    # _install_python_dependencies
    # _install_system_dependencies
    # _build_wheel
