from functools import wraps
from typing import Callable
import time


def log_call(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[CALL] Running {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[CALL] Finished {func.__name__}")
        return result
    return wrapper


def timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper


def validate_not_empty(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, str) and not arg.strip():
                raise ValueError("String argument cannot be empty")
        for key, value in kwargs.items():
            if isinstance(value, str) and not value.strip():
                raise ValueError(f"String argument '{key}' cannot be empty")
        return func(*args, **kwargs)
    return wrapper


def debug(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[DEBUG] {func.__name__} called with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[DEBUG] {func.__name__} returned {result}")
        return result
    return wrapper