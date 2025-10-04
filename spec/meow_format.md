# MEOW Format Specification v1.0

**MEOW** - Mosaic Encoding Over Wire

## Overview

MEOW is a text-based image format designed to display images directly in terminals using Unicode block characters and ANSI 24-bit RGB color sequences. The format enables sharing terminal graphics over wire (SSH, chat, scripts).

## File Extensions

- `.meow` - Both static images and animations use the same extension

## Format Structure

### Static Images

```
MEOW/1.0
WIDTH:<width_in_chars>
HEIGHT:<height_in_chars>
BASIS:<basis_x>,<basis_y>
DATA:
<line1_with_ansi_and_unicode>
<line2_with_ansi_and_unicode>
...
```

### Animated Images

```
MEOW-ANIM/1.0
WIDTH:<width_in_chars>
HEIGHT:<height_in_chars>
BASIS:<basis_x>,<basis_y>
FRAMES:<frame_count>
DELAY:<delay_in_ms>
DATA:
FRAME:0
<frame0_line1>
<frame0_line2>
...
FRAME:1
<frame1_line1>
<frame1_line2>
...
```

## Header Fields

### Required Fields (Static Images)

- `MEOW/1.0` - Format identifier and version (MUST be first line)
- `WIDTH:<int>` - Image width in terminal characters
- `HEIGHT:<int>` - Image height in terminal characters
- `BASIS:<int>,<int>` - Pixel subdivision (e.g., `2,2` for quadrants)
- `DATA:` - Separator before image data

### Required Fields (Animations)

- `MEOW-ANIM/1.0` - Animation format identifier (MUST be first line)
- `WIDTH:<int>` - Frame width in terminal characters
- `HEIGHT:<int>` - Frame height in terminal characters
- `BASIS:<int>,<int>` - Pixel subdivision
- `FRAMES:<int>` - Total number of frames
- `DELAY:<int>` - Milliseconds between frames
- `DATA:` - Separator before frame data

### Frame Markers (Animations Only)

- `FRAME:<int>` - Frame number (0-indexed, sequential)

## BASIS System

The BASIS system defines pixel subdivision levels for mosaic encoding:

| BASIS | Patterns | Unicode Range | Terminal Support |
|-------|----------|---------------|------------------|
| 1,2   | 4        | Block Elements | Universal |
| 2,2   | 16       | Quadrant Blocks | Excellent |
| 2,3   | 64       | Sextant Blocks | Good (Unicode 13.0+) |
| 2,4   | 256      | Legacy Computing | Limited (Unicode 16.0+) |

Each BASIS (x,y) means each terminal character represents an x×y pixel block.

## Unicode Character Sets

### BASIS 1,2 (4 characters)
```
 ▀▄█
```
- ` ` (U+0020) - Empty
- `▀` (U+2580) - Upper half block
- `▄` (U+2584) - Lower half block  
- `█` (U+2588) - Full block

### BASIS 2,2 (16 characters)
```
 ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█
```
Quadrant blocks (U+2580-U+259F range)

### BASIS 2,3 (64 characters)
```
 🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬑🬒🬓🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬧🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻▀▄█
```
Sextant blocks (U+1FB00-U+1FB3B range, Unicode 13.0)

### BASIS 2,4 (256 characters)
Legacy Computing Supplement (U+1CC00-U+1CCA3 range, Unicode 16.0)

Full character table defined in `spec/basis-tables.json`

## ANSI Color Format

Each character cell uses 24-bit RGB foreground and background colors:

```
\x1b[38;2;<R>;<G>;<B>m\x1b[48;2;<R>;<G>;<B>m<UNICODE_CHAR>\x1b[0m
```

Where:
- `\x1b[38;2;<R>;<G>;<B>m` - Set foreground RGB color (0-255 per channel)
- `\x1b[48;2;<R>;<G>;<B>m` - Set background RGB color (0-255 per channel)
- `<UNICODE_CHAR>` - Unicode block character
- `\x1b[0m` - Reset formatting

### Example

A single red-on-blue quadrant character:
```
\x1b[38;2;255;0;0m\x1b[48;2;0;0;255m▘\x1b[0m
```

## Encoding Algorithm

Based on EnGlyph mosaic approach:

1. **Resize**: Scale image to `WIDTH×BASIS_X` by `HEIGHT×BASIS_Y` pixels
2. **Cell Processing**: For each terminal character position:
   - Extract `BASIS_X×BASIS_Y` pixel block
   - Quantize block to 2 colors using `PIL.quantize(colors=2)` or equivalent
   - Generate bit pattern: `pattern += 2**pixel_index` for each foreground pixel
   - Select Unicode character: `blocks[pattern]`
   - Compute RGB centroids for foreground/background colors
   - Output ANSI color sequence

### Bit Pattern Indexing

For BASIS x,y with n = x×y pixels per cell:
- Pixels indexed 0 to (n-1) in row-major order (left-to-right, top-to-bottom)
- Foreground pixel at index i contributes 2^i to pattern
- Pattern value 0 to (2^n - 1) maps to character at that index in BASIS table

### Color Centroid Calculation

For each pixel block:
1. Separate pixels into foreground and background sets based on quantization
2. Compute RGB centroid (average) of foreground pixels
3. Compute RGB centroid (average) of background pixels
4. Use centroids as ANSI foreground/background colors

## Display Requirements

### Terminal Requirements
- 24-bit RGB color support (truecolor)
- Unicode block character rendering
- UTF-8 text encoding

### Minimal Display
Static images MUST display correctly with:
```bash
cat filename.meow
```

### Animation Display
Animations REQUIRE:
- Frame timing control
- Screen clearing between frames
- Keyboard interrupt handling (Ctrl+C)

## Animation Timing

- `DELAY` field specifies milliseconds between frames
- Implementations SHOULD honor the specified delay
- Default delay: 100ms if not specified or invalid
- Animation loops indefinitely unless:
  - User interrupts (Ctrl+C)
  - Implementation provides loop count parameter
  - EOF or error condition

## Compatibility Matrix

| BASIS | Terminal Requirement | Font Requirement | Recommended Use |
|-------|---------------------|------------------|-----------------|
| 1,2   | Any terminal | Any font | Maximum compatibility |
| 2,2   | Truecolor support | Basic Unicode | Recommended default |
| 2,3   | Truecolor support | Unicode 13.0+ font | High quality |
| 2,4   | Truecolor support | Unicode 16.0+ font | Experimental/demos |

## Over Wire Usage

MEOW files are designed to be shared "over wire":
- Copy/paste into SSH sessions
- Embed in scripts and documentation  
- Share in terminal-based chat
- Store in version control (text format)
- Stream over network connections
- Display with standard tools (`cat`, `less -R`)

## Validation

A valid MEOW file MUST:
1. Start with `MEOW/1.0` or `MEOW-ANIM/1.0`
2. Include all required header fields
3. Have `DATA:` separator before content
4. Contain `WIDTH * HEIGHT` lines of image data (static)
5. Contain valid ANSI escape sequences
6. Use UTF-8 encoding
7. End with newline

For animations:
- Include `FRAME:N` markers in sequential order (0, 1, 2, ...)
- Each frame MUST have `WIDTH * HEIGHT` lines
- Total frames MUST match `FRAMES` header value

## Error Handling

Implementations SHOULD handle:
- Missing or malformed headers → Error
- Invalid BASIS values → Error
- Mismatched dimensions → Error
- Truncated data → Error
- Invalid UTF-8 → Error
- Missing frames (animation) → Error

## Version History

- **v1.0** (2025-01-27) - Initial specification
  - Static image support
  - Animation support
  - BASIS 1,2 / 2,2 / 2,3 / 2,4
  - 24-bit RGB colors