import yaml
from pathlib import Path
from typing import List, Optional, TypedDict


class TemplateItem(TypedDict):
    template: str
    output: Optional[str]
    output_light: Optional[str]
    output_dark: Optional[str]


def load_template_config(path: Path) -> List[TemplateItem]:
    with path.open("r") as f:
        config = yaml.safe_load(f)
    return config.get("templates", [])
