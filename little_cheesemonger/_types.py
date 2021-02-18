import sys
from typing import List, Optional

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


class ConfigurationType(TypedDict):
    environment_variables: Optional[List[str]]
    system_dependencies: Optional[List[str]]
    python_dependencies: Optional[List[str]]
    python_versions: Optional[List[str]]
    steps: Optional[List[str]]
