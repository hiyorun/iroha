from .base import ColorGeneratorBackend
from .material import MaterialYouColorGenerator

__all__ = ["ColorGeneratorBackend", "MaterialYouColorGenerator"]

BACKENDS = {
    "material": MaterialYouColorGenerator,
}
