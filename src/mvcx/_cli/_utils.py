import shutil
from importlib.abc import Traversable
from pathlib import Path


def copy_files(files: Traversable, path: Path) -> None:
    for item in files.iterdir():
        source_item_path = files.joinpath(item.name)
        target_item_path = path.joinpath(item.name)

        if source_item_path.is_dir():
            # Use shutil.copytree for subdirectories.
            # The 'dirs_exist_ok=True' flag handles cases where
            # a subdirectory of the same name already exists in the target.
            shutil.copytree(source_item_path, target_item_path, dirs_exist_ok=True)  # type: ignore
        else:
            # Use shutil.copy2 for files to preserve metadata.
            shutil.copy2(source_item_path, target_item_path)  # type: ignore
