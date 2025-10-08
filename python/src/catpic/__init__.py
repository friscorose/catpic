"""catpic - Terminal Image Viewer using MEOW format."""

from .core import BASIS, get_default_basis
from .decoder import CatpicDecoder, CatpicPlayer
from .encoder import CatpicEncoder

# Low-level primitives for advanced TUI development
from .primitives import (
    Cell,
    cells_to_ansi_lines,
    compute_centroid,
    get_full_glut,
    get_pips_glut,
    image_to_cells,
    pattern_to_index,
    process_cell,
    quantize_cell,
    render_image_ansi,
)

__version__ = "0.1.0"

__all__ = [
    # High-level API
    "CatpicEncoder",
    "CatpicDecoder",
    "CatpicPlayer",
    "BASIS",
    "get_default_basis",
    # Low-level primitives
    "Cell",
    "quantize_cell",
    "compute_centroid",
    "pattern_to_index",
    "process_cell",
    "image_to_cells",
    "cells_to_ansi_lines",
    "render_image_ansi",
    # GLUT functions
    "get_full_glut",
    "get_pips_glut",
]
