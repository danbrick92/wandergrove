import importlib
import importlib.util
import inspect
from pathlib import Path
from typing import Any


def get_class_fqcn(fqcn: str, as_instance: bool = False, **kwargs) -> Any:
    """Import a class by its fully-qualified class name and optionally instantiate it."""
    module_name, class_name = fqcn.rsplit(".", 1)
    module = importlib.import_module(module_name)
    class_obj = getattr(module, class_name)

    if not inspect.isclass(class_obj):
        raise TypeError(f"{fqcn} is not a class")

    return class_obj(**kwargs) if as_instance else class_obj


def load_module_from_path(path: str | Path) -> None:
    """Import all .py files in a directory as top-level modules."""
    path = Path(path)

    if not path.is_dir():
        raise OSError(f"Directory does not exist: {path}")

    for py_file in path.glob("*.py"):
        spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
