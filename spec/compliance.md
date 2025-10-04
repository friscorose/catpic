# Compliance Requirements

All catpic implementations MUST meet these requirements to be considered compliant.

## 1. Test Vectors

**Requirement**: Pass all test cases in `spec/test-vectors.json`

### Test Execution
- Run test vectors using implementation's test suite
- Compare output byte-for-byte with expected results
- All tests MUST pass for compliance

### Test Coverage
- Static image encoding (all BASIS levels)
- Animation encoding
- Format parsing
- Error handling

## 2. API Implementation

**Requirement**: Implement the complete API defined in `spec/api.md`

### Required Components
- Encoder class/module with:
  - Constructor accepting BASIS parameter or using environment variable
  - `encode_image()` method
  - `encode_animation()` method
- Decoder class/module with:
  - `display()` method
  - `display_file()` method
- Player class/module with:
  - `play()` method
  - `play_file()` method

### API Behavior
- Function signatures MUST match specification (adjusted for language conventions)
- Parameter order MUST match specification
- Return types MUST be equivalent
- Error conditions MUST be handled as specified

## 3. MEOW Format

**Requirement**: Generate and parse valid MEOW format per `spec/meow-format.md`

### Output Format
- Header fields in correct order
- Valid ANSI escape sequences
- UTF-8 encoding
- Proper line termination

### Format Validation
- Parse all required header fields
- Validate BASIS values
- Verify dimension consistency
- Handle malformed input gracefully

## 4. EnGlyph Algorithm

**Requirement**: Use the EnGlyph encoding algorithm

### Algorithm Steps
All implementations MUST follow the encoding algorithm:
1. Resize to exact pixel dimensions (WIDTH × BASIS_X, HEIGHT × BASIS_Y)
2. Extract pixel blocks
3. 2-color quantization per block
4. Bit pattern generation (row-major order)
5. Character selection from BASIS table
6. RGB centroid calculation for fg/bg colors
7. ANSI color formatting

### Output Consistency
- Same input image MUST produce visually equivalent output across implementations
- Character selection MUST be identical for same BASIS level
- Color centroids MAY vary slightly due to quantization algorithm differences, but MUST be visually similar

## 5. BASIS Support

**Requirement**: Support minimum BASIS levels

### Required
- BASIS 2,2 (16 patterns) - MUST implement

### Recommended
- BASIS 1,2 (4 patterns) - SHOULD implement for maximum compatibility
- BASIS 2,3 (64 patterns) - SHOULD implement for quality

### Optional
- BASIS 2,4 (256 patterns) - MAY implement

### Character Sets
- MUST use character sets defined in `spec/meow-format.md`
- Character-to-pattern mapping MUST be consistent across implementations

## 6. Error Handling

**Requirement**: Handle errors consistently

### Required Error Detection
- File not found
- Invalid image format
- Invalid MEOW format
- Missing required headers
- Dimension mismatches
- Invalid BASIS values
- Not an animation (when expected)

### Error Reporting
- Write error messages to stderr (or language equivalent)
- Provide clear, actionable error messages
- Exit with non-zero status for CLI tools
- Throw exceptions or return error codes for libraries

## 7. Environment Variables

**Requirement**: Support `CATPIC_BASIS` environment variable

### Behavior
- Read `CATPIC_BASIS` when no explicit basis provided
- Accept formats: "2,2" or "2x2" or "2_2"
- Fall back to BASIS 2,2 if invalid or not set
- Document environment variable in implementation

## 8. Display Requirements

**Requirement**: Correctly display MEOW content in terminals

### Static Images
- Display with `cat filename.meow` works correctly
- ANSI colors render properly
- Unicode characters display correctly
- No extra newlines or spacing

### Animations
- Frame timing honors DELAY field
- Screen clears between frames
- Ctrl+C stops playback cleanly
- Terminal state restored on exit

## 9. Documentation

**Requirement**: Provide implementation-specific documentation

### Required Documentation
- Installation instructions
- Basic usage examples
- API reference
- Building/testing instructions
- Supported BASIS levels

### Language-Specific Guides
- Located in `docs/implementations/<language>.md`
- Link from root README.md

## 10. Testing Infrastructure

**Requirement**: Provide test suite

### Test Suite
- Unit tests for core functionality
- Integration tests for complete workflows
- Compliance tests using `spec/test-vectors.json`
- Test configuration in `<language>/test-config.toml`

### Test Configuration Format
```toml
[test]
command = "make test"
working_dir = "."

[compliance]
command = "make test-vectors"
expected_exit = 0
```

## Validation Checklist

Before marking an implementation as compliant, verify:

- [ ] All test vectors pass
- [ ] API matches specification
- [ ] MEOW format output is valid
- [ ] EnGlyph algorithm implemented correctly
- [ ] BASIS 2,2 supported (minimum)
- [ ] Errors handled consistently
- [ ] CATPIC_BASIS environment variable supported
- [ ] Display works in terminal
- [ ] Documentation complete
- [ ] Test suite provided
- [ ] `test-config.toml` created

## Non-Compliance Consequences

Implementations that do not meet these requirements:
- MUST NOT be marked as "compliant" in project documentation
- SHOULD be marked as "in development" or "experimental"
- MAY be included in repository but clearly labeled

## Compliance Testing

Use the root-level test script:
```bash
./scripts/test-all.sh <language>
```

This script:
1. Reads `<language>/test-config.toml`
2. Runs test suite
3. Runs compliance tests
4. Reports pass/fail status

## Version History

- **v1.0** (2025-01-27) - Initial compliance requirements