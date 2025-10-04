# catpic Protocol Specification

## Overview

catpic is a terminal image viewer that displays images using Unicode mosaic characters and ANSI colors. This document provides an overview of the catpic specifications.

## Core Specifications

The catpic protocol consists of three main specifications:

### 1. MEOW Format Specification
**File**: `spec/meow-format.md`

Defines the MEOW (Mosaic Encoding Over Wire) text-based image format:
- File structure for static images and animations
- BASIS system (pixel subdivision levels)
- Unicode character sets for each BASIS level
- ANSI color encoding
- Encoding algorithm (EnGlyph-based)
- Display requirements and compatibility

### 2. API Specification
**File**: `spec/api.md`

Defines the language-agnostic API that all implementations must provide:
- Encoder API (image → MEOW conversion)
- Decoder API (MEOW → terminal display)
- Player API (animation playback)
- Function signatures and behavior
- Error handling requirements
- Environment variable support

### 3. Compliance Requirements
**File**: `spec/compliance.md`

Defines requirements for compliant implementations:
- Test vector requirements
- API implementation requirements
- Format validation requirements
- Minimum BASIS support
- Documentation requirements
- Testing infrastructure requirements

## Implementation Status

| Language | Status | Compliance |
|----------|--------|------------|
| Python   | ✅ Complete | ✅ Reference |
| C        | 🚧 Planned | ⏳ Pending |
| Rust     | 🚧 Planned | ⏳ Pending |

Python serves as the reference implementation that defines the canonical behavior.

## Design Principles

1. **Text-Based Format**: MEOW files are plain text, suitable for version control and "over wire" transmission
2. **Terminal Native**: Display with standard tools (`cat`) for static images
3. **Language Agnostic**: Same API and behavior across all implementations
4. **Quality Scalable**: BASIS system from universal compatibility (1,2) to ultra quality (2,4)
5. **Modern Unicode**: Uses Unicode 13.0+ block characters for high-quality rendering

## Test Vectors

Canonical test cases are defined in `spec/test-vectors.json`. All implementations must pass these tests to be considered compliant.

## Contributing

When implementing catpic in a new language:

1. Review all three specification documents
2. Implement the complete API from `spec/api.md`
3. Generate valid MEOW format per `spec/meow-format.md`
4. Pass all test vectors in `spec/test-vectors.json`
5. Meet all requirements in `spec/compliance.md`
6. Add test configuration in `<language>/test-config.toml`
7. Document your implementation in `docs/implementations/<language>.md`

See `CONTRIBUTING.md` for detailed contribution guidelines.

## Version History

- **v1.0** (2025-01-27) - Initial protocol specification
  - MEOW format defined
  - API standardized
  - Compliance requirements established