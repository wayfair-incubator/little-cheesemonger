import pytest

from little_cheesemonger._platform import get_platform
from little_cheesemonger._errors import LittleCheesemongerError

from tests.constants import PLATFORM


def os_environ(mocker):
    return mocker.patch.dict(os.environ, {"AUDITWHEEL_PLAT": PLATFORM})
    

def test_get_platform__return_platform_name(os_environ):
    assert get_platform() == PLATFORM


def test_get_platform__raise_LittleCheesemongerError():
    with pytest.raises(LittleCheesemongerError, match=r"Unable to determine platform"):
        get_platform()
