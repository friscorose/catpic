# catpic Primitives API

Low-level building blocks for advanced TUI development.

**Status**: v0.5.0 - Pre-release, API may change

## Overview

The primitives API provides composable functions for terminal graphics:
- Cell-level operations
- Custom character tables (GLUTs)
- Image-to-cells conversion
- No MEOW format overhead

**Use for**: TUI frameworks, real-time graphics, mixed text/graphics, custom rendering.

## Core Types

### Cell

Atomic unit of terminal graphics.

```python
from catpic.primitives import Cell

cell = Cell(
    char='▚',
    fg_rgb=(255, 0, 0),
    bg_rgb=(0, 0, 255),
    pattern=9
)

ansi = cell.to_ansi()  # Get ANSI escape sequence
print(ansi)
```

## Quick Rendering

```python
from catpic.primitives import render_image_ansi
from PIL import Image

img = Image.open('photo.jpg')
ansi = render_image_ansi(img, width=80, pips=True)
print(ansi)
```

## Cell Processing

### image_to_cells()

Convert image to 2D cell grid.

```python
from catpic.primitives import image_to_cells, get_pips_glut
from catpic import BASIS

# Full blocks (default)
cells = image_to_cells(img, 80, 40, basis=BASIS.BASIS_2_2)

# Pips (Braille)
glut = get_pips_glut(2, 4)
cells = image_to_cells(img, 80, 40, glut=glut)

# Custom GLUT
custom = [' ', '░', '▒', '▓', '█']
cells = image_to_cells(img, 80, 40, glut=custom)
```

### process_cell()

Process single pixel block to Cell.

```python
from catpic.primitives import process_cell, get_full_glut
from catpic import BASIS

glut = get_full_glut(BASIS.BASIS_2_2)
cell_img = img.crop((0, 0, 2, 2))  # 2×2 block
cell = process_cell(cell_img, glut)
```

## Character Tables (GLUTs)

### get_full_glut()

```python
from catpic.primitives import get_full_glut
from catpic import BASIS

glut = get_full_glut(BASIS.BASIS_2_2)  # 16 quadrant blocks
glut = get_full_glut(BASIS.BASIS_2_4)  # 256 patterns
```

### get_pips_glut()

```python
from catpic.primitives import get_pips_glut

glut = get_pips_glut(2, 2)  # Quadrant dots
glut = get_pips_glut(2, 4)  # Braille (8-dot)
```

## Low-Level Functions

### quantize_cell()

```python
from catpic.primitives import quantize_cell

bits, fg_pixels, bg_pixels = quantize_cell(cell_img)
# bits: [True, False, False, True]
# fg_pixels: [(255, 0, 0), ...]
# bg_pixels: [(0, 0, 255), ...]
```

### compute_centroid()

```python
from catpic.primitives import compute_centroid

pixels = [(255, 0, 0), (200, 50, 0)]
rgb = compute_centroid(pixels)  # (227, 25, 0)
```

### pattern_to_index()

```python
from catpic.primitives import pattern_to_index

bits = [True, False, False, True]
idx = pattern_to_index(bits)  # 9 (2^0 + 2^3)
```

## Advanced Examples

### Mixed Text/Graphics

```python
from catpic.primitives import image_to_cells, cells_to_ansi_lines

cells = image_to_cells(img, 80, 20)
lines = cells_to_ansi_lines(cells)

print("=" * 80)
print("  Dashboard")
print("=" * 80)
for line in lines:
    print(line)
print("=" * 80)
```

### Custom Character Mapping

```python
# Circle gradients
glut = ['○', '◔', '◑', '◕', '●']
cells = image_to_cells(img, 80, 40, glut=glut)
```

### Cell Manipulation

```python
cells = image_to_cells(img, 80, 40)

# Highlight region
for y in range(10, 20):
    for x in range(10, 30):
        cells[y][x].fg_rgb = (255, 0, 0)

# Render
lines = cells_to_ansi_lines(cells)
for line in lines:
    print(line)
```

## Framework Integration

Use primitives as foundation, add framework-specific wrappers:

```python
# In your TUI framework
from catpic.primitives import image_to_cells, get_pips_glut

def integrate_image(image, width, height):
    # Use catpic's proven algorithms
    glut = get_pips_glut(2, 4)
    cells = image_to_cells(image, width, height, glut=glut)
    
    # Convert to your framework's format
    return convert_to_framework_format(cells)
```

This follows DRY - catpic provides core algorithms, you add integration layer.

## Performance Notes

v0.5.0 focuses on correctness. Performance optimizations planned for v1.0:
- Chunked processing for large images
- Parallel cell processing
- Caching for repeated patterns

Current implementation suitable for:
- Static images up to 200×100 cells
- Animations at 10-30 fps
- Real-time at small sizes (<50×50)

## API Stability

**Pre-v1.0**: API may change based on feedback. Breaking changes possible.

**v1.0+**: API will be stable with semantic versioning.

## See Also

- [algorithms.md](algorithms.md) - Algorithm details
- [../spec/api.md](../spec/api.md) - High-level API
- [../python/README.md](../python/README.md) - Python docs
