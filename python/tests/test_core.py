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

"""Tests for catpic core functionality."""

import pytest

from catpic.core import BASIS, CatpicCore


class TestBASIS:
    """Test BASIS enum functionality."""
    
    def test_basis_values(self):
        """Test BASIS enum values are correct."""
        assert BASIS.BASIS_1_2.value == (1, 2)
        assert BASIS.BASIS_2_2.value == (2, 2)
        assert BASIS.BASIS_2_3.value == (2, 3)
        assert BASIS.BASIS_2_4.value == (2, 4)


class TestCatpicCore:
    """Test CatpicCore functionality."""
    
    def test_block_character_sets_exist(self):
        """Test that Unicode block character sets are defined."""
        core = CatpicCore()
        
        # All BASIS levels should have character sets
        for basis in BASIS:
            assert basis in core.BLOCKS
            blocks = core.BLOCKS[basis]
            assert len(blocks) > 0
            assert isinstance(blocks[0], str)
    
    def test_basis_1_2_blocks(self):
        """Test BASIS 1,2 has correct number of blocks."""
        core = CatpicCore()
        blocks = core.BLOCKS[BASIS.BASIS_1_2]
        assert len(blocks) == 4
        assert " " in blocks
        assert "█" in blocks
    
    def test_basis_2_2_blocks(self):
        """Test BASIS 2,2 has correct number of blocks."""
        core = CatpicCore()
        blocks = core.BLOCKS[BASIS.BASIS_2_2]
        assert len(blocks) == 16
        assert " " in blocks
        assert "█" in blocks
    
    def test_format_cell(self):
        """Test cell formatting with ANSI colors."""
        result = CatpicCore.format_cell("█", (255, 0, 0), (0, 255, 0))
        
        # Should contain ANSI escape sequences
        assert "\x1b[38;2;255;0;0m" in result  # Foreground red
        assert "\x1b[48;2;0;255;0m" in result  # Background green
        assert "█" in result  # Character
        assert "\x1b[0m" in result  # Reset
    
    def test_get_basis_dimensions(self):
        """Test BASIS dimension extraction."""
        assert CatpicCore.get_basis_dimensions(BASIS.BASIS_1_2) == (1, 2)
        assert CatpicCore.get_basis_dimensions(BASIS.BASIS_2_2) == (2, 2)
        assert CatpicCore.get_basis_dimensions(BASIS.BASIS_2_3) == (2, 3)
        assert CatpicCore.get_basis_dimensions(BASIS.BASIS_2_4) == (2, 4)