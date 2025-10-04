    def encode_animation(
        self, 
        gif_path: Union[str, Path],
        width: Optional[int] = None,
        height: Optional[int] = None,
        delay: Optional[int] = None
    ) -> str:
        """
        Encode animated GIF to MEOW animation format.
        
        Placeholder implementation for# ---
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

"""catpic image encoding functionality."""

import io
from pathlib import Path
from typing import Optional, Tuple, Union

from PIL import Image, ImageSequence

from .core import BASIS, CatpicCore


class CatpicEncoder:
    """Encoder for converting images to MEOW format (Mosaic Encoding Over Wire)."""
    
    def __init__(self, basis: BASIS = BASIS.BASIS_2_2):
        """Initialize encoder with specified BASIS level."""
        self.basis = basis
        self.core = CatpicCore()
        
    def encode_image(
        self, 
        image_path: Union[str, Path], 
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> str:
        """
        Encode a single image to MEOW format.
        
        This is a placeholder implementation. Phase 1 development will implement
        the full EnGlyph-based algorithm:
        
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
                # Maintain aspect ratio
                aspect_ratio = img.height / img.width
                height = int(width * aspect_ratio * 0.5)  # Terminal char aspect correction
            
            # Placeholder: Simple character-based representation
            # Real implementation will use EnGlyph algorithm
            basis_x, basis_y = self.core.get_basis_dimensions(self.basis)
            pixel_width = width * basis_x
            pixel_height = height * basis_y
            
            # Resize image
            img_resized = img.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
            
            # Generate MEOW header
            lines = [
                "MEOW/1.0",
                f"WIDTH:{width}",
                f"HEIGHT:{height}",
                f"BASIS:{basis_x},{basis_y}",
                "DATA:",
            ]
            
            # Placeholder implementation - will be replaced with EnGlyph algorithm
            for y in range(height):
                line_chars = []
                for x in range(width):
                    # Extract pixel block
                    block_x = x * basis_x
                    block_y = y * basis_y
                    
                    # Simple averaging for placeholder
                    pixel_sum_r, pixel_sum_g, pixel_sum_b = 0, 0, 0
                    pixel_count = 0
                    
                    for py in range(block_y, min(block_y + basis_y, pixel_height)):
                        for px in range(block_x, min(block_x + basis_x, pixel_width)):
                            r, g, b = img_resized.getpixel((px, py))
                            pixel_sum_r += r
                            pixel_sum_g += g
                            pixel_sum_b += b
                            pixel_count += 1
                    
                    if pixel_count > 0:
                        avg_r = pixel_sum_r // pixel_count
                        avg_g = pixel_sum_g // pixel_count
                        avg_b = pixel_sum_b // pixel_count
                    else:
                        avg_r = avg_g = avg_b = 0
                    
                    # Simple block selection (placeholder)
                    blocks = self.core.BLOCKS[self.basis]
                    intensity = (avg_r + avg_g + avg_b) // 3
                    block_idx = min(intensity * len(blocks) // 256, len(blocks) - 1)
                    char = blocks[block_idx]
                    
                    # Format with colors (placeholder - simplified)
                    cell = self.core.format_cell(char, (avg_r, avg_g, avg_b), (0, 0, 0))
                    line_chars.append(cell)
                
                lines.append("".join(line_chars))
            
            return "\n".join(lines)
    
    def encode_animation(
        self, 
        gif_path: Union[str, Path],
        width: Optional[int] = None,
        height: Optional[int] = None,
        delay: Optional[int] = None
    ) -> str:
        """
        Encode animated GIF to MEOW animation format.
        
        Placeholder implementation for Phase 2 development.
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
            
            # Encode each frame (placeholder)
            for frame_idx in range(frame_count):
                img.seek(frame_idx)
                frame = img.copy().convert('RGB')
                
                lines.append(f"FRAME:{frame_idx}")
                
                # Use the same encoding logic as single images
                # This is simplified for placeholder - real implementation
                # will optimize for animation-specific requirements
                basis_x, basis_y = self.core.get_basis_dimensions(self.basis)
                pixel_width = width * basis_x
                pixel_height = height * basis_y
                frame_resized = frame.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
                
                for y in range(height):
                    line_chars = []
                    for x in range(width):
                        # Simplified placeholder encoding
                        block_x = x * basis_x
                        block_y = y * basis_y
                        
                        # Sample center pixel of block
                        center_x = block_x + basis_x // 2
                        center_y = block_y + basis_y // 2
                        center_x = min(center_x, pixel_width - 1)
                        center_y = min(center_y, pixel_height - 1)
                        
                        r, g, b = frame_resized.getpixel((center_x, center_y))
                        
                        # Simple character selection
                        blocks = self.core.BLOCKS[self.basis]
                        intensity = (r + g + b) // 3
                        block_idx = min(intensity * len(blocks) // 256, len(blocks) - 1)
                        char = blocks[block_idx]
                        
                        cell = self.core.format_cell(char, (r, g, b), (0, 0, 0))
                        line_chars.append(cell)
                    
                    lines.append("".join(line_chars))
            
            return "\n".join(lines) Phase 2 development.
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
            
            # Generate TIMA header
            basis_x, basis_y = self.core.get_basis_dimensions(self.basis)
            lines = [
                "TIMA/1.0",
                f"WIDTH:{width}",
                f"HEIGHT:{height}",
                f"BASIS:{basis_x},{basis_y}",
                f"FRAMES:{frame_count}",
                f"DELAY:{delay}",
                "DATA:",
            ]
            
            # Encode each frame (placeholder)
            for frame_idx in range(frame_count):
                img.seek(frame_idx)
                frame = img.copy().convert('RGB')
                
                lines.append(f"FRAME:{frame_idx}")
                
                # Use the same encoding logic as single images
                # This is simplified for placeholder - real implementation
                # will optimize for animation-specific requirements
                basis_x, basis_y = self.core.get_basis_dimensions(self.basis)
                pixel_width = width * basis_x
                pixel_height = height * basis_y
                frame_resized = frame.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
                
                for y in range(height):
                    line_chars = []
                    for x in range(width):
                        # Simplified placeholder encoding
                        block_x = x * basis_x
                        block_y = y * basis_y
                        
                        # Sample center pixel of block
                        center_x = block_x + basis_x // 2
                        center_y = block_y + basis_y // 2
                        center_x = min(center_x, pixel_width - 1)
                        center_y = min(center_y, pixel_height - 1)
                        
                        r, g, b = frame_resized.getpixel((center_x, center_y))
                        
                        # Simple character selection
                        blocks = self.core.BLOCKS[self.basis]
                        intensity = (r + g + b) // 3
                        block_idx = min(intensity * len(blocks) // 256, len(blocks) - 1)
                        char = blocks[block_idx]
                        
                        cell = self.core.format_cell(char, (r, g, b), (0, 0, 0))
                        line_chars.append(cell)
                    
                    lines.append("".join(line_chars))
            
            return "\n".join(lines)