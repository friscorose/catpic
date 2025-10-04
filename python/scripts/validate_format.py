# ---
# ## AI Collaboration Context
# **Project:** catpic - Terminal Image Viewer | **Session:** #1 | **Date:** 2025-01-27 | **Lead:** [Your Name]  
# **AI Model:** Claude Sonnet 4 | **Objective:** Create comprehensive catpic project structure
# **Prior Work:** Initial session  
# **Current Status:** Complete project scaffolding with BASIS system and EnGlyph integration. Renamed to catpic with .meow extension
# **Files in Scope:** New project - all files created  
# **Human Contributions:** Requirements analysis, EnGlyph research, BASIS system design, development strategy, UX design (viewer-first approach), naming (catpic/.meow)  
# **AI Contributions:** Project structure, code generation, documentation, testing framework  
# **Pending Decisions:** Phase 1 implementation approach, specific BASIS character sets for 2,3 and 2,4
# ---

"""MEOW format validation script."""

import sys
from pathlib import Path
from typing import Dict, Any

def validate_meow_format(file_path: Path) -> Dict[str, Any]:
    """Validate MEOW file format compliance."""
    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'metadata': {}
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result['valid'] = False
        result['errors'].append(f"Cannot read file: {e}")
        return result
    
    lines = content.strip().split('\n')
    
    if not lines:
        result['valid'] = False
        result['errors'].append("Empty file")
        return result
    
    # Validate header
    header = lines[0]
    if not header.startswith(('MEOW/', 'MEOW-ANIM/')):
        result['valid'] = False
        result['errors'].append(f"Invalid header: {header}")
        return result
    
    result['metadata']['format'] = header
    
    # Parse metadata
    data_start = None
    for i, line in enumerate(lines[1:], 1):
        if line == "DATA:":
            data_start = i + 1
            break
        elif ':' in line:
            key, value = line.split(':', 1)
            if key in ['WIDTH', 'HEIGHT', 'FRAMES', 'DELAY']:
                try:
                    result['metadata'][key.lower()] = int(value)
                except ValueError:
                    result['errors'].append(f"Invalid {key} value: {value}")
            else:
                result['metadata'][key.lower()] = value
    
    if data_start is None:
        result['valid'] = False
        result['errors'].append("No DATA: section found")
        return result
    
    # Validate required metadata
    required = ['WIDTH', 'HEIGHT', 'BASIS']
    for req in required:
        if req.lower() not in result['metadata']:
            result['errors'].append(f"Missing required field: {req}")
    
    # Validate BASIS format
    if 'basis' in result['metadata']:
        try:
            basis_parts = result['metadata']['basis'].split(',')
            if len(basis_parts) != 2:
                result['errors'].append(f"Invalid BASIS format: {result['metadata']['basis']}")
            else:
                basis_x, basis_y = map(int, basis_parts)
                if basis_x < 1 or basis_y < 1:
                    result['errors'].append(f"Invalid BASIS values: {basis_x},{basis_y}")
                result['metadata']['basis_x'] = basis_x
                result['metadata']['basis_y'] = basis_y
        except ValueError:
            result['errors'].append(f"Invalid BASIS format: {result['metadata']['basis']}")
    
    # Validate data section
    data_lines = lines[data_start:]
    expected_height = result['metadata'].get('height', 0)
    
    if header.startswith('MEOW-ANIM/'):
        # Animation validation
        frame_count = 0
        current_frame_lines = 0
        in_frame = False
        
        for line in data_lines:
            if line.startswith("FRAME:"):
                if in_frame and current_frame_lines != expected_height:
                    result['warnings'].append(f"Frame {frame_count} has {current_frame_lines} lines, expected {expected_height}")
                frame_count += 1
                current_frame_lines = 0
                in_frame = True
            elif in_frame:
                current_frame_lines += 1
        
        if in_frame and current_frame_lines != expected_height:
            result['warnings'].append(f"Last frame has {current_frame_lines} lines, expected {expected_height}")
        
        expected_frames = result['metadata'].get('frames', 0)
        if frame_count != expected_frames:
            result['warnings'].append(f"Found {frame_count} frames, expected {expected_frames}")
    
    else:
        # Static image validation
        if len(data_lines) != expected_height:
            result['warnings'].append(f"Found {len(data_lines)} lines, expected {expected_height}")
    
    # Validate ANSI sequences
    ansi_pattern_count = 0
    for line in data_lines:
        if not line.startswith("FRAME:"):
            ansi_pattern_count += line.count('\x1b[38;2;')
    
    if ansi_pattern_count == 0:
        result['warnings'].append("No ANSI color sequences found")
    
    result['valid'] = len(result['errors']) == 0
    return result


def main():
    """CLI for format validation."""
    if len(sys.argv) != 2:
        print("Usage: python validate_format.py <meow_file>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    
    result = validate_meow_format(file_path)
    
    print(f"Validating: {file_path}")
    print(f"Format: {result['metadata'].get('format', 'Unknown')}")
    print(f"Valid: {'✓' if result['valid'] else '✗'}")
    
    if result['metadata']:
        print("\nMetadata:")
        for key, value in result['metadata'].items():
            if key != 'format':
                print(f"  {key}: {value}")
    
    if result['errors']:
        print(f"\nErrors ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"  ✗ {error}")
    
    if result['warnings']:
        print(f"\nWarnings ({len(result['warnings'])}):")
        for warning in result['warnings']:
            print(f"# ---
# ## AI Collaboration Context
# **Project:** TIMG - Terminal Image Format | **Session:** #1 | **Date:** 2025-01-27 | **Lead:** [Your Name]  
# **AI Model:** Claude Sonnet 4 | **Objective:** Create comprehensive TIMG project structure
# **Prior Work:** Initial session  
# **Current Status:** Complete project scaffolding with BASIS system and EnGlyph integration
# **Files in Scope:** New project - all files created  
# **Human Contributions:** Requirements analysis, EnGlyph research, BASIS system design, development strategy  
# **AI Contributions:** Project structure, code generation, documentation, testing framework  
# **Pending Decisions:** Phase 1 implementation approach, specific BASIS character sets for 2,3 and 2,4
# ---

"""TIMG format validation script."""

import sys
from pathlib import Path
from typing import Dict, Any

def validate_timg_format(file_path: Path) -> Dict[str, Any]:
    """Validate TIMG/TIMA file format compliance."""
    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'metadata': {}
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result['valid'] = False
        result['errors'].append(f"Cannot read file: {e}")
        return result
    
    lines = content.strip().split('\n')
    
    if not lines:
        result['valid'] = False
        result['errors'].append("Empty file")
        return result
    
    # Validate header
    header = lines[0]
    if not header.startswith(('TIMG/', 'TIMA/')):
        result['valid'] = False
        result['errors'].append(f"Invalid header: {header}")
        return result
    
    result['metadata']['format'] = header
    
    # Parse metadata
    data_start = None
    for i, line in enumerate(lines[1:], 1):
        if line == "DATA:":
            data_start = i + 1
            break
        elif ':' in line:
            key, value = line.split(':', 1)
            if key in ['WIDTH', 'HEIGHT', 'FRAMES', 'DELAY']:
                try:
                    result['metadata'][key.lower()] = int(value)
                except ValueError:
                    result['errors'].append(f"Invalid {key} value: {value}")
            else:
                result['metadata'][key.lower()] = value
    
    if data_start is None:
        result['valid'] = False
        result['errors'].append("No DATA: section found")
        return result
    
    # Validate required metadata
    required = ['WIDTH', 'HEIGHT', 'BASIS']
    for req in required:
        if req.lower() not in result['metadata']:
            result['errors'].append(f"Missing required field: {req}")
    
    # Validate BASIS format
    if 'basis' in result['metadata']:
        try:
            basis_parts = result['metadata']['basis'].split(',')
            if len(basis_parts) != 2:
                result['errors'].append(f"Invalid BASIS format: {result['metadata']['basis']}")
            else:
                basis_x, basis_y = map(int, basis_parts)
                if basis_x < 1 or basis_y < 1:
                    result['errors'].append(f"Invalid BASIS values: {basis_x},{basis_y}")
                result['metadata']['basis_x'] = basis_x
                result['metadata']['basis_y'] = basis_y
        except ValueError:
            result['errors'].append(f"Invalid BASIS format: {result['metadata']['basis']}")
    
    # Validate data section
    data_lines = lines[data_start:]
    expected_height = result['metadata'].get('height', 0)
    
    if header.startswith('TIMA/'):
        # Animation validation
        frame_count = 0
        current_frame_lines = 0
        in_frame = False
        
        for line in data_lines:
            if line.startswith("FRAME:"):
                if in_frame and current_frame_lines != expected_height:
                    result['warnings'].append(f"Frame {frame_count} has {current_frame_lines} lines, expected {expected_height}")
                frame_count += 1
                current_frame_lines = 0
                in_frame = True
            elif in_frame:
                current_frame_lines += 1
        
        if in_frame and current_frame_lines != expected_height:
            result['warnings'].append(f"Last frame has {current_frame_lines} lines, expected {expected_height}")
        
        expected_frames = result['metadata'].get('frames', 0)
        if frame_count != expected_frames:
            result['warnings'].append(f"Found {frame_count} frames, expected {expected_frames}")
    
    else:
        # Static image validation
        if len(data_lines) != expected_height:
            result['warnings'].append(f"Found {len(data_lines)} lines, expected {expected_height}")
    
    # Validate ANSI sequences
    ansi_pattern_count = 0
    for line in data_lines:
        if not line.startswith("FRAME:"):
            ansi_pattern_count += line.count('\x1b[38;2;')
    
    if ansi_pattern_count == 0:
        result['warnings'].append("No ANSI color sequences found")
    
    result['valid'] = len(result['errors']) == 0
    return result


def main():
    """CLI for format validation."""
    if len(sys.argv) != 2:
        print("Usage: python validate_format.py <timg_file>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    
    result = validate_timg_format(file_path)
    
    print(f"Validating: {file_path}")
    print(f"Format: {result['metadata'].get('format', 'Unknown')}")
    print(f"Valid: {'✓' if result['valid'] else '✗'}")
    
    if result['metadata']:
        print("\nMetadata:")
        for key, value in result['metadata'].items():
            if key != 'format':
                print(f"  {key}: {value}")
    
    if result['errors']:
        print(f"\nErrors ({len(result['errors'])}):")
        for error in result['errors']:
            print(f"  ✗ {error}")
    
    if result['warnings']:
        print(f"\nWarnings ({len(result['warnings'])}):")
        for warning in result['warnings']:
            print(f"  ⚠ {warning}")
    
    if result['valid']:
        print("\n✓ File format is valid!")
        sys.exit(0)
    else:
        print(f"\n✗ File format has {len(result['errors'])} errors")
        sys.exit(1)


if __name__ == '__main__':
    main()