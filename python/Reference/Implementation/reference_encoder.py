# ---
# ## AI Collaboration Context
# **Project:** catpic - Terminal Image Viewer | **Session:** #1 | **Date:** 2025-01-27 | **Lead:** [Your Name]  
# **AI Model:** Claude Sonnet 4 | **Objective:** Create comprehensive catpic project structure
# **Prior Work:** Initial session  
# **Current Status:** Complete project scaffolding with BASIS system and EnGlyph integration. Renamed to catpic with .meow extension
# **Files in Scope:** New project - all files created  
# **Human Contributions:** Requirements analysis, EnGlyph research, BASIS system design, development strategy, UX design (viewer-first approach), naming (catpic/.meow)  
# **AI Contributions:** Project structure, code generation, documentation, testing framework  
# **Pending Decisions:** Phase 1 implementation approach, specific BASIS character sets for 2,3 and 2,4
# ---

"""
Reference implementation of catpic encoder algorithm.

This standalone script demonstrates the core EnGlyph-based algorithm
for converting images to MEOW format. Use this as a reference for
implementing the production CatpicEncoder class.
"""

from PIL import Image
import sys
from typing import Tuple, List


def create_test_image():
    """Create a simple test image for demonstration."""
    img = Image.new('RGB', (40, 20), color='white')
    pixels = img.load()
    
    # Create simple pattern
    for y in range(20):
        for x in range(40):
            if (x + y) % 8 < 4:
                pixels[x, y] = (255, 0, 0)  # Red
            else:
                pixels[x, y] = (0, 0, 255)  # Blue
    
    return img


def extract_pixel_block(img: Image.Image, char_x: int, char_y: int, basis_x: int, basis_y: int) -> List[Tuple[int, int, int]]:
    """Extract pixel block for a character position."""
    pixels = []
    pixel_x_start = char_x * basis_x
    pixel_y_start = char_y * basis_y
    
    for py in range(pixel_y_start, pixel_y_start + basis_y):
        for px in range(pixel_x_start, pixel_x_start + basis_x):
            if px < img.width and py < img.height:
                pixels.append(img.getpixel((px, py)))
            else:
                pixels.append((0, 0, 0))  # Black for out-of-bounds
    
    return pixels


def quantize_block(pixels: List[Tuple[int, int, int]]) -> Tuple[List[bool], Tuple[int, int, int], Tuple[int, int, int]]:
    """
    Quantize pixel block to 2 colors using EnGlyph approach.
    Returns: (bit_pattern, foreground_rgb, background_rgb)
    """
    # Create temporary image for quantization
    block_img = Image.new('RGB', (len(pixels), 1))
    block_img.putdata(pixels)
    
    # Quantize to 2 colors (EnGlyph method)
    quantized = block_img.quantize(colors=2, method=Image.Quantize.MEDIANCUT)
    quantized_rgb = quantized.convert('RGB')
    
    # Get quantized pixels
    quantized_pixels = list(quantized_rgb.getdata())
    
    # Find the two colors
    unique_colors = list(set(quantized_pixels))
    if len(unique_colors) == 1:
        unique_colors.append((0, 0, 0))  # Add black as second color
    
    color1, color2 = unique_colors[:2]
    
    # Determine which color is "foreground" (brighter)
    brightness1 = sum(color1) / 3
    brightness2 = sum(color2) / 3
    
    if brightness1 > brightness2:
        fg_color, bg_color = color1, color2
    else:
        fg_color, bg_color = color2, color1
    
    # Generate bit pattern (EnGlyph method)
    pattern_bits = []
    for pixel in quantized_pixels:
        pattern_bits.append(pixel == fg_color)
    
    return pattern_bits, fg_color, bg_color


def generate_bit_pattern_index(pattern_bits: List[bool]) -> int:
    """Generate bit pattern index (EnGlyph method)."""
    index = 0
    for i, bit in enumerate(pattern_bits):
        if bit:
            index += 2**i
    return index


def get_unicode_char(pattern_index: int, basis_x: int, basis_y: int) -> str:
    """Get Unicode character for bit pattern."""
    # BASIS 2,2 quadrant blocks (EnGlyph proven set)
    if basis_x == 2 and basis_y == 2:
        blocks = [
            " ", "▘", "▝", "▀",  # 0000, 0001, 0010, 0011
            "▖", "▌", "▞", "▛",  # 0100, 0101, 0110, 0111
            "▗", "▚", "▐", "▜",  # 1000, 1001, 1010, 1011
            "▄", "▙", "▟", "█",  # 1100, 1101, 1110, 1111
        ]
        return blocks[min(pattern_index, len(blocks) - 1)]
    
    # BASIS 1,2 half blocks
    elif basis_x == 1 and basis_y == 2:
        blocks = [" ", "▀", "▄", "█"]
        return blocks[min(pattern_index, len(blocks) - 1)]
    
    # Fallback
    else:
        intensity = pattern_index / (2**(basis_x * basis_y) - 1)
        if intensity < 0.25:
            return " "
        elif intensity < 0.5:
            return "░"
        elif intensity < 0.75:
            return "▒"
        else:
            return "█"


def format_ansi_cell(char: str, fg_rgb: Tuple[int, int, int], bg_rgb: Tuple[int, int, int]) -> str:
    """Format cell with ANSI colors."""
    fg_r, fg_g, fg_b = fg_rgb
    bg_r, bg_g, bg_b = bg_rgb
    
    return f"\x1b[38;2;{fg_r};{fg_g};{fg_b}m\x1b[48;2;{bg_r};{bg_g};{bg_b}m{char}\x1b[0m"


def encode_image_to_meow(img: Image.Image, width: int, height: int, basis_x: int = 2, basis_y: int = 2) -> str:
    """
    Reference implementation of MEOW encoding using EnGlyph algorithm.
    """
    # Resize image to match character grid
    pixel_width = width * basis_x
    pixel_height = height * basis_y
    img_resized = img.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
    
    # Generate header
    lines = [
        "MEOW/1.0",
        f"WIDTH:{width}",
        f"HEIGHT:{height}",
        f"BASIS:{basis_x},{basis_y}",
        "DATA:",
    ]
    
    # Process each character position
    for char_y in range(height):
        line_chars = []
        
        for char_x in range(width):
            # Extract pixel block
            pixels = extract_pixel_block(img_resized, char_x, char_y, basis_x, basis_y)
            
            # Quantize to 2 colors (EnGlyph method)
            pattern_bits, fg_color, bg_color = quantize_block(pixels)
            
            # Generate bit pattern index
            pattern_index = generate_bit_pattern_index(pattern_bits)
            
            # Get Unicode character
            char = get_unicode_char(pattern_index, basis_x, basis_y)
            
            # Format with ANSI colors
            cell = format_ansi_cell(char, fg_color, bg_color)
            line_chars.append(cell)
        
        lines.append("".join(line_chars))
    
    return "\n".join(lines)


def main():
    """Demonstrate reference encoder."""
    if len(sys.argv) > 1:
        # Load image from file
        try:
            img = Image.open(sys.argv[1]).convert('RGB')
        except Exception as e:
            print(f"Error loading image: {e}")
            return
    else:
        # Create test image
        img = create_test_image()
    
    # Encode to MEOW
    meow_data = encode_image_to_meow(img, width=20, height=10, basis_x=2, basis_y=2)
    
    # Output
    print("Reference MEOW Encoding:")
    print("=" * 50)
    print(meow_data)
    print("=" * 50)
    print("Save this output to a .meow file and view with 'cat filename.meow'")


if __name__ == '__main__':
    main()