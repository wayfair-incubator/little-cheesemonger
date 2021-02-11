from pathlib import Path

import yaml

from little_cheesemonger import LittleCheesemongerError

RECIPES_PATH = Path("/app/tests/integration/assets/recipes")


def recipe_loader(_, package_name, package_version):

    try:
        with open(RECIPES_PATH / f"{package_name}.yaml", "r") as file_handle:
            recipe_data = yaml.load(file_handle, Loader=yaml.Loader)
    except (FileNotFoundError, yaml.YAMLError) as e:
        raise LittleCheesemongerError(f"Unable to load recipe file: {e}")

    recipe = None
    for recipe_version in recipe_data["versions"].values():
        if package_version in recipe_version["package_versions"]:
            recipe = recipe_version
            break

    if recipe is None:
        raise LittleCheesemongerError(
            f"No recipe for specified version {package_version}"
        )

    # NOTE: map to little-cheesemonger configuration fields
    configuration = {
        "environment_variables": recipe["environment_variables"],
        "system_dependencies": recipe["system_dependencies"],
        "python_dependencies": recipe["python_package_dependencies"],
        "steps": recipe["bash_commands"],
    }

    return configuration
