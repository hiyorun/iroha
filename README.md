# iroha

My personal template based colour palette generator. Currently using the Python implementation of the [Material Color Utilities by T-Dynamos](https://github.com/T-Dynamos/materialyoucolor-python). Can be extended in the future if I feel like it.

## Building

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage

### Generate from Image

```bash
iroha from-image path/to/image.jpg

# With options
iroha from-image path/to/image.jpg --quality 2 --num-colors 64 --output colors.json
```

### Generate from Color

```bash
# Using hex color
iroha from-color "#4181EE"

# Using RGB
iroha from-color "rgb(65,129,238)"

# Using RGBA
iroha from-color "rgba(65,129,238,255)"

# Save to file
iroha from-color "#4181EE" --output colors.json
```

