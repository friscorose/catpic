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

"""Core catpic functionality and constants."""

from enum import Enum
from typing import Dict, List, Tuple


class BASIS(Enum):
    """BASIS system for catpic quality levels."""
    
    BASIS_1_2 = (1, 2)  # 4 patterns - Universal compatibility
    BASIS_2_2 = (2, 2)  # 16 patterns - Balanced
    BASIS_2_3 = (2, 3)  # 64 patterns - High quality  
    BASIS_2_4 = (2, 4)  # 256 patterns - Ultra quality


class CatpicCore:
    """Core catpic constants and Unicode character sets for mosaic encoding."""
    
    # Unicode block characters for different BASIS levels
    BLOCKS: Dict[BASIS, List[str]] = {
        BASIS.BASIS_1_2: [
            " ",  # Empty
            "▀",  # Upper half
            "▄",  # Lower half  
            "█",  # Full block
        ],
        
        BASIS.BASIS_2_2: [
            " ", "▘", "▝", "▀",  # 0000, 0001, 0010, 0011
            "▖", "▌", "▞", "▛",  # 0100, 0101, 0110, 0111
            "▗", "▚", "▐", "▜",  # 1000, 1001, 1010, 1011
            "▄", "▙", "▟", "█",  # 1100, 1101, 1110, 1111
        ],
        
        BASIS.BASIS_2_3: [
            # Sextant blocks 🬀-🬻 (64 patterns)
            # Full implementation would include all 64 sextant characters
            " ", "🬀", "🬁", "🬂", "🬃", "🬄", "🬅", "🬆",
            "🬇", "🬈", "🬉", "🬊", "🬋", "🬌", "🬍", "🬎",
            "🬏", "🬐", "🬑", "🬒", "🬓", "🬔", "🬕", "🬖",
            "🬗", "🬘", "🬙", "🬚", "🬛", "🬜", "🬝", "🬞",
            "🬟", "🬠", "🬡", "🬢", "🬣", "🬤", "🬥", "🬦",
            "🬧", "🬨", "🬩", "🬪", "🬫", "🬬", "🬭", "🬮",
            "🬯", "🬰", "🬱", "🬲", "🬳", "🬴", "🬵", "🬶",
            "🬷", "🬸", "🬹", "🬺", "🬻", "▀", "▄", "█",
        ],
        
        BASIS.BASIS_2_4: [
            # Legacy Computing Supplement 𜴀-𜷥 (256 patterns)
            # Placeholder - full implementation would include all 256 characters
            " ", "▘", "▝", "▀", "▖", "▌", "▞", "▛",
            "▗", "▚", "▐", "▜", "▄", "▙", "▟", "█",
            # ... additional 240 characters would be added here
        ],
    }
    
    # ANSI color format strings
    RESET = "\x1b[0m"
    FG_COLOR = "\x1b[38;2;{r};{g};{b}m"
    BG_COLOR = "\x1b[48;2;{r};{g};{b}m"
    
    @staticmethod
    def format_cell(char: str, fg_rgb: Tuple[int, int, int], bg_rgb: Tuple[int, int, int]) -> str:
        """Format a single cell with foreground/background colors."""
        fg_r, fg_g, fg_b = fg_rgb
        bg_r, bg_g, bg_b = bg_rgb
        
        return (
            f"\x1b[38;2;{fg_r};{fg_g};{fg_b}m"
            f"\x1b[48;2;{bg_r};{bg_g};{bg_b}m"
            f"{char}"
            f"\x1b[0m"
        )
    
    @staticmethod
    def get_basis_dimensions(basis: BASIS) -> Tuple[int, int]:
        """Get pixel dimensions for a BASIS level."""
        return basis.value