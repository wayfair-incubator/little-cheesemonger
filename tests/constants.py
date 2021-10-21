from pathlib import Path

PLATFORM = "PLATFORM"
ARCHITECTURE = "ARCHITECTURE"
PYTHON_VERSION = "FOO38"
PLATFORM_RAW = f"{PLATFORM}_{ARCHITECTURE}"

DIRECTORY = Path(".")
LOADER_IMPORT_PATH = "foo.bar"
LOADER_ARGS = ("foo",)
LOADER_KWARGS = {"foo": "bar"}
ENVIRONMENT_VARIABLES = ["foo=bar"]
SYSTEM_DEPENDENCIES = ["foo-1.0.0"]
PYTHON_DEPENDENCIES = ["foo==1.0.0"]
PYTHON_VERSIONS = [PYTHON_VERSION]
STEPS = ["foo"]
CONFIGURATION = {
    "environment_variables": ENVIRONMENT_VARIABLES,
    "system_dependencies": SYSTEM_DEPENDENCIES,
    "python_dependencies": PYTHON_DEPENDENCIES,
    "python_versions": PYTHON_VERSIONS,
    "steps": STEPS,
}
