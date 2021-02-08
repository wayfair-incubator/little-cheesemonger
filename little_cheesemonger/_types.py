from typing import List, Optional, TypedDict


class ConfigurationType(TypedDict):
    environment_variables: Optional[List[str]]
    system_dependencies: Optional[List[str]]
    python_dependencies: Optional[List[str]]
    steps: Optional[List[str]]
