# catpic - Python Implementation

**Reference implementation** of catpic terminal image viewer.

**Status**: v0.5.0 - Pre-release, API subject to change

## Installation

```bash
pip install catpic
# or
uv add catpic
```

## Quick Start

```bash
# Display
catpic photo.jpg
catpic animation.gif

# Save
catpic photo.jpg -o photo.meow

# Info
catpic photo.jpg --info
```

## Python API

### High-Level (Simple Use)

```python
from catpic import CatpicEncoder, CatpicDecoder

encoder = CatpicEncoder(basis=(2, 2))
meow = encoder.encode_image('photo.jpg', width=80)

decoder = CatpicDecoder()
decoder.display(meow)
```

### Low-Level (Advanced TUI Development)

```python
from catpic.primitives import image_to_cells, get_pips_glut
from PIL import Image

# Custom rendering
img = Image.open('photo.jpg')
glut = get_pips_glut(2, 4)  # Braille patterns
cells = image_to_cells(img, 80, 40, glut=glut)

# Manipulate cells
for row in cells:
    for cell in row:
        print(cell.to_ansi(), end='')
    print()
```

See [../docs/primitives-api.md](../docs/primitives-api.md) for complete primitives reference.

## Development

```bash
# Setup
cd python
uv sync --dev

# Test
uv run pytest
uv run pytest tests/test_compliance.py  # Spec compliance

# Format
uv run black src/ tests/
uv run ruff check src/ tests/

# Type check
uv run mypy src/
```

## Project Structure

```
python/
├── src/catpic/
│   ├── core.py          # BASIS system, character tables
│   ├── encoder.py       # Image → MEOW
│   ├── decoder.py       # MEOW → display
│   ├── primitives.py    # Low-level API
│   └── cli.py           # Command-line interface
├── tests/
│   ├── test_core.py
│   └── test_compliance.py
└── pyproject.toml
```

## Reference Implementation

This Python implementation defines canonical behavior for:
- EnGlyph algorithm (quantization, bit patterns, centroids)
- MEOW format structure
- BASIS character mappings
- API design patterns

Other language implementations follow this as reference.

## Contributing

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

Python-specific:
- Use Black + Ruff for formatting
- Full type hints required
- Pytest for tests
- Follow existing code patterns

## License

MIT License - see [../LICENSE](../LICENSE)
