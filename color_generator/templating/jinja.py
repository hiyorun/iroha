from pathlib import Path
from typing import Optional
from jinja2 import Environment, FileSystemLoader

from color_generator.color_types import ColorScheme


def jinja_render_template(
    template_path: Path, context: ColorScheme, output_path: Optional[Path] = None
) -> None:
    """Render a Jinja2 template with the given context."""

    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template(template_path.name)
    rendered = template.render(**context)

    if output_path:
        output_path.write_text(rendered)
        print(f"✅ Template rendered to {output_path}")
    else:
        print(rendered)
