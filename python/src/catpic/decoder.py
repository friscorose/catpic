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
        max_loops: Optional[int] = None,
        force: bool = False
    ) -> None:
        """
        Play MEOW animation content with reduced flicker.
        
        Animation plays at current cursor position instead of clearing screen.
        Saves cursor position before starting, restores after.
        
        Auto-truncates animation height to fit terminal unless force=True.
        
        Args:
            content: MEOW-ANIM format string
            delay: Override frame delay in milliseconds
            loop: Loop animation indefinitely
            max_loops: Maximum number of loops
            force: If True, skip auto-truncation and play full size
        
        Flicker reduction techniques:
        1. Save/restore cursor position
        2. Hide cursor during playback
        3. Use saved position (\x1b[u) to return to start of animation
        4. Buffer entire frame before outputting
        5. Single flush per frame
        """
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
        
        # Get animation height
        anim_height = parsed.get('height', 0)
        
        # Check terminal height and auto-truncate if needed
        import os
        import shutil
        
        terminal_size = shutil.get_terminal_size(fallback=(80, 24))
        terminal_height = terminal_size.lines
        
        # Determine display height
        if force or anim_height <= terminal_height:
            # Use full height
            display_height = anim_height
            truncated = False
        else:
            # Auto-truncate to fit terminal
            # Reserve 3 lines: current line, animation, and one for cursor after
            display_height = max(1, terminal_height - 3)
            truncated = True
            print(f"Note: Animation truncated to {display_height} lines (terminal height: {terminal_height}). Use --force to disable.", file=sys.stderr)
        
        # Use provided delay or file delay or default
        frame_delay = delay or parsed.get('delay', 100)
        delay_seconds = frame_delay / 1000.0
        
        frames = parsed['frames']
        loop_count = 0
        
        # Get expected line width from metadata
        # Each character position has ANSI codes, so we can't use simple len()
        # Instead, clear any partial lines by moving to column 0 and clearing to end
        frame_width = parsed.get('width', 80)
        
        # Save cursor position and hide cursor
        # \x1b[s = save cursor position
        # \x1b[?25l = hide cursor
        print('\x1b[s\x1b[?25l', end='', flush=True)
        
        try:
            while True:
                for frame_data in frames:
                    # Build frame using cursor positioning, no newlines
                    # \x1b[u = restore to saved position
                    output_buffer = ['\x1b[u']
                    
                    for idx, line in enumerate(frame_data['lines']):
                        if idx >= display_height:
                            break
                        
                        # Output line content
                        output_buffer.append(line)
                        
                        # Clear to end of line (removes artifacts)
                        output_buffer.append('\x1b[K')
                        
                        # Move to next line (down 1, column 0) - but not after last line
                        if idx < display_height - 1:
                            output_buffer.append('\x1b[B\x1b[G')
                    
                    # Output entire frame at once
                    print(''.join(output_buffer), end='', flush=True)
                    
                    # Wait for next frame
                    time.sleep(delay_seconds)
                
                if not loop:
                    break
                
                loop_count += 1
                if max_loops is not None and loop_count >= max_loops:
                    break
                    
        except KeyboardInterrupt:
            pass
        finally:
            # Restore cursor position, show cursor
            print('\x1b[u\x1b[?25h', end='', flush=True)
            # Move cursor below animation
            # Use exact positioning: down display_height lines, then one more for new prompt
            if display_height > 0:
                for _ in range(display_height):
                    print('\x1b[B', end='')
                print()  # Final newline for prompt
    
    def play_file(
        self, 
        meow_path: Union[str, Path],
        delay: Optional[int] = None,
        loop: bool = True,
        max_loops: Optional[int] = None,
        force: bool = False
    ) -> None:
        """Play MEOW animation file."""
        try:
            with open(meow_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.play(content, delay, loop, max_loops, force)
        except FileNotFoundError:
            print(f"Error: File '{meow_path}' not found", file=sys.stderr)
        except UnicodeDecodeError:
            print(f"Error: Cannot decode file '{meow_path}' as UTF-8", file=sys.stderr)
