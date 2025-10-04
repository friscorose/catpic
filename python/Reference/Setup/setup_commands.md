---
## AI Collaboration Context
**Project:** catpic - Terminal Image Viewer | **Session:** #1 | **Date:** 2025-01-27 | **Lead:** [Your Name]  
**AI Model:** Claude Sonnet 4 | **Objective:** Create comprehensive catpic project structure
**Prior Work:** Initial session  
**Current Status:** Complete project scaffolding with BASIS system and EnGlyph integration. Renamed to catpic with .meow extension
**Files in Scope:** New project - all files created  
**Human Contributions:** Requirements analysis, EnGlyph research, BASIS system design, development strategy, UX design (viewer-first approach), naming (catpic/.meow)  
**AI Contributions:** Project structure, code generation, documentation, testing framework  
**Pending Decisions:** Phase 1 implementation approach, specific BASIS character sets for 2,3 and 2,4
---

# catpic Development Setup Commands

## Initial Setup

### Clone and Setup Repository
```bash
# Clone repository
git clone <repository-url>
cd catpic

# Initialize UV environment
uv sync --dev

# Activate virtual environment  
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate     # Windows

# Verify installation
uv run python -c "import catpic; print('catpic package loaded successfully')"
```

### Install Development Dependencies
```bash
# Install all dependencies including dev tools
uv sync --dev

# Or install specific dev tools
uv add --dev pytest black ruff mypy types-pillow
```

## Development Workflow

### Code Formatting and Linting
```bash
# Format code with Black
uv run black src/ tests/ examples/

# Check code with Ruff
uv run ruff check src/ tests/ examples/

# Fix auto-fixable issues
uv run ruff check --fix src/ tests/ examples/

# Type checking with mypy
uv run mypy src/
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/catpic --cov-report=html

# Run specific test file
uv run pytest tests/test_core.py

# Run tests with verbose output
uv run pytest -v

# Create test images (run once)
uv run python tests/fixtures/create_test_images.py
```

### Package Development
```bash
# Install package in development mode
uv pip install -e .

# Build package
uv build

# Test CLI installation
uv run catpic --help
```

## Usage Examples

### Basic Image Display
```bash
# Display image directly (primary use case)
uv run catpic photo.jpg

# Display with custom dimensions
uv run catpic photo.png --width 60 --height 30

# Use different BASIS level
uv run catpic image.jpg --basis 2,3

# Display animated GIF
uv run catpic animation.gif
```

### Generate Cat-able Files
```bash
# Generate .meow file from static image
uv run catpic generate image.jpg

# Generate with custom settings
uv run catpic generate photo.png --width 60 --output photo.meow

# Convert animated GIF to .meow
uv run catpic convert animation.gif

# Display .meow file
cat image.meow
uv run catpic image.meow

# Get file information
uv run catpic info image.meow
```

### Python API Usage
```bash
# Interactive development
uv run python

# Example session:
# >>> from catpic import CatpicEncoder, BASIS
# >>> encoder = CatpicEncoder(basis=BASIS.BASIS_2_2)
# >>> data = encoder.encode_image('image.jpg', width=40)
# >>> print(data)
```

## Development Tasks

### Phase 1 Development
```bash
# Run reference implementation
uv run python Reference/Implementation/reference-encoder.py

# Test core functionality
uv run pytest tests/test_core.py -v

# Validate format compliance
uv run python scripts/validate_format.py examples/sample.meow
```

### Phase 2 Development (Animation)
```bash
# Test animation encoding
uv run catpic convert test.gif --output test.meow

# Validate animation playback
uv run catpic test.meow

# Performance testing
uv run python -m cProfile -s cumtime -c "from catpic import CatpicEncoder; CatpicEncoder().encode_animation('large.gif')"
```

### Phase 3 Development (Integration)
```bash
# Test Textual integration (when implemented)
uv run python examples/textual_integration.py

# Performance benchmarks
uv run python scripts/benchmark_encoding.py

# Terminal compatibility testing
uv run python scripts/test_terminals.py
```

## Troubleshooting

### Common Issues

#### Unicode Display Problems
```bash
# Test Unicode support
echo "▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"
echo "🬀🬁🬂🬃🬄🬅🬆🬇"

# Check terminal capabilities
echo $TERM
locale charmap
```

#### Color Support Issues
```bash
# Test 24-bit color support
echo -e "\x1b[38;2;255;0;0mRed\x1b[38;2;0;255;0mGreen\x1b[38;2;0;0;255mBlue\x1b[0m"

# Check COLORTERM variable
echo $COLORTERM
```

#### Package Issues
```bash
# Clean and reinstall
uv clean
rm -rf .venv
uv sync --dev

# Rebuild package
uv build --clean
```

### Development Environment
```bash
# Check Python version
python --version  # Should be 3.8+

# Check UV version
uv --version

# List installed packages
uv pip list

# Check package installation
uv run python -c "import catpic; print(catpic.__version__)"
```

## Production Deployment

### Package Building
```bash
# Build wheel and source distribution
uv build

# Verify build contents
uv run python -m zipfile -l dist/*.whl

# Test installation from wheel
uv pip install dist/*.whl --force-reinstall
```

### Quality Assurance
```bash
# Full test suite
uv run pytest --cov=src/catpic --cov-report=term-missing

# Type checking
uv run mypy src/ --strict

# Code quality
uv run ruff check src/ tests/
uv run black --check src/ tests/

# Security check (if bandit added)
uv run bandit -r src/
```

### Release Checklist
```bash
# 1. Run full test suite
uv run pytest

# 2. Update version in pyproject.toml
# 3. Update CHANGELOG.md
# 4. Test package build
uv build

# 5. Test CLI functionality
uv run catpic --help
uv run catpic generate --help

# 6. Validate format specification
uv run python scripts/validate_format.py

# 7. Create release commit
git add -A
git commit -m "Release v0.1.0"
git tag v0.1.0

# 8. Build final package
uv build --clean
```

## Initial Setup

### Clone and Setup Repository
```bash
# Clone repository
git clone <repository-url>
cd timg

# Initialize UV environment
uv sync --dev

# Activate virtual environment  
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate     # Windows

# Verify installation
uv run python -c "import timg; print('TIMG package loaded successfully')"
```

### Install Development Dependencies
```bash
# Install all dependencies including dev tools
uv sync --dev

# Or install specific dev tools
uv add --dev pytest black ruff mypy types-pillow
```

## Development Workflow

### Code Formatting and Linting
```bash
# Format code with Black
uv run black src/ tests/ examples/

# Check code with Ruff
uv run ruff check src/ tests/ examples/

# Fix auto-fixable issues
uv run ruff check --fix src/ tests/ examples/

# Type checking with mypy
uv run mypy src/
```

### Testing
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/timg --cov-report=html

# Run specific test file
uv run pytest tests/test_core.py

# Run tests with verbose output
uv run pytest -v

# Create test images (run once)
uv run python tests/fixtures/create_test_images.py
```

### Package Development
```bash
# Install package in development mode
uv pip install -e .

# Build package
uv build

# Test CLI installation
uv run timg --help
```

## Usage Examples

### Basic Image Conversion
```bash
# Convert image with default settings
uv run timg convert image.jpg

# Specify output file and dimensions
uv run timg convert photo.png --width 60 --height 30 --output photo.timg

# Use different BASIS level
uv run timg convert image.jpg --basis 2,3 --width 80

# Convert animated GIF
uv run timg convert animation.gif --output animation.tima --delay 150
```

### Display and Playback
```bash
# Display static image
cat image.timg

# Display using TIMG command
uv run timg display image.timg

# Play animation
uv run timg play animation.tima

# Play with custom settings
uv run timg play animation.tima --delay 200 --no-loop

# Get file information
uv run timg info image.timg
```

### Python API Usage
```bash
# Interactive development
uv run python

# Example session:
# >>> from timg import TIMGEncoder, BASIS
# >>> encoder = TIMGEncoder(basis=BASIS.BASIS_2_2)
# >>> data = encoder.encode_image('image.jpg', width=40)
# >>> print(data)
```

## Development Tasks

### Phase 1 Development
```bash
# Run reference implementation
uv run python Reference/Implementation/reference-encoder.py

# Test core functionality
uv run pytest tests/test_core.py -v

# Validate format compliance
uv run python scripts/validate_format.py examples/sample.timg
```

### Phase 2 Development (Animation)
```bash
# Test animation encoding
uv run timg convert test.gif --output test.tima

# Validate animation playback
uv run timg play test.tima --max-loops 3

# Performance testing
uv run python -m cProfile -s cumtime -c "from timg import TIMGEncoder; TIMGEncoder().encode_animation('large.gif')"
```

### Phase 3 Development (Integration)
```bash
# Test Textual integration (when implemented)
uv run python examples/textual_integration.py

# Performance benchmarks
uv run python scripts/benchmark_encoding.py

# Terminal compatibility testing
uv run python scripts/test_terminals.py
```

## Troubleshooting

### Common Issues

#### Unicode Display Problems
```bash
# Test Unicode support
echo "▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"
echo "🬀🬁🬂🬃🬄🬅🬆🬇"

# Check terminal capabilities
echo $TERM
locale charmap
```

#### Color Support Issues
```bash
# Test 24-bit color support
echo -e "\x1b[38;2;255;0;0mRed\x1b[38;2;0;255;0mGreen\x1b[38;2;0;0;255mBlue\x1b[0m"

# Check COLORTERM variable
echo $COLORTERM
```

#### Package Issues
```bash
# Clean and reinstall
uv clean
rm -rf .venv
uv sync --dev

# Rebuild package
uv build --clean
```

### Development Environment
```bash
# Check Python version
python --version  # Should be 3.8+

# Check UV version
uv --version

# List installed packages
uv pip list

# Check package installation
uv run python -c "import timg; print(timg.__version__)"
```

## Production Deployment

### Package Building
```bash
# Build wheel and source distribution
uv build

# Verify build contents
uv run python -m zipfile -l dist/*.whl

# Test installation from wheel
uv pip install dist/*.whl --force-reinstall
```

### Quality Assurance
```bash
# Full test suite
uv run pytest --cov=src/timg --cov-report=term-missing

# Type checking
uv run mypy src/ --strict

# Code quality
uv run ruff check src/ tests/
uv run black --check src/ tests/

# Security check (if bandit added)
uv run bandit -r src/
```

### Release Checklist
```bash
# 1. Run full test suite
uv run pytest

# 2. Update version in pyproject.toml
# 3. Update CHANGELOG.md
# 4. Test package build
uv build

# 5. Test CLI functionality
uv run timg --help
uv run timg convert --help

# 6. Validate format specification
uv run python scripts/validate_format.py

# 7. Create release commit
git add -A
git commit -m "Release v0.1.0"
git tag v0.1.0

# 8. Build final package
uv build --clean
```