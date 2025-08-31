from pathlib import Path
from typing import Optional

import typer
from color_generator.color_types import Theme
from color_generator.core import get_backend
from color_generator.templating.jinja import jinja_render_template
from color_generator.templating.map import load_template_config

app = typer.Typer(help="Iroha CLI: Generate color schemes from images or colors.")


@app.command("from-image")
def from_image(
    image_path: Path = typer.Argument(..., exists=True, help="Path to the image file."),
    quality: int = typer.Option(
        100,
        "--quality",
        "-q",
        min=1,
        max=100,
        help="Extraction quality (1 = fastest, 100 = best).",
    ),
    num_colors: int = typer.Option(
        128, "--num-colors", "-n", help="Number of colors to extract."
    ),
    json_output: Optional[Path] = typer.Option(
        None, "--json", "-j", help="Optional output path for saving the JSON."
    ),
    template: Optional[Path] = typer.Option(
        None, "--template", "-i", help="Optional Jinja2 template to render output."
    ),
    template_output: Optional[Path] = typer.Option(
        None, "--template-output", "-o", help="Path to save rendered template output."
    ),
    template_map: Optional[Path] = typer.Option(
        None, "--template-map", "-m", help="YAML config with template-output map"
    ),
    dark_mode: Optional[bool] = typer.Option(
        None, "--dark", "-d", help="Set default color scheme as dark mode"
    ),
    backend: str = typer.Option(
        "material",
        "--backend",
        "-b",
        help="Color generation backend to use. Backends available: 'material'",
    ),
):
    """
    Generate a color scheme from an image.
    """
    sampling_rate = 101 - quality
    generator = get_backend(backend)
    generator.configure(quality=sampling_rate, num_colors=num_colors)

    mode: Theme = "light"
    if dark_mode:
        mode = "dark"
    schemes = generator.generate_from_image(mode, image_path)
    if template_map:
        config = load_template_config(template_map)
        for item in config:
            template_path = Path(item["template"])
            output_path = item.get("output")
            output_light_path = item.get("output_light")
            output_dark_path = item.get("output_dark")

            if output_path:
                jinja_render_template(
                    template_path, schemes["default"], Path(output_path)
                )
            if output_light_path:
                jinja_render_template(
                    template_path, schemes["light"], Path(output_light_path)
                )
            if output_dark_path:
                jinja_render_template(
                    template_path, schemes["dark"], Path(output_dark_path)
                )
        return
    if template:
        jinja_render_template(template, schemes["default"], template_output)
    else:
        output = generator.to_json(schemes["default"])
        if json_output:
            json_output.write_text(output)
            typer.echo(f"Saved to {json_output}")
        else:
            typer.echo(output)


@app.command("from-color")
def from_color(
    color: str = typer.Argument(
        ..., help="Color in hex (#RRGGBB/#AARRGGBB) or rgb/rgba() format."
    ),
    json_output: Optional[Path] = typer.Option(
        None, "--json", "-j", help="Optional output path for saving the JSON."
    ),
    template: Optional[Path] = typer.Option(
        None, "--template", "-t", help="Optional Jinja2 template to render output."
    ),
    template_output: Optional[Path] = typer.Option(
        None,
        "--template-output",
        "-o",
        help="Optional save path for the rendered template. Defaults to printing to the terminal (stdout) if --template is used without this flag.",
    ),
    template_map: Optional[Path] = typer.Option(
        None, "--template-map", "-m", help="YAML config with template-output map"
    ),
    dark_mode: Optional[bool] = typer.Option(
        None, "--dark", "-d", help="Set default color scheme as dark mode"
    ),
    backend: str = typer.Option(
        "material", "--backend", "-b", help="Color generation backend to use."
    ),
):
    """
    Generate a color scheme from a single color.
    """
    if color.startswith("#"):
        hex_color = color[1:].zfill(8)
        if len(hex_color) == 6:
            hex_color = "FF" + hex_color
        color_int = int(hex_color, 16)
    elif color.startswith("rgb"):
        values = color.strip("rgba()").split(",")
        r = int(values[0])
        g = int(values[1])
        b = int(values[2])
        a = int(values[3]) if len(values) > 3 else 255
        color_int = (a << 24) | (r << 16) | (g << 8) | b
    else:
        typer.echo("Invalid color format. Use hex or rgb(a).", err=True)
        raise typer.Exit(1)

    generator = get_backend(backend)
    mode: Theme = "light"
    if dark_mode:
        mode = "dark"
    schemes = generator.generate_from_color(mode, color_int)
    if template_map:
        config = load_template_config(template_map)
        for item in config:
            template_path = Path(item["template"])
            output_path = item.get("output")
            output_light_path = item.get("output_light")
            output_dark_path = item.get("output_dark")

            if output_path:
                jinja_render_template(
                    template_path, schemes["default"], Path(output_path)
                )
            if output_light_path:
                jinja_render_template(
                    template_path, schemes["light"], Path(output_light_path)
                )
            if output_dark_path:
                jinja_render_template(
                    template_path, schemes["dark"], Path(output_dark_path)
                )
        return
    if template:
        jinja_render_template(template, schemes["default"], template_output)
    else:
        output = generator.to_json(schemes["default"])
        if json_output:
            json_output.write_text(output)
            typer.echo(f"Saved to {json_output}")
        else:
            typer.echo(output)


def main():
    app()


if __name__ == "__main__":
    main()
