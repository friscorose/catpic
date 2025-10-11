"""
Low-level mosaic primitives for advanced TUI development.

These functions provide the building blocks for terminal graphics:
- Cell-level operations (quantize, character selection, color calculation)
- Image-to-cells conversion
- Custom character table (GLUT) support

Use these to build custom TUI graphics, animations, or integrate with
frameworks like Textual. The high-level encoder uses these internally.
"""

from typing import Dict, List, Optional, Tuple, Union

from PIL import Image

from .core import BASIS, CatpicCore


class Cell:
    """
    Represents a single terminal character cell with mosaic encoding.
    
    A cell is the atomic unit of terminal graphics in catpic:
    - One Unicode character
    - Foreground RGB color
    - Background RGB color
    
    Attributes:
        char: Unicode character (from GLUT)
        fg_rgb: Foreground color (r, g, b) tuple
        bg_rgb: Background color (r, g, b) tuple
        pattern: Bit pattern index (0 to 2^(basis_x*basis_y)-1)
    """
    
    def __init__(
        self,
        char: str,
        fg_rgb: Tuple[int, int, int],
        bg_rgb: Tuple[int, int, int],
        pattern: int = 0,
    ):
        self.char = char
        self.fg_rgb = fg_rgb
        self.bg_rgb = bg_rgb
        self.pattern = pattern
    
    def to_ansi(self) -> str:
        """Convert cell to ANSI escape sequence."""
        return CatpicCore.format_cell(self.char, self.fg_rgb, self.bg_rgb)
    
    def __repr__(self) -> str:
        return f"Cell('{self.char}', fg={self.fg_rgb}, bg={self.bg_rgb}, pattern={self.pattern})"


# Glyph Lookup Tables (GLUT)
# These map bit patterns to Unicode characters

def get_full_glut(basis: BASIS) -> List[str]:
    """
    Get full-fill GLUT for BASIS level.
    
    Returns character table where pixels are represented as filled blocks.
    This is the default rendering style (used by CatpicCore.BLOCKS).
    
    Args:
        basis: BASIS level
    
    Returns:
        List of characters indexed by bit pattern
    """
    return CatpicCore.BLOCKS[basis]


def get_pips_glut(basis_x: int, basis_y: int) -> List[str]:
    """
    Get pips (Braille-style) GLUT for basis dimensions.
    
    Pips use partial-fill characters (dots/braille patterns) instead of
    solid blocks. Popular in many TUI image tools.
    
    Based on EnGlyph's pips_glut. Supports:
    - BASIS 1,1: Single dot
    - BASIS 1,2: Vertical braille-style
    - BASIS 2,2: Quadrant dots
    - BASIS 2,3: Sextant dots
    - BASIS 2,4: Braille patterns (2×4 = 8 dots)
    
    Args:
        basis_x: Horizontal subdivision (1 or 2)
        basis_y: Vertical subdivision (1-4)
    
    Returns:
        List of characters indexed by bit pattern
    
    Example:
        >>> glut = get_pips_glut(2, 4)
        >>> glut[255]  # All bits set
        '⣿'  # Full braille block
    """
    # Pips GLUTs from EnGlyph - copied directly from toglyxels.py
    # Structure: pips_glut[x][y] is a string of characters
    pips_glut = [[], ["", "", ""], ["", "", "", "", ""]]
    pips_glut[1][1] = " ◦"
    pips_glut[1][2] = " ᛫.:"
    pips_glut[2][2] = " 𜰡𜰢𜰣𜰤𜰥𜰦𜰧𜰨𜰩𜰪𜰫𜰬𜰭𜰮𜰯"
    pips_glut[2][3] = " 𜹑𜹒𜹓𜹔𜹕𜹖𜹗𜹘𜹙𜹚𜹛𜹜𜹝𜹞𜹟𜹠𜹡𜹢𜹣𜹤𜹥𜹦𜹧𜹨𜹩𜹪𜹫𜹬𜹭𜹮𜹯𜹰𜹱𜹲𜹳𜹴𜹵𜹶𜹷𜹸𜹹𜹺𜹻𜹼𜹽𜹾𜹿𜺀𜺁𜺂𜺃𜺄𜺅𜺆𜺇𜺈𜺉𜺊𜺋𜺌𜺍𜺎𜺏"
    pips_glut[2][4] = (
        "⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿"
        "⡀⡁⡂⡃⡄⡅⡆⡇⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛⡜⡝⡞⡟⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿"
        "⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟⢠⢡⢢⢣⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷⢸⢹⢺⢻⢼⢽⢾⢿"
        "⣀⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿"
    )
    
    # Convert string to list of characters
    if basis_x < len(pips_glut) and basis_y < len(pips_glut[basis_x]):
        return list(pips_glut[basis_x][basis_y])
    else:
        raise ValueError(f"No pips GLUT for BASIS ({basis_x}, {basis_y})")


def quantize_cell(
    cell_img: Image.Image,
) -> Tuple[List[bool], List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
    """
    Quantize a pixel block to 2 colors (foreground/background).
    
    Uses PIL's median cut algorithm to find two representative colors,
    then classifies each pixel as foreground (bright) or background (dark).
    
    Args:
        cell_img: PIL Image containing BASIS_X × BASIS_Y pixels
    
    Returns:
        pattern_bits: List of bools (True = foreground, False = background)
        fg_pixels: List of RGB tuples for foreground pixels
        bg_pixels: List of RGB tuples for background pixels
    
    Example:
        >>> cell = img.crop((0, 0, 2, 2))  # 2×2 block
        >>> bits, fg, bg = quantize_cell(cell)
        >>> bits  # [True, False, False, True] = pattern 9
    """
    fg_pixels = []
    bg_pixels = []
    
    # Quantize to 2 colors using median cut
    duotone = cell_img.quantize(colors=2)
    
    # Classify each pixel and collect original colors
    for idx, pixel_class in enumerate(list(duotone.getdata())):
        original_pixel = cell_img.getdata()[idx]
        if pixel_class:  # Foreground
            fg_pixels.append(original_pixel)
        else:  # Background
            bg_pixels.append(original_pixel)
    
    # Generate bit pattern (True = foreground)
    pattern_bits = [
        bool(pixel_class) for pixel_class in duotone.getdata()
    ]
    
    return pattern_bits, fg_pixels, bg_pixels


def compute_centroid(pixels: List[Tuple[int, int, int]]) -> Tuple[int, int, int]:
    """
    Compute RGB centroid (average) of pixel list.
    
    Args:
        pixels: List of (r, g, b) tuples
    
    Returns:
        (r, g, b) tuple with averaged values
    
    Example:
        >>> pixels = [(255, 0, 0), (200, 50, 0)]
        >>> compute_centroid(pixels)
        (227, 25, 0)
    """
    n = len(pixels)
    if n == 0:
        return (0, 0, 0)
    
    r_sum = sum(p[0] for p in pixels)
    g_sum = sum(p[1] for p in pixels)
    b_sum = sum(p[2] for p in pixels)
    
    return (r_sum // n, g_sum // n, b_sum // n)


def pattern_to_index(pattern_bits: List[bool]) -> int:
    """
    Convert bit pattern to character lookup index.
    
    Args:
        pattern_bits: List of bools in row-major order
    
    Returns:
        Integer index (0 to 2^n - 1)
    
    Example:
        >>> pattern_to_index([True, False, False, True])  # Bits 0 and 3 set
        9  # 2^0 + 2^3
    """
    index = 0
    for i, bit in enumerate(pattern_bits):
        if bit:
            index += 2**i
    return index


def process_cell(
    cell_img: Image.Image,
    glut: List[str],
) -> Cell:
    """
    Convert pixel block to mosaic Cell using custom GLUT.
    
    This is the core primitive that combines all steps:
    1. Quantize to 2 colors
    2. Generate bit pattern
    3. Select character from GLUT
    4. Compute color centroids
    
    Args:
        cell_img: PIL Image of BASIS_X × BASIS_Y pixels
        glut: Character lookup table (from get_full_glut or get_pips_glut or custom)
    
    Returns:
        Cell object with character and colors
    
    Example:
        >>> cell_img = img.crop((0, 0, 2, 2))
        >>> glut = get_full_glut(BASIS.BASIS_2_2)
        >>> cell = process_cell(cell_img, glut)
        >>> print(cell.to_ansi())  # ANSI colored character
        
        >>> # Or with pips
        >>> glut = get_pips_glut(2, 2)
        >>> cell = process_cell(cell_img, glut)
    """
    # Quantize and classify pixels
    pattern_bits, fg_pixels, bg_pixels = quantize_cell(cell_img)
    
    # Generate character index and select from GLUT
    pattern_idx = pattern_to_index(pattern_bits)
    char = glut[min(pattern_idx, len(glut) - 1)]
    
    # Compute colors
    fg_color = compute_centroid(fg_pixels)
    bg_color = compute_centroid(bg_pixels)
    
    return Cell(char, fg_color, bg_color, pattern_idx)


def image_to_cells(
    image: Image.Image,
    width: int,
    height: int,
    glut: Optional[List[str]] = None,
    basis: Optional[BASIS] = None,
) -> List[List[Cell]]:
    """
    Convert PIL Image to 2D grid of mosaic Cells.
    
    Resizes image to exact dimensions needed, then processes each
    BASIS_X × BASIS_Y block into a Cell.
    
    Args:
        image: PIL Image (any size, will be resized)
        width: Output width in terminal characters
        height: Output height in terminal characters
        glut: Character lookup table (optional, uses full blocks if None)
        basis: BASIS level (required if glut not provided)
    
    Returns:
        2D list: cells[y][x] = Cell
    
    Examples:
        >>> # Default (full blocks, BASIS 2,2)
        >>> cells = image_to_cells(img, 80, 40, basis=BASIS.BASIS_2_2)
        
        >>> # With pips
        >>> glut = get_pips_glut(2, 4)
        >>> cells = image_to_cells(img, 80, 40, glut=glut)
        
        >>> # Custom GLUT
        >>> custom_glut = [' ', '░', '▒', '▓', '█']  # 4-level grayscale
        >>> cells = image_to_cells(img, 80, 40, glut=custom_glut)
    
    Use this for:
    - Custom TUI layouts
    - Mixed text/graphics
    - Animation frame preprocessing
    - Integration with terminal libraries
    """
    # Determine GLUT and BASIS dimensions
    if glut is None:
        if basis is None:
            raise ValueError("Must provide either 'glut' or 'basis'")
        glut = get_full_glut(basis)
        basis_x, basis_y = basis.value
    else:
        # Infer basis from GLUT size
        num_patterns = len(glut)
        # Find basis that produces this many patterns (2^(x*y))
        import math
        total_bits = int(math.log2(num_patterns))
        # Common basis dimensions
        if total_bits == 2:  # 4 patterns
            basis_x, basis_y = 1, 2
        elif total_bits == 4:  # 16 patterns
            basis_x, basis_y = 2, 2
        elif total_bits == 6:  # 64 patterns
            basis_x, basis_y = 2, 3
        elif total_bits == 8:  # 256 patterns
            basis_x, basis_y = 2, 4
        else:
            raise ValueError(f"Cannot infer BASIS from GLUT size {num_patterns}")
    
    # Convert to RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to exact pixel dimensions
    pixel_width = width * basis_x
    pixel_height = height * basis_y
    img_resized = image.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
    
    # Process each cell
    cells = []
    for y in range(height):
        row = []
        for x in range(width):
            # Extract pixel block
            block_x = x * basis_x
            block_y = y * basis_y
            cell_img = img_resized.crop((
                block_x,
                block_y,
                block_x + basis_x,
                block_y + basis_y,
            ))
            
            # Process to Cell
            cell = process_cell(cell_img, glut)
            row.append(cell)
        
        cells.append(row)
    
    return cells


def cells_to_ansi_lines(cells: List[List[Cell]]) -> List[str]:
    """
    Convert 2D Cell grid to ANSI-formatted text lines.
    
    Args:
        cells: 2D list from image_to_cells()
    
    Returns:
        List of strings (one per row) with ANSI codes
    
    Example:
        >>> cells = image_to_cells(img, 80, 40, basis=BASIS.BASIS_2_2)
        >>> lines = cells_to_ansi_lines(cells)
        >>> for line in lines:
        ...     print(line)  # Displays in terminal
    """
    lines = []
    for row in cells:
        line_parts = [cell.to_ansi() for cell in row]
        lines.append(''.join(line_parts))
    return lines


# Convenience function for quick experiments
def render_image_ansi(
    image: Image.Image,
    width: int = 80,
    height: Optional[int] = None,
    basis: BASIS = BASIS.BASIS_2_2,
    pips: bool = False,
) -> str:
    """
    One-line image to ANSI string conversion.
    
    Quick utility for experiments and demos.
    
    Args:
        image: PIL Image
        width: Terminal width
        height: Terminal height (auto-calculated if None)
        basis: BASIS level
        pips: Use pips (Braille-style) instead of full blocks
    
    Returns:
        Complete ANSI string ready to print
    
    Example:
        >>> from PIL import Image
        >>> from catpic.primitives import render_image_ansi
        >>> img = Image.open('photo.jpg')
        >>> ansi = render_image_ansi(img, width=60)
        >>> print(ansi)  # Displays image
        
        >>> # With pips
        >>> ansi = render_image_ansi(img, width=60, pips=True)
    """
    # Auto-calculate height
    if height is None:
        aspect_ratio = image.height / image.width
        height = int(width * aspect_ratio * 0.5)
    
    # Get GLUT
    if pips:
        basis_x, basis_y = basis.value
        glut = get_pips_glut(basis_x, basis_y)
        cells = image_to_cells(image, width, height, glut=glut)
    else:
        # Fixed: Pass basis as keyword argument
        cells = image_to_cells(image, width, height, basis=basis)
    
    lines = cells_to_ansi_lines(cells)
    return '\n'.join(lines)
