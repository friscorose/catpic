"""catpic image encoding functionality."""

from pathlib import Path
from typing import Optional, Tuple, Union

from PIL import Image

from .core import BASIS, CatpicCore, get_default_basis


class CatpicEncoder:
    """Encoder for converting images to MEOW format (Mosaic Encoding Over Wire)."""
    
    def __init__(self, basis: Optional[Union[BASIS, Tuple[int, int]]] = None):
        """Initialize encoder with specified BASIS level.
        
        Args:
            basis: Either a BASIS enum, tuple (2, 2), or None.
                   If None, uses CATPIC_BASIS environment variable or defaults to BASIS_2_2.
        
        Environment:
            CATPIC_BASIS: Set default BASIS (e.g., "2,4" or "2x4" or "2_4")
        """
        # If no basis provided, check environment variable
        if basis is None:
            self.basis = get_default_basis()
        # Handle both BASIS enum and tuple formats
        elif isinstance(basis, tuple):
            # Convert tuple to BASIS enum
            basis_map = {
                (1, 2): BASIS.BASIS_1_2,
                (2, 2): BASIS.BASIS_2_2,
                (2, 3): BASIS.BASIS_2_3,
                (2, 4): BASIS.BASIS_2_4,
            }
            if basis not in basis_map:
                raise ValueError(f"Invalid BASIS tuple: {basis}. Must be one of {list(basis_map.keys())}")
            self.basis = basis_map[basis]
        else:
            self.basis = basis
        
        self.core = CatpicCore()
        
    def encode_image(
        self, 
        image_path: Union[str, Path], 
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> str:
        """
        Encode a single image to MEOW format using EnGlyph algorithm.
        
        Algorithm:
        1. Resize image to WIDTH×BASIS_X by HEIGHT×BASIS_Y pixels
        2. For each cell: Extract BASIS_X×BASIS_Y pixel block  
        3. Quantize to 2 colors using PIL.quantize(colors=2)
        4. Generate bit pattern: pattern += 2**i for each lit pixel
        5. Select Unicode character: blocks[pattern]
        6. Compute RGB centroids for foreground/background
        7. Output ANSI color sequence
        """
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate dimensions
            if width is None:
                width = 80  # Default terminal width
            if height is None:
                # Maintain aspect ratio with terminal character aspect correction
                aspect_ratio = img.height / img.width
                height = int(width * aspect_ratio * 0.5)
            
            # Get BASIS dimensions
            basis_x, basis_y = self.core.get_basis_dimensions(self.basis)
            pixel_width = width * basis_x
            pixel_height = height * basis_y
            
            # Resize image to exact pixel dimensions needed
            img_resized = img.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
            
            # Generate MEOW header
            lines = [
                "MEOW/1.0",
                f"WIDTH:{width}",
                f"HEIGHT:{height}",
                f"BASIS:{basis_x},{basis_y}",
                "DATA:",
            ]
            
            # Get character lookup table for this BASIS level
            blocks = self.core.BLOCKS[self.basis]
            
            # Process each cell using EnGlyph algorithm
            for y in range(height):
                line_chars = []
                for x in range(width):
                    # Extract pixel block for this cell
                    block_x = x * basis_x
                    block_y = y * basis_y
                    cell_img = img_resized.crop((
                        block_x, 
                        block_y, 
                        block_x + basis_x, 
                        block_y + basis_y
                    ))
                    
                    # Apply EnGlyph algorithm to this cell
                    glut_idx, fg_color, bg_color = self._cell_to_glyph(cell_img)
                    char = blocks[glut_idx]
                    
                    # Format with ANSI colors
                    cell = self.core.format_cell(char, fg_color, bg_color)
                    line_chars.append(cell)
                
                lines.append("".join(line_chars))
            
            return "\n".join(lines)
    
    def _cell_to_glyph(self, cell_img: Image.Image) -> Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]:
        """
        Convert a pixel block to glyph index and colors using EnGlyph algorithm.
        
        This is the core algorithm from toglyxels.py:_img4cell2vals4seg()
        
        Algorithm steps:
        1. Quantize block to 2 colors using PIL median cut
        2. Classify each pixel as foreground (1) or background (0)
        3. Generate bit pattern: sum of 2^i for each foreground pixel (row-major order)
        4. Separate original pixels into fg/bg sets based on classification
        5. Compute RGB centroids (averages) for each set
        
        Example (BASIS 2,2):
            Pixels:     Quantized:    Bit Pattern:
            [R][B]      [1][0]        pattern = 2^0 = 1
            [B][R]  ->  [0][1]    ->  pattern += 2^3 = 9
            
            Result: blocks[9] = "▚" with red fg, blue bg
        
        Returns:
            (glut_index, fg_rgb, bg_rgb)
        """
        fg_pixels = []
        bg_pixels = []
        glut_idx = 0
        
        # Step 1: Quantize to 2 colors using median cut algorithm
        # PIL's quantize(colors=2) uses median cut to find two representative
        # colors that best represent the block's color distribution
        duotone = cell_img.quantize(colors=2)
        
        # Step 2 & 3: Build bit pattern and separate fg/bg pixels
        # Pixel at index i contributes 2^i to pattern if classified as foreground
        for idx, pixel_class in enumerate(list(duotone.getdata())):
            if pixel_class:  # Foreground pixel
                fg_pixels.append(cell_img.getdata()[idx])
                glut_idx += 2**idx  # Bit pattern generation
            else:  # Background pixel
                bg_pixels.append(cell_img.getdata()[idx])
        
        # Step 4: Compute color centroids (arithmetic mean of RGB values)
        fg_color = self._compute_centroid(fg_pixels)
        bg_color = self._compute_centroid(bg_pixels)
        
        return (glut_idx, fg_color, bg_color)
    
    def _compute_centroid(self, rgb_list) -> Tuple[int, int, int]:
        """
        Compute RGB centroid (average) from list of RGB tuples.
        
        Centroid = arithmetic mean of all pixel values in the set.
        This provides the representative color for either foreground
        or background pixels in a block.
        
        From toglyxels.py:_colors2rgb4sty()
        
        Args:
            rgb_list: List of (r, g, b) tuples
        
        Returns:
            (r, g, b) tuple with averaged values
        
        Example:
            [(255, 0, 0), (200, 50, 0)] -> (227, 25, 0)
        """
        n = len(rgb_list)
        if n == 0:
            return (0, 0, 0)
        
        r_sum = g_sum = b_sum = 0
        for r, g, b in rgb_list:
            r_sum += r
            g_sum += g
            b_sum += b
        
        return (r_sum // n, g_sum // n, b_sum // n)
    
    def encode_animation(
        self, 
        gif_path: Union[str, Path],
        width: Optional[int] = None,
        height: Optional[int] = None,
        delay: Optional[int] = None
    ) -> str:
        """
        Encode animated GIF to MEOW animation format.
        
        Uses the same EnGlyph algorithm per frame.
        """
        with Image.open(gif_path) as img:
            if not getattr(img, 'is_animated', False):
                raise ValueError("Input file is not an animated image")
            
            # Get animation properties
            frame_count = getattr(img, 'n_frames', 1)
            if delay is None:
                delay = img.info.get('duration', 100)
            
            # Calculate dimensions
            if width is None:
                width = 60  # Smaller default for animations
            if height is None:
                aspect_ratio = img.height / img.width
                height = int(width * aspect_ratio * 0.5)
            
            # Generate MEOW animation header
            basis_x, basis_y = self.core.get_basis_dimensions(self.basis)
            lines = [
                "MEOW-ANIM/1.0",
                f"WIDTH:{width}",
                f"HEIGHT:{height}",
                f"BASIS:{basis_x},{basis_y}",
                f"FRAMES:{frame_count}",
                f"DELAY:{delay}",
                "DATA:",
            ]
            
            # Get character lookup table
            blocks = self.core.BLOCKS[self.basis]
            pixel_width = width * basis_x
            pixel_height = height * basis_y
            
            # Encode each frame
            for frame_idx in range(frame_count):
                img.seek(frame_idx)
                frame = img.copy().convert('RGB')
                frame_resized = frame.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
                
                lines.append(f"FRAME:{frame_idx}")
                
                # Process frame using same cell encoding
                for y in range(height):
                    line_chars = []
                    for x in range(width):
                        block_x = x * basis_x
                        block_y = y * basis_y
                        cell_img = frame_resized.crop((
                            block_x,
                            block_y,
                            block_x + basis_x,
                            block_y + basis_y
                        ))
                        
                        # Apply EnGlyph algorithm
                        glut_idx, fg_color, bg_color = self._cell_to_glyph(cell_img)
                        char = blocks[glut_idx]
                        cell = self.core.format_cell(char, fg_color, bg_color)
                        line_chars.append(cell)
                    
                    lines.append("".join(line_chars))
            
            return "\n".join(lines)
