"""
catpic - Terminal Image Viewer using Unicode mosaics and ANSI colors

High-level API for quick image display and MEOW format handling.
Low-level primitives API for TUI framework integration.
"""

__version__ = "0.5.0"

from typing import Optional, Tuple, Union
from pathlib import Path
from PIL import Image

# Import encoder and decoder classes
from .encoder import CatpicEncoder
from .decoder import CatpicDecoder

# Import core types for tests
from .core import BASIS

# High-level convenience functions
def render_image_ansi(
    image: Union[str, Path, Image.Image],
    width: Optional[int] = None,
    height: Optional[int] = None,
    basis: Optional[Tuple[int, int]] = None,
    pips: bool = False
) -> str:
    """
    Render an image to ANSI string for terminal display.
    
    Args:
        image: Path to image file or PIL Image object
        width: Output width in characters (default: 80)
        height: Output height in characters (default: auto from aspect ratio)
        basis: BASIS level as tuple (x, y) - e.g., (2, 2), (2, 4)
               If None, uses CATPIC_BASIS env var or default (2, 2)
        pips: If True, use pip/dot characters instead of blocks (not implemented yet)
    
    Returns:
        ANSI-formatted string ready for terminal output
    
    Example:
        >>> from catpic import render_image_ansi
        >>> ansi = render_image_ansi('photo.jpg', width=80, basis=(2, 4))
        >>> print(ansi)
    """
    encoder = CatpicEncoder(basis=basis)
    
    # Handle PIL Image object
    if isinstance(image, Image.Image):
        # Save to temp file since encoder expects file path
        # TODO: Refactor encoder to accept PIL Image directly
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            image.save(tmp.name)
            result = encoder.encode_image(tmp.name, width=width, height=height)
        Path(tmp.name).unlink()  # Clean up temp file
        
        # Strip MEOW header, return just the ANSI data
        lines = result.split('\n')
        data_start = lines.index('DATA:') + 1
        return '\n'.join(lines[data_start:])
    
    # Handle file path
    result = encoder.encode_image(image, width=width, height=height)
    
    # Strip MEOW header, return just the ANSI data
    lines = result.split('\n')
    data_start = lines.index('DATA:') + 1
    return '\n'.join(lines[data_start:])


def load_meow(filepath: Union[str, Path]):
    """
    Load a MEOW format file.
    
    Args:
        filepath: Path to .meow file
    
    Returns:
        Tuple of (frames, metadata) where frames is list of ANSI strings
        and metadata is dict with width, height, basis, etc.
    
    Example:
        >>> frames, meta = load_meow('animation.meow')
        >>> print(frames[0])  # Display first frame
    """
    decoder = CatpicDecoder()
    return decoder.load(filepath)


def save_meow(filepath: Union[str, Path], image: Union[str, Path, Image.Image],
              width: Optional[int] = None, height: Optional[int] = None,
              basis: Optional[Tuple[int, int]] = None):
    """
    Save an image as MEOW format file.
    
    Args:
        filepath: Output .meow file path
        image: Source image (path or PIL Image)
        width: Output width in characters
        height: Output height in characters
        basis: BASIS level as tuple (x, y)
    
    Example:
        >>> save_meow('output.meow', 'photo.jpg', width=80, basis=(2, 4))
    """
    encoder = CatpicEncoder(basis=basis)
    
    # Handle PIL Image
    if isinstance(image, Image.Image):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            image.save(tmp.name)
            meow_content = encoder.encode_image(tmp.name, width=width, height=height)
        Path(tmp.name).unlink()
    else:
        meow_content = encoder.encode_image(image, width=width, height=height)
    
    # Write to file
    with open(filepath, 'w') as f:
        f.write(meow_content)

# Primitives API - Core types
from .primitives import Cell

# Primitives API - GLUT functions
from .primitives import get_full_glut, get_pips_glut

# Primitives API - Cell processing
from .primitives import (
    quantize_cell,
    compute_centroid,
    pattern_to_index,
    process_cell,
)

# Primitives API - Image processing
from .primitives import image_to_cells, cells_to_ansi_lines

__all__ = [
    # Version
    "__version__",
    # High-level API
    "render_image_ansi",
    "load_meow",
    "save_meow",
    # Core types
    "BASIS",
    "CatpicEncoder",
    "CatpicDecoder",
    # Primitives - Core types
    "Cell",
    # Primitives - GLUTs
    "get_full_glut",
    "get_pips_glut",
    # Primitives - Cell processing
    "quantize_cell",
    "compute_centroid",
    "pattern_to_index",
    "process_cell",
    # Primitives - Image processing
    "image_to_cells",
    "cells_to_ansi_lines",
]
