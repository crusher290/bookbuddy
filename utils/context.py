from contextlib import contextmanager
from typing import Any
import json
import pickle
from exceptions import FileOperationError


@contextmanager
def safe_file_open(filename: str, mode: str = 'r', encoding: str = 'utf-8'):
    file = None
    try:
        file = open(filename, mode, encoding=encoding)
        yield file
    except FileNotFoundError:
        raise FileOperationError(filename, "File not found")
    except PermissionError:
        raise FileOperationError(filename, "Permission denied")
    except Exception as e:
        raise FileOperationError(filename, str(e))
    finally:
        if file:
            file.close()


@contextmanager
def safe_json_load(filename: str):
    try:
        with safe_file_open(filename, 'r') as file:
            data = json.load(file)
            yield data
    except json.JSONDecodeError as e:
        raise FileOperationError(filename, f"Invalid JSON: {str(e)}")


@contextmanager
def safe_pickle_load(filename: str):
    try:
        with safe_file_open(filename, 'rb') as file:
            data = pickle.load(file)
            yield data
    except pickle.UnpicklingError as e:
        raise FileOperationError(filename, f"Invalid pickle: {str(e)}")


@contextmanager
def safe_json_save(filename: str, data: Any):
    try:
        with safe_file_open(filename, 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            yield file
    except Exception as e:
        raise FileOperationError(filename, str(e))


@contextmanager
def safe_pickle_save(filename: str, data: Any):
    try:
        with safe_file_open(filename, 'wb') as file:
            pickle.dump(data, file)
            yield file
    except Exception as e:
        raise FileOperationError(filename, str(e))


@contextmanager
def temporary_change(value: Any, attribute: str, obj: Any):
    old_value = getattr(obj, attribute)
    setattr(obj, attribute, value)
    try:
        yield
    finally:
        setattr(obj, attribute, old_value)