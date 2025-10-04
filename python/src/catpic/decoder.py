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

"""catpic decoding and display functionality."""

import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Union


class CatpicDecoder:
    """Decoder for displaying MEOW format images."""
    
    def __init__(self):
        """Initialize decoder."""
        pass
    
    def parse_meow(self, content: str) -> Dict[str, Union[str, int, List[str]]]:
        """Parse MEOW content and extract metadata and data."""
        lines = content.strip().split('\n')
        
        if not lines or not lines[0].startswith(('MEOW/', 'MEOW-ANIM/')):
            raise ValueError("Invalid MEOW format: missing header")
        
        format_type = lines[0]
        metadata = {'format': format_type}
        data_lines = []
        in_data_section = False
        current_frame_lines = []
        frames = []
        current_frame = None
        
        for line in lines[1:]:
            if line == "DATA:":
                in_data_section = True
                continue
            
            if not in_data_section:
                # Parse metadata
                if ':' in line:
                    key, value = line.split(':', 1)
                    if key in ['WIDTH', 'HEIGHT', 'FRAMES', 'DELAY']:
                        metadata[key.lower()] = int(value)
                    else:
                        metadata[key.lower()] = value
            else:
                # Handle frame data for animations
                if line.startswith("FRAME:"):
                    if current_frame is not None:
                        frames.append({
                            'frame': current_frame,
                            'lines': current_frame_lines
                        })
                    current_frame = int(line.split(':', 1)[1])
                    current_frame_lines = []
                else:
                    if format_type.startswith('MEOW-ANIM/'):
                        current_frame_lines.append(line)
                    else:
                        data_lines.append(line)
        
        # Handle last frame for animations
        if current_frame is not None:
            frames.append({
                'frame': current_frame,
                'lines': current_frame_lines
            })
        
        if format_type.startswith('MEOW-ANIM/'):
            metadata['frames'] = frames
        else:
            metadata['data_lines'] = data_lines
        
        return metadata
    
    def display(self, content: str, file=None) -> None:
        """Display MEOW content to terminal."""
        if file is None:
            file = sys.stdout
        
        try:
            parsed = self.parse_meow(content)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return
        
        if parsed['format'].startswith('MEOW-ANIM/'):
            # Animation - display first frame only
            if 'frames' in parsed and parsed['frames']:
                for line in parsed['frames'][0]['lines']:
                    print(line, file=file)
            else:
                print("Error: No frames found in animation", file=sys.stderr)
        else:
            # Static image
            if 'data_lines' in parsed:
                for line in parsed['data_lines']:
                    print(line, file=file)
            else:
                print("Error: No image data found", file=sys.stderr)
    
    def display_file(self, meow_path: Union[str, Path], file=None) -> None:
        """Display MEOW file contents."""
        try:
            with open(meow_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.display(content, file)
        except FileNotFoundError:
            print(f"Error: File '{meow_path}' not found", file=sys.stderr)
        except UnicodeDecodeError:
            print(f"Error: Cannot decode file '{meow_path}' as UTF-8", file=sys.stderr)


class CatpicPlayer:
    """Player for MEOW animated images."""
    
    def __init__(self):
        """Initialize player."""
        self.decoder = CatpicDecoder()
    
    def play(
        self, 
        content: str, 
        delay: Optional[int] = None,
        loop: bool = True,
        max_loops: Optional[int] = None
    ) -> None:
        """Play MEOW animation content."""
        try:
            parsed = self.decoder.parse_meow(content)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return
        
        if not parsed['format'].startswith('MEOW-ANIM/'):
            print("Error: Not an animation file", file=sys.stderr)
            return
        
        if 'frames' not in parsed or not parsed['frames']:
            print("Error: No frames found in animation", file=sys.stderr)
            return
        
        # Use provided delay or file delay or default
        frame_delay = delay or parsed.get('delay', 100)
        delay_seconds = frame_delay / 1000.0
        
        frames = parsed['frames']
        loop_count = 0
        
        try:
            while True:
                for frame_data in frames:
                    # Clear screen (move cursor to top-left)
                    print('\x1b[H\x1b[2J', end='', flush=True)
                    
                    # Display frame
                    for line in frame_data['lines']:
                        print(line)
                    
                    # Wait for next frame
                    time.sleep(delay_seconds)
                
                if not loop:
                    break
                
                loop_count += 1
                if max_loops is not None and loop_count >= max_loops:
                    break
                    
        except KeyboardInterrupt:
            # Restore cursor and clear screen on Ctrl+C
            print('\x1b[?25h\x1b[H\x1b[2J', end='', flush=True)
    
    def play_file(
        self, 
        meow_path: Union[str, Path],
        delay: Optional[int] = None,
        loop: bool = True,
        max_loops: Optional[int] = None
    ) -> None:
        """Play MEOW animation file."""
        try:
            with open(meow_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.play(content, delay, loop, max_loops)
        except FileNotFoundError:
            print(f"Error: File '{meow_path}' not found", file=sys.stderr)
        except UnicodeDecodeError:
            print(f"Error: Cannot decode file '{meow_path}' as UTF-8", file=sys.stderr)