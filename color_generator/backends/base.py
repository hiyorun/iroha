from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple
from ..color_types import ColorScheme, ColorSchemes, Theme


class ColorGeneratorBackend(ABC):
    @abstractmethod
    def configure(self, **kwargs):
        """Configure backend parameters. Override in subclass if needed."""
        pass

    @abstractmethod
    def generate_from_image(self, mode: Theme, image_path: Path) -> ColorSchemes:
        pass

    @abstractmethod
    def generate_from_color(self, mode: Theme, color: int) -> ColorSchemes:
        pass

    @abstractmethod
    def to_json(self, scheme: ColorScheme) -> str:
        pass
