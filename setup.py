
#!/usr/bin/env python

import setuptools

if __name__ == "__main__":
    setuptools.setup()

#
# # type: ignore
#
# import ast
# import re
#
# import setuptools
#
# _version_re = re.compile(r"__version__\s+=\s+(.*)")
# with open("little_cheesemonger/__init__.py", "rb") as f:
#     _match = _version_re.search(f.read().decode("utf-8"))
#     if _match is None:
#         print("No version found")
#         raise SystemExit(1)
#     version = str(ast.literal_eval(_match.group(1)))
#
#
# setuptools.setup(
#     name="little-cheesemonger",
#     version=version,
#     url="https://github.com/wayfair-incubator/little-cheesemonger",
#     author="Chris Antonellis",
#     author_email="cantonellis@wayfair.com",
#     description="Modify an environment to build and bundle a Python package into a manylinux wheel.",
#     long_description=open("README.md").read(),
#     long_description_content_type="text/markdown",
#     packages=setuptools.find_packages(
#         exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
#     ),
#     entry_points = {
#         "console_scripts": [
#             "little-cheesemonger=little_cheesemonger._cli:entrypoint"
#         ],
#     },
#     package_data={"little_cheesemonger": ["py.typed"]},
#     python_requires=">=3.6",
#     install_requires=["click~=7.1"],
#     classifiers=[
#         "Development Status :: 4 - Beta",
#         "Programming Language :: Python",
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.6",
#         "Programming Language :: Python :: 3.7",
#         "Programming Language :: Python :: 3.8",
#     ],
# )
