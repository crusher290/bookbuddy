import time
from functools import wraps
from typing import Callable, Type, Tuple, Optional


def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: Tuple[Type[Exception], ...] = (Exception,)):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        print(f"[FAILED] {func.__name__} failed after {max_attempts} attempts")
                        raise e
                    print(f"[RETRY] {func.__name__} attempt {attempts} failed. Retrying in {delay}s...")
                    time.sleep(delay)
                except Exception as e:
                    raise e
            return None
        return wrapper
    return decorator


def retry_if_error(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        attempts = 0
        while attempts < 3:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                attempts += 1
                if attempts >= 3:
                    print(f"[FAILED] {func.__name__} failed after 3 attempts")
                    raise e
                print(f"[RETRY] {func.__name__} attempt {attempts} failed. Retrying...")
                time.sleep(1)
        return None
    return wrapper


def retry_on_file_error(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        attempts = 0
        while attempts < 3:
            try:
                return func(*args, **kwargs)
            except (FileNotFoundError, PermissionError, OSError) as e:
                attempts += 1
                if attempts >= 3:
                    print(f"[FAILED] File operation {func.__name__} failed after 3 attempts")
                    raise e
                print(f"[RETRY] File operation attempt {attempts} failed. Retrying in 0.5s...")
                time.sleep(0.5)
            except Exception as e:
                raise e
        return None
    return wrapper