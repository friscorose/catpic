# Contributing to catpic

Thank you for contributing! This guide keeps things simple so you can focus on writing good code.

## Core Principle

Each language implementation is **self-contained**. Everything needed to build, test, and use an implementation lives in its language directory.

## Directory Structure

```
project-root/
├── docs/              # Shared documentation
├── spec/              # What all implementations must do
├── python/            # Complete Python project
├── c/                 # Complete C project
└── [language]/        # Your new implementation
```

## Basic Requirements

All contributions must:

1. **Follow the spec**: Implement what's defined in `spec/`
2. **Match the API**: Function names, parameters, and behavior should be equivalent across languages
3. **Pass test vectors**: Use the shared tests in `spec/test-vectors.json`
4. **Be self-contained**: Your language directory should build and run independently
5. **Include documentation**: Explain how to build and use your code

### Language-Agnostic API

Users should be able to switch languages with minimal friction. If Python has `calculate(input, options)`, then C should have `calculate()` with equivalent parameters, and Rust should have `calculate()`.

Use language conventions (snake_case vs camelCase, etc.) but keep concepts identical:
- Same function/method names (adjusted for language style)
- Same parameters in the same order
- Same return types (conceptually)
- Same error conditions and handling approach

## Adding a New Language

Create a directory structure like this:

```
rust/
├── README.md          # How to build, test, and use
├── src/               # Your source code
├── tests/             # Your tests (must include test vectors)
└── examples/          # At least one working example
```

Then:
- Add a CI workflow in `.github/workflows/rust.yml`
- Add your language to the table in root `README.md`
- Link to detailed docs in `docs/implementations/rust.md`

**That's it.** Use whatever tools and conventions are standard for your language.

## Modifying Existing Code

- Python changes go in `python/`
- C changes go in `c/`
- Keep changes focused on one thing
- Tests must pass

Language-specific style guides live in each implementation's directory (e.g., `python/README.md`).

## Changing Specifications

Spec changes affect all implementations. Open an issue first to discuss impact.

## Testing

Your implementation must:
- Include its own test suite using standard tooling for your language
- Provide a `test-config.toml` that describes how to run tests
- Pass all test vectors from `spec/test-vectors.json`

### Test Configuration

Create `[language]/test-config.toml`:

```toml
[build]
command = "make"           # How to build (optional)

[test]
command = "make test"      # How to run tests
working_dir = "."          # Relative to language directory

[compliance]
command = "make test-vectors"  # How to run spec compliance tests
expected_exit = 0              # Expected exit code for success
```

Examples:

**Python** (`python/test-config.toml`):
```toml
[test]
command = "uv run pytest"

[compliance]
command = "uv run pytest tests/test_compliance.py"
```

**C** (`c/test-config.toml`):
```toml
[build]
command = "make"

[test]
command = "make test"

[compliance]
command = "make test-vectors"
```

The root `scripts/test-all.sh` uses these configs to validate all implementations automatically.

## Pull Requests

- Use clear PR titles: `[Language] What you changed`
- One logical change per PR
- Update docs if you change behavior
- Make sure tests pass

## Questions?

Open an issue. We'll figure it out together.

---

**Keep it simple. Keep it working. Keep it documented.**

---

## Prospective Development

This section outlines ongoing work and aspirational directions for catpic. Contributions in these areas are welcome—please open an issue to discuss your approach before starting major work.

### Current Work in Progress

**Color Fallback Modes**
- 256-color terminal support (for older terminals)
- 16-color ANSI fallback
- Grayscale and monochrome modes
- Automatic detection and adaptation to terminal capabilities

**Dithering Algorithms**
- Floyd-Steinberg dithering for smoother gradients
- Ordered dithering options
- Configurable dithering strength

**Performance Optimization**
- Parallel cell processing for large images
- Chunked rendering for streaming applications
- Memory-efficient handling of animations
- Caching strategies for repeated renders

### Aspirational Directions

#### Advanced Terminal Graphics

Detect and utilize modern terminal graphics protocols when available, with glyxel rendering as the universal fallback:

**Sixel Graphics**
- Native bitmap graphics for terminals with Sixel support
- Common in xterm, mlterm, and modern terminal emulators
- Significantly higher resolution and color fidelity

**Kitty Graphics Protocol**
- High-performance image display with advanced features
- Supports transparency, cropping, and compositing
- Growing adoption in modern terminals

**Detection & Fallback Strategy**
```
1. Query terminal for Sixel/Kitty support
2. Use native graphics if available
3. Fall back to glyxel rendering (BASIS 2,4)
4. Further fall back to lower BASIS or color modes if needed
```

This approach ensures catpic works everywhere while providing optimal rendering where possible.

#### Multi-Language Ecosystem

**Rust Implementation**
- High-performance, memory-safe alternative to Python
- Zero-cost abstractions for embedded systems
- Native library for integration with Rust applications
- Target: API parity with Python reference implementation

**Go Implementation**
- Excellent concurrency for server applications
- Simple deployment (single binary)
- Strong ecosystem for network services
- Target: Compatible with Python MEOW format and primitives API

**Cross-Language Goals**
- Maintain API consistency across implementations
- Shared test vectors ensure behavioral compatibility
- Language-specific idioms where appropriate
- Common MEOW format as interchange standard

#### Extended Format Support

**Modern Image Formats**
- WebP: Efficient compression for web contexts
- AVIF: Next-generation format with excellent quality/size ratio
- Animated PNG (APNG): Alternative to GIF with better compression

**Streaming & Real-Time**
- Video file rendering (frame extraction)
- Real-time camera/webcam feed display
- Network stream support (RTSP, HTTP streaming)
- Performance considerations for real-time rendering

**Advanced Features**
- Transparency handling with terminal background detection
- Multi-layer compositing for TUI applications
- Color space conversion (sRGB, Display P3, etc.)

### Contributing to Prospective Features

If you're interested in working on any of these areas:

1. **Start with an issue**: Describe your approach and get feedback before investing time
2. **Reference prior art**: Link to relevant specs, implementations, or research
3. **Ensure cross-platform compatibility**: Test on Linux, macOS, and Windows where applicable
4. **Add comprehensive tests**: Demonstrate the feature works correctly
5. **Update documentation**: Include examples and usage patterns
6. **Consider the primitives API**: Can the feature benefit other TUI frameworks?

### Research Areas

Areas where community input would be valuable:

- **Color quantization algorithms**: Better than median cut for specific use cases?
- **Perceptual color metrics**: Using CIEDE2000 or similar for better color matching
- **Terminal capability detection**: Reliable methods across diverse environments
- **Compression techniques**: MEOW format optimization for storage/transmission
- **Accessibility**: Ensuring rendered content is accessible to screen readers

Have ideas or expertise in these areas? Open an issue to start a discussion.

