from color_generator.backends import BACKENDS
from color_generator.backends.base import ColorGeneratorBackend


def get_backend(name: str = "material") -> ColorGeneratorBackend:
    try:
        return BACKENDS[name]()
    except KeyError:
        raise ValueError(f"Unknown backend: {name}")
