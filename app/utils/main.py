from typing import Callable, Optional


def response(
    results: list[tuple],
    key1: str = "label",
    key2: str = "value",
    value_func: Optional[Callable[[float], float]] = None,
):
    return [
        {key1: key, key2: value_func(value) if value_func else value}
        for key, value in results
    ]
