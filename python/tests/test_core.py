"""Tests for catpic core functionality."""

import pytest

from catpic.core import BASIS, CatpicCore, get_default_basis


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
        # All BASIS levels should have character sets
        for basis in BASIS:
            assert basis in CatpicCore.BLOCKS
            blocks = CatpicCore.BLOCKS[basis]
            assert len(blocks) > 0
            assert isinstance(blocks[0], str)
    
    def test_basis_1_2_blocks(self):
        """Test BASIS 1,2 has correct number of blocks."""
        blocks = CatpicCore.BLOCKS[BASIS.BASIS_1_2]
        assert len(blocks) == 4
        assert " " in blocks
        assert "█" in blocks
    
    def test_basis_2_2_blocks(self):
        """Test BASIS 2,2 has correct number of blocks."""
        blocks = CatpicCore.BLOCKS[BASIS.BASIS_2_2]
        assert len(blocks) == 16
        assert " " in blocks
        assert "█" in blocks
    
    def test_basis_2_3_blocks(self):
        """Test BASIS 2,3 has 64 blocks."""
        blocks = CatpicCore.BLOCKS[BASIS.BASIS_2_3]
        assert len(blocks) == 64
    
    def test_basis_2_4_blocks(self):
        """Test BASIS 2,4 has 256 blocks."""
        blocks = CatpicCore.BLOCKS[BASIS.BASIS_2_4]
        assert len(blocks) == 256
    
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


class TestGetDefaultBasis:
    """Test environment variable BASIS selection."""
    
    def test_default_without_env(self, monkeypatch):
        """Test default BASIS when no env var set."""
        monkeypatch.delenv("CATPIC_BASIS", raising=False)
        basis = get_default_basis()
        assert basis == BASIS.BASIS_2_2
    
    def test_env_var_comma(self, monkeypatch):
        """Test BASIS from env var with comma format."""
        monkeypatch.setenv("CATPIC_BASIS", "2,4")
        basis = get_default_basis()
        assert basis == BASIS.BASIS_2_4
    
    def test_env_var_x(self, monkeypatch):
        """Test BASIS from env var with x format."""
        monkeypatch.setenv("CATPIC_BASIS", "2x3")
        basis = get_default_basis()
        assert basis == BASIS.BASIS_2_3
    
    def test_env_var_invalid(self, monkeypatch):
        """Test invalid env var falls back to default."""
        monkeypatch.setenv("CATPIC_BASIS", "invalid")
        basis = get_default_basis()
        assert basis == BASIS.BASIS_2_2
