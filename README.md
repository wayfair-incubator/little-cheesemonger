<p align="center">
  <img width="300" height="300" src="logo.svg" alt="cheese chef">
</p>

# little-cheesemonger

`little-cheesemonger` is a package that can set up a manylinux build environment to compile a
correctly linked manylinux wheel. Configuration data is loaded from a `pyproject.toml` file, or
a custom data loader can be implemented.

## Installation

```bash
pip install little-cheesemonger==0.2.0
```

## Quickstart

To trigger environment setup, either run `little-cheesemonger` from the root directory of a package, or pass the path to the package you want compiled. The package must contain configuration data in its `pyproject.toml` file for environment setup to work.

```bash
little-cheesemonger path/to/package
```

## Default Configuration

The manylinux image version is controlled by last section of the configuration heading. The `latest` tag is always used.

```toml
[tool.little-cheesemonger.manylinux2014_x86_64]
environment_variables = [
  "FOO=BAR"
]
system_dependencies = [
  "atlas"
]
python_dependencies = [
  "nyancat==0.1.2"
]
python_versions = [
  "cp36-cp36m"
  "cp38-cp38"
]
steps = [
  "touch /foobar.txt"
]
```

* `environment_variables` is a list of environment variables to set in the container
prior to building the wheel. They are expected to be in `KEY=VALUE` format.
* `system_dependencies` is a list of CentOS system dependencies to install via `YUM`.
They are expected to be in `package-version` format.
* `python_dependencies` is a list of Python dependencies to install via `pip`. They
are expected to be in `package==version` format. They are currently installed for
all available versions of Python in a given manylinux image.
* `python_versions` is a list of Python versions to install Python dependencies for
in a given manylinux image. They are expected to follow the Python installation directory
naming convention from in the specified manyliniux image, ex. `cp36-cp36m`. Python version names
can be found by running `ls /opt/python` in a manylinux image.
* `steps` is a list of steps to execute via bash. Package building and uploading could
be implemented here, or `little-cheesemonger` could be integrated into a larger system!

# Custom Data Loader

You can pass the path to an importable function, as well as positional and keyword arguments to `little-cheesemonger` to customize how configuration data is loaded.

```bash
little-cheesemonger --data-loader path.to.function --loader-arg foo --loader-kwarg foo=bar
```

Custom data loader functions must accept `directory` as the first argument with positional and keyword arguments passed to the loader function after. The function must return a dictionary of configuration data matching the fields above.

```python
def my_custom_loader(directory: Path, ...) -> Dict:
  pass
```
