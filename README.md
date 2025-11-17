# catpic

Turn images into terminal eye candy using Unicode mosaics and ANSI colors.

**The twist:** Save as MEOW format and display with `cat`. Yes, the POSIX command. No special viewer needed.

```bash
catpic photo.jpg -o photo.meow
cat photo.meow  # 🐱 Just works
```

> **Note:** This is v0.9.0 Release Candidate. While core functionality is stable and well-tested, some features (multi-language implementations, iTerm2 protocol on non-Mac platforms, edge cases across terminal emulators) are still being validated. We'd love your feedback, bug reports, terminal compatibility notes, or just a "hey, this worked great!" on [GitHub Issues](https://github.com/friscorose/catpic/issues). Early adopters welcome! 🎉

## Installation

**Quick install (recommended):**

```bash
# Using uv (fast, modern)
uv tool install catpic

# Using pipx (isolated environment)
pipx install catpic

# Using pip (system-wide)
pip install catpic
```

**Verify installation:**
```bash
catpic --version
catpic --detect  # Check your terminal's capabilities
```

**First image:**
```bash
catpic photo.jpg
```

## What are Glyxels?

**Glyxels** (glyph + pixels) are what happens when you treat each terminal character as a tiny canvas. catpic uses the EnGlyph algorithm to subdivide characters into grids—for example, BASIS 2×4 means each character represents 8 glyxels (2 wide, 4 tall).

The magic:
1. Slice your image into character-sized cells
2. Find the two most important colors in each cell
3. Pick the Unicode character that matches the glyxel pattern
4. Paint it with ANSI true-color

Result? A standard 80×24 terminal becomes a 160×96 glyxel display. Not bad for text.

## Features

- **`cat`-compatible format**: MEOW files display with standard POSIX `cat`
- **Multiple protocols**: Kitty Graphics, Sixel, iTerm2, and Glyxel (Unicode mosaic)
- **Protocol-aware animation**: GIF playback works across ALL protocols (even those without native animation support)
- **Multiple BASIS levels**: Trade speed for quality (1×2 to 2×4)
- **Smooth animations**: No flicker, proper timing, loop control
- **Auto-detection**: Picks the best protocol for your terminal
- **Primitives API**: Build your own TUI graphics with composable functions
- **Environment aware**: Automatic terminal size and aspect ratio detection
- **Multi-language**: Python (stable), C (in development), Rust/Go (planned)

## Architecture (v0.9)

catpic uses a layered architecture for protocol-agnostic rendering:

- **FrameBuffer**: Protocol-agnostic display interface
- **LayerRenderer**: Timing-aware frame sequences with loop support
- **GeometryAPI**: Canvas inference and format conversions
- **Protocol Generators**: Pluggable output formats (Kitty, Sixel, iTerm2, Glyxel)

This design enables:
- **Multi-protocol animation** - Same MEOW file works across all terminals
- **Frame sequencing without native support** - Kitty/Sixel/iTerm2 don't have animation primitives, but catpic provides smooth GIF playback by managing frame sequences with precise timing
- **External frame sources** - Games, video players, and emulators can use catpic for display
- **Idempotent conversions** - Glyxel ↔ PNG ↔ Glyxel with no data loss
- **Future extensions** - New features without breaking MEOW format

### Using catpic as a Library

catpic's abstractions make it easy to add terminal graphics to your project:

**Display static images:**
```python
from catpic.framebuffer import FrameBuffer
from catpic.detection import detect_best_protocol

# Auto-detect best protocol for this terminal
protocol = detect_best_protocol()
fb = FrameBuffer(protocol, width=80, height=24)

# Render PNG data
with open('image.png', 'rb') as f:
    fb.render(f.read())
```

**Animated sequences (games, video, live displays):**
```python
from catpic.renderer import LayerRenderer

renderer = LayerRenderer(fb)
renderer.setup_animation_canvas(height=24)

# Game loop or video frames
frames = [
    {'data': frame1_png, 'render_at_ms': 0},
    {'data': frame2_png, 'render_at_ms': 16},  # 60 FPS
    {'data': frame3_png, 'render_at_ms': 32},
]

renderer.render_with_loop(frames, loop_count=0)  # Loop forever
renderer.teardown_animation_canvas(height=24)
```

**Canvas geometry calculations:**
```python
from catpic.geometry import GeometryAPI

# Convert between glyxel cells and pixels
pixel_size = GeometryAPI.glyxel_to_pixels(width=40, height=20, basis=(2,4))
cell_size = GeometryAPI.pixels_to_glyxel(pixel_width=320, pixel_height=240, basis=(2,4))

# Infer canvas dimensions from MEOW content
from catpic.decoder import parse_meow
meow = parse_meow(meow_content)
width, height = GeometryAPI.infer_canvas_size(meow)
```

**For complete API documentation**, see [docs/api-reference.md](docs/api-reference.md).

## Installation & Usage

**See [IMPLEMENTATION.md](IMPLEMENTATION.md) for installation instructions and API documentation for your language.**

Each implementation provides the same core functionality with language-appropriate APIs and conventions.

**Current status:**
- **Python:** Stable, fully functional (reference implementation)
- **C** In development 
- **Rust, Go:** Planned (architecture designed for multi-language support)

## Graphics Protocols

catpic supports multiple terminal graphics protocols with automatic detection and fallback:

| Protocol | Terminals | Quality | Speed | Testing Status |
|----------|-----------|---------|-------|----------------|
| **Kitty** | Kitty | Excellent | Very Fast | ✅ Verified in Kitty terminal |
| **iTerm2** | iTerm2, VSCode<sup>†</sup>, WezTerm, Tabby | Excellent | Very Fast | ⚠️ Needs Mac hardware testing |
| **Sixel** | xterm<sup>‡</sup>, mlterm, foot, WezTerm | Good | Fast | ✅ Verified in xterm, VSCode |
| **Glyxel** | All terminals | Fair | Fast | ✅ Universal fallback |

<sup>†</sup> Requires `terminal.integrated.enableImages` setting  
<sup>‡</sup> Requires `xterm -ti vt340` or sixel compile option

**Auto-detection priority:** Kitty > iTerm2 > Sixel > Glyxel

**Testing note:** iTerm2 protocol generates valid escape sequences (verified in tests) but needs validation on native iTerm2/Mac hardware. VSCode terminal image support varies by configuration.

```bash
# Auto-detect best protocol
catpic photo.jpg

# Force specific protocol
catpic photo.jpg --protocol kitty
catpic photo.jpg --protocol sixel
catpic photo.jpg --protocol iterm2
catpic photo.jpg --protocol glyxel

# Detect capabilities for your terminal
catpic --detect
```

### Terminal Configuration

#### VSCode Integrated Terminal

VSCode supports iTerm2 inline images and Sixel graphics. For optimal display:

**Required Settings:**

1. **Enable Image Support** (for iTerm2 protocol):
   - Settings → Search "terminal images"
   - Enable: `Terminal › Integrated: Enable Images`

2. **Fix Aspect Ratio** (prevents distortion):
   - `Terminal › Integrated: Minimum Contrast Ratio` → `1`  
     _(Default adjusts contrast; set to 1 for "Do Nothing")_
   - `Terminal › Integrated: Line Height` → `1`  
     _(Default 1.1 causes aspect ratio distortion)_

3. **Performance** (optional):
   - `Terminal › Integrated: GPU Acceleration` → `on`

**Without these settings:**
- Images may display with incorrect aspect ratios
- Colors may be adjusted unexpectedly
- Line spacing may create visual gaps

#### xterm Sixel Support

xterm requires VT340 emulation mode for Sixel graphics:

```bash
# Run with Sixel support
xterm -ti vt340

# Or compile xterm with sixel support
./configure --enable-sixel-graphics
```

#### tmux Configuration

tmux requires passthrough configuration for graphics protocols:

```bash
# ~/.tmux.conf
set -g allow-passthrough on
```

Then reload:
```bash
tmux source-file ~/.tmux.conf
```

**Note:** Inside tmux, some terminal-specific environment variables (like `KITTY_WINDOW_ID`) may not propagate. Use `catpic --detect` to see available protocols, or force a specific protocol with `--protocol`.

**Reference:** https://tmuxai.dev/tmux-allow-passthrough/

## Configuration

catpic uses a unified JSON configuration via the `CATPIC_CONFIG` environment variable:

```bash
export CATPIC_CONFIG='{"protocol":"sixel","basis":"2,4","aspect 2x4":2.0}'
catpic photo.jpg  # Uses your configuration
```

**Auto-detect and persist:**

```bash
# Detect optimal settings for your terminal
catpic --detect

# Example output with command to persist:
export CATPIC_CONFIG='{"protocol":"sixel","basis":"2,2","aspect base":2.0,...}'

# Add to your shell profile to make permanent:
echo 'eval "$(catpic --detect)"' >> ~/.bashrc
```

**Configuration keys:**

| Key | Values | Default | Description |
|-----|--------|---------|-------------|
| `protocol` | `kitty`, `sixel`, `iterm2`, `glyxel`, `auto` | `auto` | Graphics protocol to use |
| `basis` | `1,2`, `2,2`, `2,3`, `2,4` | `2,2` | Quality level (see BASIS section) |
| `aspect base` | float | `2.0` | Base character aspect ratio |
| `aspect 1x2` | float | `2.0` | Aspect correction for BASIS 1×2 |
| `aspect 2x2` | float | `0.9` | Aspect correction for BASIS 2×2 |
| `aspect 2x3` | float | `1.5` | Aspect correction for BASIS 2×3 |
| `aspect 2x4` | float | `2.0` | Aspect correction for BASIS 2×4 |

**Session overrides:**

You can override configuration per-command without changing your environment:

```bash
# Override protocol (doesn't modify CATPIC_CONFIG)
catpic photo.jpg --protocol kitty

# Override basis
catpic photo.jpg --basis 2,4

# Show current configuration
catpic --config
```

## How BASIS Works

BASIS (x, y) defines the glyxel grid per character:

**Available BASIS levels:**

| BASIS | Patterns | Quality | Color Fidelity | Unicode Requirement |
|-------|----------|---------|----------------|---------------------|
| `1,2` | 4 | Fast, chunky | Perfect (2 colors/cell) | Basic (block elements) |
| `2,2` | 16 | Balanced | Approximate | Unicode 13.0+ (quadrant blocks) |
| `2,3` | 64 | Smooth gradients | Approximate | Unicode 13.0+ (sextant blocks) |
| `2,4` | 256 | Maximum detail | Approximate | Unicode 13.0+ (mosaic blocks U+1CD00) |

**Trade-offs:**
- **BASIS 1×2**: Perfect color representation (2 colors per cell, no approximation) but chunky appearance
- **BASIS > 1×2**: Better spatial detail, but colors are approximated to fit the 2-color constraint per cell
- Higher BASIS = more glyxels per character = better detail, but slower rendering and color approximation

**Color accuracy note:** Each terminal character can only display 2 colors (foreground + background). BASIS 1×2 uses simple half-blocks, so colors map perfectly. Higher BASIS levels subdivide cells into more glyxels, requiring color approximation to find the best 2-color representation for each cell's content.

**Terminal compatibility:** Most modern terminals support all BASIS levels. If you see missing characters or boxes, your terminal may need:
- Updated Unicode fonts with Unicode 13.0+ support
- Proper rendering of quadrant blocks (U+2596-259F)
- Proper rendering of sextant blocks (U+1FB00-1FB3B)
- Proper rendering of mosaic blocks (U+1CD00-1CEBF) for BASIS 2×4

**Setting BASIS:**

```bash
# Via configuration (recommended)
export CATPIC_CONFIG='{"basis":"2,4",...}'

# Per-command override
catpic photo.jpg --basis 2,4
```

## MEOW Format

**M**osaic **E**ncoding **O**ver **W**ire—glyxel images as plain text with ANSI escape codes.

MEOW files are `cat`-compatible: they're standard text with embedded metadata and ANSI color codes. No special viewer needed.

**Current version:** 0.9 (supports multiple graphics protocols with embedded PNG)

**Example usage:**
```bash
# Create
catpic sunset.jpg -o sunset.meow

# Display (any of these work)
cat sunset.meow
less -R sunset.meow
head -n 30 sunset.meow  # Preview
```

MEOW files contain:
- Canvas metadata (size, animation settings, BASIS)
- Layer metadata (position, transparency, frame timing)
- Protocol-specific data (PNG for Kitty/Sixel/iTerm2, glyxel for universal fallback)
- Standard ANSI escape codes for colors
- Unicode characters encoding glyxel patterns

**Format specification:** See [spec/meow_format.md](spec/meow_format.md)

## Troubleshooting

### Protocol Issues

**Images don't display:**
- Check supported protocols: `catpic --detect`
- Try forcing glyxel: `catpic image.jpg --protocol glyxel`
- Verify terminal configuration (see Terminal Configuration above)

**Sixel shows garbled output:**
- xterm: Use `xterm -ti vt340` or compile with `--enable-sixel-graphics`
- Some terminals claim xterm compatibility but lack sixel rendering
- Sixel detection works, but rendering depends on terminal build options

**iTerm2 in VSCode doesn't work:**
- Enable `terminal.integrated.enableImages` setting
- May require GPU acceleration (check VSCode docs)
- Fallback: Use `--protocol sixel` (auto-detected and works reliably)

**Kitty graphics in tmux:**
- Configure tmux passthrough: `set -g allow-passthrough on`
- Or use catpic outside tmux
- Fallback protocols (sixel/glyxel) work in tmux

### Display Quality

**Images look squashed or stretched:**
- Adjust `CATPIC_CHAR_ASPECT` (see Environment Variables)
- Try different protocols: `--protocol kitty` or `--protocol sixel`

**Missing characters or boxes:**
- Update terminal font (Unicode 13.0+ support)
- Try lower BASIS: `--basis 1,2`
- Check terminal Unicode support

**Colors look wrong:**
- VSCode: Set `Minimum Contrast Ratio` to 1
- Verify 24-bit color support: `echo $COLORTERM` should show `truecolor`

## Project Structure

catpic is designed as a multi-language project with consistent behavior:

```
catpic/
├── python/              # Python reference implementation (stable, v0.9.0)
├── c/                   # C implementation (planned)
├── rust/                # Rust implementation (planned)
├── go/                  # Go implementation (planned)
├── docs/                # Architecture and API documentation
├── spec/                # MEOW format and compliance specifications
└── benchmarks/          # Performance comparisons
```

**Multi-language goal:** All implementations will:
- Support the identical MEOW format
- Pass the same compliance test suite
- Implement the EnGlyph algorithm consistently
- Support all BASIS levels
- Support all graphics protocols (Kitty, Sixel, iTerm2, Glyxel)

Language-specific APIs will differ to match ecosystem conventions.

**Current status:** Python implementation is complete and serves as the reference. C/Rust/Go implementations are part of the roadmap.

## Documentation

### User Documentation
- **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - Installation and language-specific usage
- **[docs/getting-started.md](docs/getting-started.md)** - Quick start guide
- **[docs/primitives_api.md](docs/primitives_api.md)** - Low-level API for TUI development
- **[docs/api-reference.md](docs/api-reference.md)** - Complete API reference

### Implementation Guides
- **[docs/implementations/python.md](docs/implementations/python.md)** - Python-specific documentation
- **[docs/implementations/c.md](docs/implementations/c.md)** - C implementation guide

### Specifications
- **[spec/meow_format.md](spec/meow_format.md)** - MEOW format specification (v0.9)
- **[spec/compliance.md](spec/compliance.md)** - Cross-language test requirements
- **[spec/protocol.md](spec/protocol.md)** - Graphics protocol implementations
- **[spec/api.md](spec/api.md)** - API design principles

### Contributing
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines and standards

## Related Projects

- **[timg](https://github.com/hzeller/timg/)** - Terminal image and video viewer with similar goals
- **[viu](https://github.com/atanunq/viu)** - Terminal image viewer in Rust
- **[chafa](https://hpjansson.org/chafa/)** - Character art facsimile generator
- **[EnGlyph](https://github.com/friscorose/textual-EnGlyph)** - The Textual widget that inspired this

**What makes catpic different:**
- **MEOW format** - Stored, layered, animated terminal graphics that work with `cat`
- **Universal animation** - GIF playback across ALL protocols (even Kitty/Sixel/iTerm2, which lack native animation)
- **Multi-protocol** - Automatic fallback across terminal capabilities
- **Basis-aware rendering** - Quality vs. size tradeoffs with consistent API
- **Multi-language** - Consistent behavior across Python, C, Rust, Go implementations

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style and testing requirements
- How to add new BASIS levels
- Cross-language implementation guidelines
- Protocol support (Kitty, Sixel, iTerm2, future protocols)
- Prospective features (streaming, video playback, etc.)

## License

MIT—do whatever you want with it.

## See Also

- [EnGlyph](https://github.com/friscorose/textual-EnGlyph) - The Textual widget that inspired this
- [docs/primitives_api.md](docs/primitives_api.md) - Build your own TUI graphics

---

## About This Project

**catpic was built entirely through Claude Sonnet 4.5's free web interface.**

Yes, really. The entire codebase—architecture, implementation, tests, documentation, and this README—was developed through conversational sessions with Claude. No paid API credits, no enterprise plan, just careful session management and clear communication.

**What this demonstrates:**
- **Serious engineering** is possible with free-tier AI tools when managed properly
- **Architecture-first thinking** works: we designed abstractions (FrameBuffer, LayerRenderer) before implementing features
- **Incremental complexity** wins: started with static images, added protocols, then animation, then timing models
- **Test-driven development** catches regressions: 283 tests kept refactoring safe
- **Clear requirements** matter: specific goals, checkpoints, and visual verification tests guided every session

**The human contribution:**
- **EnGlyph algorithm** - Core glyxel encoding/decoding (pure human code, no LLM)
- System architecture and API design decisions
- Quality assurance through visual verification across terminals
- Session management and continuation prompts (the real meta-skill)
- Terminal testing across platforms (Kitty, xterm, VSCode, tmux)

**The AI contribution:**
- Implementation of the encoder, decoder, protocols, and geometry.
- Test suite design and implementation (283 tests)
- Documentation generation (specs, API docs, examples)
- Bug diagnosis and fixes (sixel rendering, canvas inference, protocol teardown)
- Architectural refactoring (v0.9 protocol-aware animation)

**This isn't a toy project.** It's a production-ready terminal graphics library with:
- Multi-protocol support (4 different terminal graphics systems)
- Idempotent format conversion (glyxel ↔ PNG ↔ glyxel)
- Protocol-agnostic animation with timing models
- Clean abstractions for external use (games, video, emulators)
- Comprehensive test coverage

**If you're building something non-trivial with AI assistance:**
- Manage context carefully (continuation prompts are your state persistence)
- Design first, implement second (architecture pays off)
- Test continuously (catch issues early)
- Use visual verification for graphics/UI work
- Keep sessions focused (one feature per checkpoint)

The tools are free. The results can be serious. You just need a plan and patience.

---

*Built with Claude Sonnet 4.5 (Anthropic) exploring what's possible when you treat AI as a thoughtful collaborator rather than a magic code generator.*
