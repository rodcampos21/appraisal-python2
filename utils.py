import importlib
from typing import Optional, Union
import logging
from argparse import ArgumentTypeError


class Logging:
    ...


class Csv:
    def __init__(
        self, name: str, mode: str, debugger: Union[Logging, Optional[None]] = Logging()
    ) -> None:
        ...
        self.file = open(name, mode)

    def __enter__(self):
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        

def missing_rate_float(x: float) -> float:
    """
    Custom type function for validating "missing_range" argument in eraser module
    """
    try:
        x = float(x)
    except ValueError:
        raise ArgumentTypeError("%r not a floating-point literal" % (x,))

    if x < 0.0 or x > 1.0:
        raise ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x


def str_to_class(module_name: str, class_name: str):
    """
    Return a class instance from a string reference
    """
    try:
        module_ = importlib.import_module(module_name)
        try:
            class_ = getattr(module_, class_name)()
        except AttributeError:
            print('Class does not exist')
    except ImportError:
        print('Module does not exist')
    return class_ or None