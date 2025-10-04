# catpic API Specification v1.0

Language-agnostic API that all catpic implementations MUST provide.

## Design Principles

1. **Consistent naming**: Use language conventions (snake_case vs camelCase) but keep concepts identical
2. **Same parameters**: Functions take equivalent parameters in the same order
3. **Same behavior**: Identical inputs produce identical outputs across languages
4. **Same errors**: Handle error conditions consistently

## Core API

### Encoder

Create instances to encode images to MEOW format.

#### Constructor

```
Encoder(basis?) -> Encoder instance
```

**Parameters:**
- `basis` (optional): Quality level
  - Accept tuple format: `(2, 2)`
  - Accept enum format: `BASIS_2_2` (or language equivalent)
  - Accept null/None: Use `CATPIC_BASIS` environment variable or default to `(2, 2)`

**Environment:**
- `CATPIC_BASIS`: Default BASIS level (e.g., "2,4" or "2x4" or "2_4")

**Examples:**
```python
# Python
encoder = CatpicEncoder(basis=(2, 2))
encoder = CatpicEncoder(basis=BASIS.BASIS_2_2)
encoder = CatpicEncoder()  # Uses env var or default
```

```c
// C
catpic_encoder_t *encoder = catpic_encoder_new(2, 2);
catpic_encoder_t *encoder = catpic_encoder_new_default();  // Uses env var
```

```rust
// Rust
let encoder = CatpicEncoder::new(2, 2);
let encoder = CatpicEncoder::default();  // Uses env var
```

#### Encode Image

```
encode_image(image_path, width?, height?) -> string
```

**Parameters:**
- `image_path`: Path to image file (string or path object)
- `width` (optional): Output width in terminal characters (default: 80)
- `height` (optional): Output height in terminal characters (default: auto-calculated from aspect ratio)

**Returns:**
- String containing complete MEOW format content

**Errors:**
- File not found
- Invalid image format
- Image decoding error
- Invalid dimensions (0 or negative)

**Behavior:**
- If only width specified: Calculate height maintaining aspect ratio with 0.5 character aspect correction
- If only height specified: Calculate width maintaining aspect ratio  
- If both specified: Use exact dimensions (may distort image)
- Character aspect correction: Terminal characters are typically ~2:1 height:width ratio

**Examples:**
```python
# Python
meow = encoder.encode_image('photo.jpg', width=80)
meow = encoder.encode_image('photo.jpg', width=100, height=50)
```

```c
// C
char *meow = catpic_encode_image(encoder, "photo.jpg", 80, 0);
char *meow = catpic_encode_image(encoder, "photo.jpg", 100, 50);
```

#### Encode Animation

```
encode_animation(gif_path, width?, height?, delay?) -> string
```

**Parameters:**
- `gif_path`: Path to animated GIF file
- `width` (optional): Output width in terminal characters (default: 60)
- `height` (optional): Output height in terminal characters (default: auto-calculated)
- `delay` (optional): Override frame delay in milliseconds (default: use GIF timing)

**Returns:**
- String containing complete MEOW-ANIM format content

**Errors:**
- File not found
- Not an animated image
- Invalid image format
- Invalid dimensions

**Examples:**
```python
# Python
meow_anim = encoder.encode_animation('animation.gif', width=60)
meow_anim = encoder.encode_animation('animation.gif', delay=50)
```

### Decoder

Create instances to decode and display MEOW format.

#### Constructor

```
Decoder() -> Decoder instance
```

**Parameters:** None

**Examples:**
```python
# Python
decoder = CatpicDecoder()
```

```c
// C
catpic_decoder_t *decoder = catpic_decoder_new();
```

#### Display

```
display(content, output?) -> void
```

**Parameters:**
- `content`: MEOW format string
- `output` (optional): Output stream (default: stdout)

**Behavior:**
- Parse MEOW format
- Output to terminal with ANSI codes
- For animations: Display only first frame
- No newline buffering (immediate output)

**Errors:**
- Invalid MEOW format
- Missing required headers
- Truncated data

**Examples:**
```python
# Python
decoder.display(meow)
decoder.display(meow, file=sys.stderr)
```

```c
// C
catpic_display(decoder, meow, stdout);
```

#### Display File

```
display_file(meow_path, output?) -> void
```

**Parameters:**
- `meow_path`: Path to .meow file
- `output` (optional): Output stream (default: stdout)

**Errors:**
- File not found
- Invalid UTF-8 encoding
- Invalid MEOW format

**Examples:**
```python
# Python
decoder.display_file('image.meow')
```

### Player

Create instances to play MEOW animations.

#### Constructor

```
Player() -> Player instance
```

**Examples:**
```python
# Python
player = CatpicPlayer()
```

#### Play

```
play(content, delay?, loop?, max_loops?) -> void
```

**Parameters:**
- `content`: MEOW-ANIM format string
- `delay` (optional): Override delay in milliseconds (default: use file delay)
- `loop` (optional): Loop indefinitely (default: true)
- `max_loops` (optional): Maximum loop count (default: infinite)

**Behavior:**
- Clear screen before each frame
- Display frame
- Wait specified delay
- Loop until interrupted (Ctrl+C) or max_loops reached
- Restore cursor and clear screen on exit

**Errors:**
- Not an animation format
- Invalid MEOW-ANIM format
- No frames found

**Keyboard:**
- Ctrl+C: Stop playback, restore terminal

**Examples:**
```python
# Python
player.play(meow_anim)
player.play(meow_anim, delay=100, max_loops=3)
```

#### Play File

```
play_file(meow_path, delay?, loop?, max_loops?) -> void
```

Same as `play()` but loads from file.

## Encoding Algorithm

All implementations MUST use the EnGlyph algorithm:

1. **Resize** image to `WIDTH * BASIS_X` by `HEIGHT * BASIS_Y` pixels
2. **For each cell** (character position):
   - Extract `BASIS_X × BASIS_Y` pixel block
   - Quantize to 2 colors (foreground/background)
   - Generate bit pattern: sum of `2^i` for each foreground pixel (row-major order)
   - Select character: `blocks[bit_pattern]`
   - Compute RGB centroid (average) for foreground pixels
   - Compute RGB centroid (average) for background pixels
   - Format with ANSI: `\x1b[38;2;{fg_r};{fg_g};{fg_b}m\x1b[48;2;{bg_r};{bg_g};{bg_b}m{char}\x1b[0m`

### Quantization

- Use 2-color quantization (median cut or equivalent)
- Separate pixels into foreground/background sets
- Higher intensity → foreground (typically)

### Color Centroid

```
centroid_rgb = (
    sum(r_values) / count,
    sum(g_values) / count,
    sum(b_values) / count
)
```

If no pixels in set (all background or all foreground), use `(0, 0, 0)`.

## BASIS Character Tables

Implementations MUST support BASIS levels defined in `spec/meow-format.md`:

- BASIS 1,2: 4 characters
- BASIS 2,2: 16 characters (required)
- BASIS 2,3: 64 characters (recommended)
- BASIS 2,4: 256 characters (optional)

Character mappings defined in `spec/basis-tables.json`.

## Error Handling

### Required Error Messages

Implementations SHOULD provide clear error messages for:

- **File errors**: "File 'X' not found"
- **Format errors**: "Invalid MEOW format: missing header"
- **Dimension errors**: "Width must be positive"
- **Basis errors**: "Invalid BASIS: (X,Y)"
- **Animation errors**: "Not an animated image"

### Error Reporting

- Write errors to stderr (or language equivalent)
- Exit with non-zero status code for CLI tools
- Throw exceptions or return error codes for libraries

## Testing

All implementations MUST:
1. Pass test vectors in `spec/test-vectors.json`
2. Produce byte-identical MEOW output for same inputs
3. Display test images correctly in terminal

See `spec/compliance.md` for full requirements.

## Language-Specific Notes

### Python
- Use `BASIS` enum from `catpic.core`
- Accept `Union[str, Path]` for file paths
- Type hints required

### C
- Use `catpic_encoder_t*` opaque pointers
- Caller responsible for freeing returned strings with `catpic_free()`
- Return NULL on error, set errno

### Rust
- Use `Result<String, CatpicError>` for fallible operations
- Implement `Default` trait for encoder/decoder
- Support `AsRef<Path>` for file paths

## Version History

- **v1.0** (2025-01-27) - Initial specification
  - Encoder, Decoder, Player APIs
  - EnGlyph algorithm requirement
  - Environment variable support