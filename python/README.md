```
## AI Collaboration Context
**Project:** catpic - Terminal Image Viewer | **Session:** #1 | **Date:** 2025-01-27 | **Lead:** [Your Name]  
**AI Model:** Claude Sonnet 4 | **Objective:** Create comprehensive catpic project structure
**Prior Work:** Initial session  
**Current Status:** Complete project scaffolding with BASIS system and EnGlyph integration. Renamed to catpic with .meow extension
**Files in Scope:** New project - all files created  
**Human Contributions:** Requirements analysis, EnGlyph research, BASIS system design, development strategy, UX design (viewer-first approach), naming (catpic/.meow)  
**AI Contributions:** Project structure, code generation, documentation, testing framework  
**Pending Decisions:** Phase 1 implementation approach, specific BASIS character sets for 2,3 and 2,4
```

# catpic - Terminal Image Viewer

Display images directly in your terminal using mosaic block characters and ANSI colors.

## Features

- **Instant display**: Show any image format directly in terminal with `catpic image.jpg`
- **Animation support**: Play GIFs directly with `catpic animation.gif` 
- **Cat-able files**: Generate `.meow` files for sharing over wire and scripting
- **Scalable quality**: BASIS system from universal compatibility to ultra-high quality
- **Modern Python**: Built with UV, type hints, and comprehensive testing

## Installation

```bash
# Using uv (recommended)
uv add catpic

# Using pip
pip install catpic
```

## Quick Start

```bash
# Display any image directly in terminal
catpic photo.jpg

# Display animated GIF directly  
catpic animation.gif

# Generate cat-able files when needed
catpic generate photo.jpg          # Creates photo.meow
catpic convert animation.gif       # Creates animation.meow

# Display cat-able files
cat photo.meow
catpic animation.meow             # or cat animation.meow
```

## BASIS System

catpic uses a pixel subdivision system for different quality/compatibility levels:

- **BASIS 1,2**: 4 patterns ( ▀▄█) - Universal terminal compatibility
- **BASIS 2,2**: 16 patterns (quadrant blocks) - Balanced quality/compatibility
- **BASIS 2,3**: 64 patterns (sextant blocks) - High quality
- **BASIS 2,4**: 256 patterns (Legacy Computing) - Ultra quality

## MEOW Format

**MEOW** (Mosaic Encoding Over Wire) - A text-based format for terminal images that can be cat-ed, shared over SSH, and embedded in scripts.

## Python API

```python
from catpic import CatpicEncoder, CatpicDecoder, CatpicPlayer

# Display any image directly (primary use case)
encoder = CatpicEncoder(basis=(2, 2))
meow_content = encoder.encode_image('photo.jpg', width=80)
decoder = CatpicDecoder()
decoder.display(meow_content)

# Generate cat-able file
with open('photo.meow', 'w') as f:
    f.write(meow_content)

# Animation
meow_anim = encoder.encode_animation('animation.gif')
player = CatpicPlayer()
player.play(meow_anim)
```

## Development

```bash
# Setup development environment
uv sync --dev

# Run tests
uv run pytest

# Format code
uv run black src/ tests/
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

## License

MIT License - see LICENSE file for details.
