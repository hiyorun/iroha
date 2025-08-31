from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image
import json

from materialyoucolor.scheme import Scheme
from materialyoucolor.quantize import QuantizeCelebi
from materialyoucolor.score.score import Score

from color_generator.color_types import ColorObject, ColorScheme, ColorSchemes, Theme

from .base import ColorGeneratorBackend


class MaterialYouColorGenerator(ColorGeneratorBackend):
    def __init__(self, quality: int = 1, num_colors: int = 128):
        """Initialize the color generator.

        Args:
            quality: Quality of color extraction (1 = best, higher = faster but lower quality)
            num_colors: Number of colors to extract from image
        """
        self.quality = quality
        self.num_colors = num_colors

    def configure(self, **kwargs):
        """Override to configure settings dynamically."""
        if "quality" in kwargs:
            self.quality = kwargs["quality"]
        if "num_colors" in kwargs:
            self.num_colors = kwargs["num_colors"]

    def _rgba_to_color_object(self, rgba: List[int]) -> ColorObject:
        """Convert RGBA list to ColorObject dict."""
        r, g, b, a = rgba
        roundedAlpha = round(a / 255, 1)
        h, s, l = self._rgb_to_hsl(r, g, b)
        return {
            "r": r,
            "g": g,
            "b": b,
            "h": round(h),
            "s": round(s),
            "l": round(l),
            "a": roundedAlpha,
            "rgb": f"rgb({r},{g},{b})",
            "rgba": f"rgba({r},{g},{b},{roundedAlpha})",
            "hex": f"#{r:02X}{g:02X}{b:02X}",
            "hex_unhashed": f"{r:02X}{g:02X}{b:02X}",
            "hsla": f"hsla({round(h)},{round(s)}%,{round(l)}%,{roundedAlpha})",
            "hsla_no_decor": f"hsla({round(h)},{round(s)},{round(l)},{roundedAlpha})",
            "hsl": f"hsl({round(h)},{round(s)}%,{round(l)}%)",
            "hsl_no_decor": f"hsl({round(h)},{round(s)},{round(l)})",
        }

    def _rgb_to_hsl(self, r: int, g: int, b: int) -> Tuple[float, float, float]:
        norm_r = r / 255.0
        norm_g = g / 255.0
        norm_b = b / 255.0

        max_c = max(norm_r, norm_g, norm_b)
        min_c = min(norm_r, norm_g, norm_b)
        lightness = (max_c + min_c) / 2

        if max_c == min_c:
            h = s = 0.0
        else:
            d = max_c - min_c
            s = d / (2 - max_c - min_c) if lightness > 0.5 else d / (max_c + min_c)

            if max_c == norm_r:
                h = (norm_g - norm_b) / d + (6 if norm_g < norm_b else 0)
            elif max_c == norm_g:
                h = (norm_b - norm_r) / d + 2
            else:
                h = (norm_r - norm_g) / d + 4

            h /= 6

        return h * 360, s * 100, lightness * 100

    def _int_to_rgba(self, color_int: int) -> List[int]:
        """Convert color integer to RGBA list."""
        r = (color_int >> 16) & 0xFF
        g = (color_int >> 8) & 0xFF
        b = color_int & 0xFF
        a = (color_int >> 24) & 0xFF
        return [r, g, b, a]

    def _scheme_to_color_scheme(self, scheme: Scheme) -> ColorScheme:
        """Convert Material You scheme to our ColorScheme type."""
        props = scheme.props
        return {
            "primary": self._rgba_to_color_object(props["primary"]),
            "onPrimary": self._rgba_to_color_object(props["onPrimary"]),
            "primaryContainer": self._rgba_to_color_object(props["primaryContainer"]),
            "onPrimaryContainer": self._rgba_to_color_object(
                props["onPrimaryContainer"]
            ),
            "secondary": self._rgba_to_color_object(props["secondary"]),
            "onSecondary": self._rgba_to_color_object(props["onSecondary"]),
            "secondaryContainer": self._rgba_to_color_object(
                props["secondaryContainer"]
            ),
            "onSecondaryContainer": self._rgba_to_color_object(
                props["onSecondaryContainer"]
            ),
            "tertiary": self._rgba_to_color_object(props["tertiary"]),
            "onTertiary": self._rgba_to_color_object(props["onTertiary"]),
            "tertiaryContainer": self._rgba_to_color_object(props["tertiaryContainer"]),
            "onTertiaryContainer": self._rgba_to_color_object(
                props["onTertiaryContainer"]
            ),
            "error": self._rgba_to_color_object(props["error"]),
            "onError": self._rgba_to_color_object(props["onError"]),
            "errorContainer": self._rgba_to_color_object(props["errorContainer"]),
            "onErrorContainer": self._rgba_to_color_object(props["onErrorContainer"]),
            "background": self._rgba_to_color_object(props["background"]),
            "onBackground": self._rgba_to_color_object(props["onBackground"]),
            "surface": self._rgba_to_color_object(props["surface"]),
            "onSurface": self._rgba_to_color_object(props["onSurface"]),
            "surfaceVariant": self._rgba_to_color_object(props["surfaceVariant"]),
            "onSurfaceVariant": self._rgba_to_color_object(props["onSurfaceVariant"]),
            "outline": self._rgba_to_color_object(props["outline"]),
            "outlineVariant": self._rgba_to_color_object(props["outlineVariant"]),
            "shadow": self._rgba_to_color_object(props["shadow"]),
            "scrim": self._rgba_to_color_object(props["scrim"]),
            "inverseSurface": self._rgba_to_color_object(props["inverseSurface"]),
            "inverseOnSurface": self._rgba_to_color_object(props["inverseOnSurface"]),
            "inversePrimary": self._rgba_to_color_object(props["inversePrimary"]),
            # "surfaceTint": self._rgba_to_color_rgb(props["surfaceTint"]),
        }

    def generate_from_image(self, mode: Theme, image_path: Path) -> ColorSchemes:
        """Generate a color scheme from an image.

        Args:
            scheme: "light" or "dark" mode as the default ColorScheme
            image_path: Path to the image file

        Returns:
            ColorSchemes: Contains the default, the light, and dark color schemes.
        """
        image = Image.open(image_path)
        pixel_len = image.width * image.height
        image_data = image.getdata()

        pixel_array = [image_data[i] for i in range(0, pixel_len, self.quality)]
        result = QuantizeCelebi(pixel_array, self.num_colors)
        scored_colors = Score.score(result)
        primary_color = scored_colors[0]

        light_scheme = Scheme.light(primary_color)
        dark_scheme = Scheme.dark(primary_color)
        default_scheme: Scheme
        if mode == "dark":
            default_scheme = dark_scheme
        else:
            default_scheme = light_scheme
        return {
            "default": self._scheme_to_color_scheme(default_scheme),
            "light": self._scheme_to_color_scheme(light_scheme),
            "dark": self._scheme_to_color_scheme(dark_scheme),
        }

    def generate_from_color(self, mode: Theme, color: int) -> ColorSchemes:
        """Generate a color scheme from a single color.

        Args:
            color: Color as integer (0xAARRGGBB format)

        Returns:
            ColorScheme: Generated color scheme
        """
        light_scheme = Scheme.light(color)
        dark_scheme = Scheme.dark(color)
        default_scheme: Scheme
        if mode == "dark":
            default_scheme = dark_scheme
        else:
            default_scheme = light_scheme
        return {
            "default": self._scheme_to_color_scheme(default_scheme),
            "light": self._scheme_to_color_scheme(light_scheme),
            "dark": self._scheme_to_color_scheme(dark_scheme),
        }

    def to_json(self, scheme: ColorScheme) -> str:
        """Convert color scheme to JSON string.

        Args:
            scheme: Color scheme to convert

        Returns:
            str: JSON string representation of the color scheme
        """
        return json.dumps(scheme, indent=2)
