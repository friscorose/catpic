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

"""Create test images for catpic testing."""

from pathlib import Path
from PIL import Image, ImageDraw


def create_test_images():
    """Create basic test images for development."""
    fixtures_dir = Path(__file__).parent
    
    # Simple gradient image
    img = Image.new('RGB', (100, 50), color='white')
    draw = ImageDraw.Draw(img)
    
    # Create horizontal gradient
    for x in range(100):
        color_val = int(255 * x / 99)
        draw.line([(x, 0), (x, 49)], fill=(color_val, color_val, color_val))
    
    img.save(fixtures_dir / 'gradient.png')
    
    # Simple colored squares
    img = Image.new('RGB', (60, 60), color='white')
    draw = ImageDraw.Draw(img)
    
    # Red square
    draw.rectangle([5, 5, 25, 25], fill='red')
    # Green square  
    draw.rectangle([35, 5, 55, 25], fill='green')
    # Blue square
    draw.rectangle([5, 35, 25, 55], fill='blue')
    # Yellow square
    draw.rectangle([35, 35, 55, 55], fill='yellow')
    
    img.save(fixtures_dir / 'squares.png')
    
    print(f"Created test images in {fixtures_dir}")


if __name__ == '__main__':
    create_test_images()