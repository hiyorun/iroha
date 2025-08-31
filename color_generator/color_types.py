from typing import Literal, TypedDict, Protocol, runtime_checkable
from pathlib import Path

LightMode = Literal["light"]
DarkMode = Literal["dark"]
Theme = LightMode | DarkMode


class ColorObject(TypedDict):
    r: int
    g: int
    b: int
    h: int
    s: int
    l: int
    a: float
    rgba: str
    rgb: str
    hex: str
    hex_unhashed: str
    hsla: str
    hsla_no_decor: str
    hsl: str
    hsl_no_decor: str


class ColorScheme(TypedDict):
    primary: ColorObject
    onPrimary: ColorObject
    primaryContainer: ColorObject
    onPrimaryContainer: ColorObject
    secondary: ColorObject
    onSecondary: ColorObject
    secondaryContainer: ColorObject
    onSecondaryContainer: ColorObject
    tertiary: ColorObject
    onTertiary: ColorObject
    tertiaryContainer: ColorObject
    onTertiaryContainer: ColorObject
    error: ColorObject
    onError: ColorObject
    errorContainer: ColorObject
    onErrorContainer: ColorObject
    background: ColorObject
    onBackground: ColorObject
    surface: ColorObject
    onSurface: ColorObject
    surfaceVariant: ColorObject
    onSurfaceVariant: ColorObject
    outline: ColorObject
    outlineVariant: ColorObject
    shadow: ColorObject
    scrim: ColorObject
    inverseSurface: ColorObject
    inverseOnSurface: ColorObject
    inversePrimary: ColorObject


class ColorSchemes(TypedDict):
    default: ColorScheme
    light: ColorScheme
    dark: ColorScheme


@runtime_checkable
class ColorGenerator(Protocol):
    def generate_from_image(self, image_path: Path) -> ColorScheme:
        """Generate a color scheme from an image."""
        ...

    def generate_from_color(self, color: int) -> ColorScheme:
        """Generate a color scheme from a single color."""
        ...
