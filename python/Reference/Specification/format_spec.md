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

## BASIS System

The BASIS system defines pixel subdivision levels for mosaic encoding:

- **BASIS 1,2**: 4 patterns - Universal terminal compatibility
- **BASIS 2,2**: 16 patterns - Balanced quality/compatibility  
- **BASIS 2,3**: 64 patterns - High quality
- **BASIS 2,4**: 256 patterns - Ultra quality

Each BASIS (x,y) means each terminal character represents an x×y pixel block.

## Unicode Character Sets

### BASIS 1,2 (4 characters)
- ` ` (space) - Empty
- `▀` - Upper half block
- `▄` - Lower half block  
- `█` - Full block

### BASIS 2,2 (16 characters)
Quadrant blocks: ` ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█`

### BASIS 2,3 (64 characters)
Sextant blocks: `🬀🬁🬂🬃🬄🬅🬆🬇🬈🬉🬊🬋🬌🬍🬎🬏🬐🬑🬒🬓🬔🬕🬖🬗🬘🬙🬚🬛🬜🬝🬞🬟🬠🬡🬢🬣🬤🬥🬦🬧🬨🬩🬪🬫🬬🬭🬮🬯🬰🬱🬲🬳🬴🬵🬶🬷🬸🬹🬺🬻`

### BASIS 2,4 (256 characters)
Legacy Computing Supplement: `𜴀-𜷥` (256 total patterns)

## ANSI Color Format

Each character cell uses 24-bit RGB foreground and background colors:

```
\x1b[38;2;<R>;<G>;<B>m\x1b[48;2;<R>;<G>;<B>m<UNICODE_CHAR>\x1b[0m
```

Where:
- `\x1b[38;2;<R>;<G>;<B>m` - Set foreground RGB color
- `\x1b[48;2;<R>;<G>;<B>m` - Set background RGB color  
- `<UNICODE_CHAR>` - Unicode block character
- `\x1b[0m` - Reset formatting

## Encoding Algorithm

Based on EnGlyph mosaic approach:

1. **Resize**: Scale image to `WIDTH×BASIS_X` by `HEIGHT×BASIS_Y` pixels
2. **Cell Processing**: For each terminal character position:
   - Extract `BASIS_X×BASIS_Y` pixel block
   - Quantize block to 2 colors using `PIL.quantize(colors=2)`
   - Generate bit pattern: `pattern += 2**pixel_index` for lit pixels
   - Select Unicode character: `blocks[pattern]`
   - Compute RGB centroids for foreground/background colors
   - Output ANSI color sequence

## Display Requirements

- Terminal must support 24-bit RGB colors (most modern terminals)
- Unicode block character support required
- Files should display correctly with `cat filename.meow`
- No special viewer software required for static images
- catpic tool recommended for animations

## Animation Timing

- `DELAY` field specifies milliseconds between frames
- Default: 100ms if not specified
- Animation loops indefinitely unless stopped

## Compatibility

- **Minimum**: BASIS 1,2 works on virtually all terminals
- **Recommended**: BASIS 2,2 for balanced quality/compatibility
- **High Quality**: BASIS 2,3 for modern terminals with sextant block support
- **Ultra**: BASIS 2,4 requires terminals with Legacy Computing Supplement

## Over Wire Usage

MEOW files are designed to be shared "over wire":
- Copy/paste into SSH sessions
- Embed in scripts and documentation
- Share in terminal-based chat
- Store in version control
- Stream over network connections