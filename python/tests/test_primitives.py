"""Tests for catpic primitives API."""

import pytest
from PIL import Image

from catpic import BASIS
from catpic.primitives import (
    Cell,
    compute_centroid,
    get_full_glut,
    get_pips_glut,
    image_to_cells,
    pattern_to_index,
    process_cell,
    quantize_cell,
    render_image_ansi,
)


class TestCell:
    """Test Cell class."""
    
    def test_cell_creation(self):
        """Test Cell creation."""
        cell = Cell("█", (255, 0, 0), (0, 0, 255), 15)
        assert cell.char == "█"
        assert cell.fg_rgb == (255, 0, 0)
        assert cell.bg_rgb == (0, 0, 255)
        assert cell.pattern == 15
    
    def test_cell_to_ansi(self):
        """Test Cell ANSI conversion."""
        cell = Cell("▚", (255, 0, 0), (0, 255, 0), 9)
        ansi = cell.to_ansi()
        assert "\x1b[38;2;255;0;0m" in ansi
        assert "\x1b[48;2;0;255;0m" in ansi
        assert "▚" in ansi
        assert "\x1b[0m" in ansi


class TestGLUT:
    """Test GLUT functions."""
    
    def test_get_full_glut_2_2(self):
        """Test full GLUT for BASIS 2,2."""
        glut = get_full_glut(BASIS.BASIS_2_2)
        assert len(glut) == 16
        assert glut[0] == " "
        assert glut[15] == "█"
    
    def test_get_full_glut_2_4(self):
        """Test full GLUT for BASIS 2,4."""
        glut = get_full_glut(BASIS.BASIS_2_4)
        assert len(glut) == 256
    
    def test_get_pips_glut_2_2(self):
        """Test pips GLUT for 2×2."""
        glut = get_pips_glut(2, 2)
        assert len(glut) == 16
        assert glut[0] == " "
    
    def test_get_pips_glut_2_4(self):
        """Test pips GLUT for 2×4 (Braille)."""
        glut = get_pips_glut(2, 4)
        assert len(glut) == 256


class TestPrimitives:
    """Test primitive functions."""
    
    def test_compute_centroid(self):
        """Test RGB centroid calculation."""
        pixels = [(255, 0, 0), (205, 50, 0)]
        centroid = compute_centroid(pixels)
        assert centroid == (230, 25, 0)
    
    def test_compute_centroid_empty(self):
        """Test centroid with empty list."""
        centroid = compute_centroid([])
        assert centroid == (0, 0, 0)
    
    def test_pattern_to_index(self):
        """Test bit pattern to index conversion."""
        bits = [True, False, False, True]
        idx = pattern_to_index(bits)
        assert idx == 9  # 2^0 + 2^3
    
    def test_pattern_to_index_all_false(self):
        """Test all false pattern."""
        bits = [False, False, False, False]
        idx = pattern_to_index(bits)
        assert idx == 0
    
    def test_pattern_to_index_all_true(self):
        """Test all true pattern."""
        bits = [True, True, True, True]
        idx = pattern_to_index(bits)
        assert idx == 15  # 2^0 + 2^1 + 2^2 + 2^3


class TestImageProcessing:
    """Test image processing functions."""
    
    def test_quantize_cell(self):
        """Test cell quantization."""
        # Create 2×2 test image
        img = Image.new('RGB', (2, 2))
        img.putpixel((0, 0), (255, 0, 0))
        img.putpixel((1, 0), (0, 0, 0))
        img.putpixel((0, 1), (0, 0, 0))
        img.putpixel((1, 1), (255, 0, 0))
        
        bits, fg, bg = quantize_cell(img)
        assert len(bits) == 4
        assert len(fg) > 0 or len(bg) > 0
    
    def test_process_cell(self):
        """Test complete cell processing."""
        img = Image.new('RGB', (2, 2), (128, 128, 128))
        glut = get_full_glut(BASIS.BASIS_2_2)
        
        cell = process_cell(img, glut)
        assert isinstance(cell, Cell)
        assert cell.char in glut
        assert len(cell.fg_rgb) == 3
        assert len(cell.bg_rgb) == 3
    
    def test_image_to_cells_basic(self):
        """Test image to cells conversion."""
        img = Image.new('RGB', (40, 20), (128, 128, 128))
        cells = image_to_cells(img, 20, 10, basis=BASIS.BASIS_2_2)
        
        assert len(cells) == 10  # Height
        assert len(cells[0]) == 20  # Width
        assert isinstance(cells[0][0], Cell)
    
    def test_image_to_cells_with_pips(self):
        """Test image to cells with pips GLUT."""
        img = Image.new('RGB', (40, 20), (128, 128, 128))
        glut = get_pips_glut(2, 2)
        cells = image_to_cells(img, 20, 10, glut=glut)
        
        assert len(cells) == 10
        assert len(cells[0]) == 20
    
    def test_render_image_ansi(self):
        """Test quick ANSI rendering."""
        img = Image.new('RGB', (40, 20), (128, 128, 128))
        ansi = render_image_ansi(img, width=20, height=10)
        
        assert isinstance(ansi, str)
        assert len(ansi) > 0
        assert "\x1b[" in ansi  # Contains ANSI codes
