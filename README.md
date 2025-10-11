# catpic

Turn images into terminal eye candy using Unicode mosaics and ANSI colors.

## What are Glyxels?

**Glyxels** (glyph + pixels) are what happens when you treat each terminal character as a tiny canvas. catpic uses the EnGlyph algorithm to subdivide characters into grids—for example, BASIS 2×4 means each character represents 8 pixels (2 wide, 4 tall).

The magic:
1. Slice your image into character-sized cells
2. Find the two most important colors in each cell
3. Pick the Unicode character that matches the pixel pattern
4. Paint it with ANSI true-color

Result? A standard 80×24 terminal becomes a 160×96 pixel display. Not bad for text.

## Features

- **Multiple BASIS levels**: Trade speed for quality (1×2 to 2×4)
- **MEOW format**: Save rendered images for instant replay
- **Smooth animations**: GIF playback with no flicker
- **Primitives API**: Build your own TUI graphics with composable functions
- **Environment aware**: `CATPIC_BASIS` sets your preferred quality

## Installation

### As a CLI Tool

```bash
uv tool install catpic
```

System-wide command, isolated environment. Just works.

### As a Library

```bash
pip install catpic
# or
uv add catpic
```

Requires Python 3.8+

## Quick Start

```bash
# Display an image
catpic photo.jpg

# Crank up the quality
export CATPIC_BASIS=2,4
catpic photo.jpg

# Save for later
catpic photo.jpg -o photo.meow
catpic photo.meow  # instant display

# Animate
catpic animation.gif
```

## Python (Reference Implementation)

### High-Level API

```python
from catpic import render_image_ansi, save_meow, load_meow
from PIL import Image

# Quick render
img = Image.open('photo.jpg')
ansi = render_image_ansi(img, width=60, basis=(2, 4))
print(ansi)

# Save as MEOW
save_meow('output.meow', img, width=60, basis=(2, 4))

# Load and display
frames, metadata = load_meow('output.meow')
print(frames[0])
```

### Primitives API

For when you need fine control:

```python
from catpic import (
    Cell, get_full_glut, image_to_cells, 
    cells_to_ansi_lines
)
from catpic import BASIS
from PIL import Image

# Custom rendering pipeline
img = Image.open('photo.jpg')
glut = get_full_glut(BASIS.BASIS_2_4)
cells = image_to_cells(img, width=80, height=40, glut=glut)

# Now you have a 2D grid of Cell objects
# Do whatever you want with them
for row in cells:
    for cell in row:
        # cell.char, cell.fg_rgb, cell.bg_rgb, cell.pattern
        pass

# Convert to ANSI when ready
lines = cells_to_ansi_lines(cells)
print('\n'.join(lines))
```

See [docs/primitives_api.md](docs/primitives_api.md) for the full primitives reference.

## Project Structure

```
catpic/
├── python/              # Reference implementation
│   ├── src/catpic/     # Core library
│   ├── tests/          # Test suite
│   └── scripts/        # Utilities
├── c/                   # C implementation (WIP)
├── docs/                # Architecture & API docs
│   ├── primitives_api.md
│   └── implementations/
├── spec/                # Format specifications
│   ├── meow_format.md
│   ├── api.md
│   └── compliance.md
├── scripts/             # Cross-language testing
└── benchmarks/          # Performance data
```

All implementations share the MEOW format and pass identical compliance tests.

## How BASIS Works

BASIS (x, y) defines the pixel grid per character:

- **1×2** (4 patterns): Fast, chunky. Good for large images.
- **2×2** (16 patterns): Balanced. Default for most use cases.
- **2×3** (64 patterns): Smooth gradients. Sextant blocks.
- **2×4** (256 patterns): Maximum detail. Braille patterns.

Higher BASIS = better quality, slower rendering. Pick your poison.

## MEOW Format

**M**osaic **E**ncoding **O**ver **W**ire—a simple text format for terminal graphics:

```
MEOW/1.0
WIDTH:80
HEIGHT:24
BASIS:2,4
DATA:
[ANSI-colored character grid]
```

Human-readable, easily streamable, version-controlled friendly. It's just fancy text all the way down.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style and testing requirements
- How to add new BASIS levels
- Cross-language implementation guidelines
- Prospective features (Sixel/Kitty graphics, streaming, etc.)

## Testing

```bash
cd python
uv sync --all-extras
uv run pytest -v
```

All implementations must pass the compliance test suite in `spec/compliance.md`.

## License

MIT—do whatever you want with it.

## See Also

- [EnGlyph](https://github.com/friscorose/textual-EnGlyph) - The Textual widget that inspired this
- [docs/primitives_api.md](docs/primitives_api.md) - Build your own TUI graphics
- [spec/meow_format.md](spec/meow_format.md) - Format specification

---

*Built with Claude (Anthropic) exploring terminal graphics techniques that don't suck.*
