# catpic - Terminal Image Viewer

Display images directly in your terminal using Unicode mosaic characters and ANSI colors.

```bash
catpic photo.jpg
```

**Multi-language project**: Python implementation complete and serving as reference for C, Rust, and other language ports.

## Features

- **Direct display**: Show any image format in terminal
- **Quality levels**: BASIS 1,2 (universal) through 2,4 (ultra) quality
- **Animations**: Play GIFs directly in terminal
- **Cat-able files**: `.meow` format for sharing over SSH, embedding in scripts
- **No dependencies**: Static images work with `cat`, no viewer needed
- **Cross-platform**: Works wherever terminals support Unicode and truecolor

## Quick Start

```bash
# Python (reference implementation)
pip install catpic

# Display image
catpic photo.jpg

# Play animation
catpic animation.gif

# Generate shareable file
catpic photo.jpg > photo.meow
cat photo.meow  # Display anywhere
```

## BASIS System

Control quality vs compatibility:

```bash
export CATPIC_BASIS=2,2  # Balanced (default)
export CATPIC_BASIS=2,3  # High quality
export CATPIC_BASIS=2,4  # Ultra quality
export CATPIC_BASIS=1,2  # Maximum compatibility
```

| BASIS | Patterns | Unicode | Quality | Compatibility |
|-------|----------|---------|---------|---------------|
| 1,2   | 4        | Block Elements | Low | Universal |
| 2,2   | 16       | Quadrant Blocks | Good | Excellent |
| 2,3   | 64       | Sextant Blocks | High | Good |
| 2,4   | 256      | Legacy Computing | Ultra | Limited |

## Implementations

| Language | Status | Installation | Documentation |
|----------|--------|--------------|---------------|
| **Python** | ✅ Stable | `pip install catpic` | [docs/implementations/python.md](docs/implementations/python.md) |
| **C** | 🚧 Planned | TBD | [docs/implementations/c.md](docs/implementations/c.md) |
| **Rust** | 🚧 Planned | TBD | [docs/implementations/rust.md](docs/implementations/rust.md) |

Python serves as the reference implementation. All language ports follow the same [API specification](spec/api.md).

## Python API

```python
from catpic import CatpicEncoder, CatpicDecoder, CatpicPlayer

# Encode and display
encoder = CatpicEncoder(basis=(2, 2))
meow = encoder.encode_image('photo.jpg', width=80)
decoder = CatpicDecoder()
decoder.display(meow)

# Generate .meow file
with open('photo.meow', 'w') as f:
    f.write(meow)

# Play animation
meow_anim = encoder.encode_animation('animation.gif')
player = CatpicPlayer()
player.play(meow_anim)
```

## MEOW Format

**MEOW** (Mosaic Encoding Over Wire) is a text-based format for terminal images:

- Plain text format (UTF-8)
- Works with `cat`, `less -R`, version control
- Embeddable in scripts and documentation
- Shareable over SSH, chat, wire protocols
- Self-contained with metadata

Example:
```
MEOW/1.0
WIDTH:80
HEIGHT:40
BASIS:2,2
DATA:
[ANSI colored Unicode characters]
```

See [spec/meow-format.md](spec/meow_format.md) for complete specification.

## Project Structure

```
catpic/
├── spec/                    # Specifications (format, API, compliance)
├── docs/                    # Documentation and guides
├── python/                  # Python implementation (reference)
├── c/                       # C implementation (planned)
├── rust/                    # Rust implementation (planned)
└── scripts/                 # Cross-language testing
```

## Documentation

- **Getting Started**: [docs/getting-started.md](docs/getting-started.md)
- **MEOW Format**: [spec/meow-format.md](spec/meow-format.md)
- **API Reference**: [spec/api.md](spec/api.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

## Requirements

**Display Requirements:**
- Terminal with Unicode support
- Truecolor (24-bit RGB) support
- Font with appropriate Unicode blocks

**Tested Terminals:**
- iTerm2 (macOS)
- Windows Terminal
- GNOME Terminal
- Alacritty
- Kitty

**Recommended Fonts:**
- Cascadia Code v2404.3+
- JetBrains Mono
- Fira Code
- Iosevka

## Development

```bash
# Clone repository
git clone https://github.com/friscorose/catpic.git
cd catpic/python

# Setup (using uv)
uv sync --dev

# Run tests
uv run pytest

# Test all implementations
cd ..
./scripts/test-all.sh
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new language implementations.

## Technology

catpic uses the **EnGlyph algorithm** for mosaic encoding:

1. Resize image to cell grid (WIDTH × BASIS_X by HEIGHT × BASIS_Y pixels)
2. For each cell, quantize to 2 colors (foreground/background)
3. Generate bit pattern from pixel states
4. Map pattern to Unicode character
5. Calculate RGB centroids for colors
6. Output ANSI escape sequence

This produces high-quality terminal graphics while maintaining the "cat-able" text format.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- **Repository**: https://github.com/friscorose/catpic
- **Specifications**: [spec/](spec/)
- **Documentation**: [docs/](docs/)
- **Python Package**: [python/](python/)
- **EnGlyph**: https://github.com/friscorose/textual-EnGlyph

---

**Status**: Python implementation complete and stable. Specifications finalized. Ready for additional language implementations.
