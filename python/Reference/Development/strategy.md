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

# catpic Development Strategy

## Phase Overview

Development is structured in three phases, with each phase building on proven foundations from the EnGlyph project analysis.

## Phase 1: Core Implementation (3-4 weeks)

### Objectives
- Implement working TIMG encoder/decoder with EnGlyph algorithm
- Create functional CLI interface
- Establish comprehensive test suite

### Key Deliverables

#### CatpicEncoder.encode_image()
Replace placeholder with EnGlyph-based implementation:

```python
def encode_image(self, image_path, width=None, height=None):
    # 1. Load and prepare image
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        
    # 2. Calculate dimensions
    basis_x, basis_y = self.core.get_basis_dimensions(self.basis)
    pixel_width = width * basis_x
    pixel_height = height * basis_y
    
    # 3. Resize image
    img_resized = img.resize((pixel_width, pixel_height), Image.Resampling.LANCZOS)
    
    # 4. Process each character cell
    for y in range(height):
        for x in range(width):
            # Extract pixel block
            block = extract_pixel_block(img_resized, x, y, basis_x, basis_y)
            
            # EnGlyph algorithm
            quantized = block.quantize(colors=2)
            pattern = generate_bit_pattern(quantized)
            char = self.core.BLOCKS[self.basis][pattern]
            fg_rgb, bg_rgb = compute_rgb_centroids(block, quantized)
            
            # Format output
            cell = self.core.format_cell(char, fg_rgb, bg_rgb)
```

#### CLI Enhancement
- Improve BASIS parameter validation
- Add progress indicators for large images
- Enhanced error handling and user feedback

#### Test Suite
- Comprehensive unit tests for core functions
- Integration tests with real images
- BASIS system validation tests
- Color accuracy tests

### AI Session Prompts for Phase 1

#### Encoder Implementation
"I need to implement the CatpicEncoder.encode_image() method using the EnGlyph algorithm. The current placeholder implementation needs to be replaced with:

1. Proper pixel block extraction for BASIS (x,y) subdivision
2. PIL.quantize(colors=2) for 2-color reduction per block  
3. Bit pattern generation: pattern += 2**pixel_index
4. RGB centroid calculation for foreground/background colors
5. Unicode character selection from BLOCKS[basis][pattern]

The EnGlyph analysis shows this approach works reliably. Please implement the complete algorithm with proper error handling."

#### Testing Framework
"Create comprehensive tests for the catpic core functionality, focusing on:
- BASIS system character set validation
- Color formatting accuracy  
- Pixel block processing
- Edge cases and error conditions
- Integration tests with sample images

Use pytest and include fixtures for test images."

## Phase 2: Animation Support (2-3 weeks)

### Objectives
- Implement MEOW-ANIM format encoding/decoding
- Create CatpicPlayer with timing controls
- Optimize for animation performance

### Key Features
- GIF frame extraction with PIL.ImageSequence
- Frame-by-frame encoding with shared optimization
- Playback controls (loop, delay override, max loops)
- Memory-efficient frame processing

### AI Session Prompts for Phase 2

#### Animation Encoding
"Implement MEOW-ANIM format support in CatpicEncoder.encode_animation(). Need to:
1. Use PIL.ImageSequence to extract GIF frames
2. Apply same EnGlyph algorithm per frame
3. Generate MEOW-ANIM format with FRAME: sections
4. Handle timing from GIF metadata
5. Optimize for repeated patterns between frames"

#### Player Implementation  
"Create CatpicPlayer.play() method with: format support in TIMGEncoder.encode_animation(). Need to:
1. Use PIL.ImageSequence to extract GIF frames
2. Apply same EnGlyph algorithm per frame
3. Generate TIMA format with FRAME: sections
4. Handle timing from GIF metadata
5. Optimize for repeated patterns between frames"

#### Player Implementation  
"Create TIMGPlayer.play() method with:
- Terminal screen clearing between frames
- Precise timing control with time.sleep()
- Keyboard interrupt handling (Ctrl+C)
- Loop control and frame rate options
- Memory efficient frame loading"

## Phase 3: Integration & Polish (1-2 weeks)

### Objectives
- EnGlyph widget compatibility
- Advanced features and optimizations
- Documentation completion

### Integration Points
- Textual Strip generation from TIMG data
- EnGlyph widget rendering compatibility
- Performance optimizations

### AI Session Prompts for Phase 3

#### EnGlyph Integration
"Add Textual integration to catpic by creating methods that generate EnGlyph-compatible Strip objects from MEOW data. This should allow MEOW files to be displayed in Textual applications seamlessly."

#### Performance Optimization
"Optimize catpic encoding performance for large images and animations:
1. Memory usage optimization for large files
2. Parallel processing for independent blocks
3. Caching strategies for repeated patterns
4. Progressive encoding options"

## Success Criteria

### Phase 1
- [ ] `catpic image.jpg` displays images correctly
- [ ] All BASIS levels implemented and tested
- [ ] CLI displays common image formats
- [ ] 90%+ test coverage on core functionality

### Phase 2  
- [ ] `catpic animation.gif` plays smoothly
- [ ] GIF conversion preserves timing and quality
- [ ] Memory usage reasonable for typical animations
- [ ] Playback controls function correctly

### Phase 3
- [ ] Textual integration working
- [ ] Performance acceptable for production use
- [ ] Documentation complete
- [ ] Ready for public release

## Risk Mitigation

- **Unicode Support**: Test on multiple terminal types early
- **Performance**: Profile with large images in Phase 1
- **Color Accuracy**: Validate against EnGlyph reference
- **Memory Usage**: Monitor during animation development