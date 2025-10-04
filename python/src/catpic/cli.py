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

"""Command-line interface for catpic."""

from pathlib import Path
from typing import Optional

import click

from .core import BASIS
from .decoder import CatpicDecoder, CatpicPlayer
from .encoder import CatpicEncoder


def parse_basis(basis_str: str) -> BASIS:
    """Parse BASIS string to BASIS enum."""
    basis_map = {
        "1,2": BASIS.BASIS_1_2,
        "2,2": BASIS.BASIS_2_2, 
        "2,3": BASIS.BASIS_2_3,
        "2,4": BASIS.BASIS_2_4,
    }
    
    if basis_str not in basis_map:
        raise click.BadParameter(
            f"Invalid BASIS '{basis_str}'. Must be one of: {', '.join(basis_map.keys())}"
        )
    
    return basis_map[basis_str]


@click.group(invoke_without_command=True)
@click.argument('image_file', type=click.Path(exists=True, path_type=Path), required=False)
@click.option('--basis', '-b', default='2,2', help='BASIS level (1,2 | 2,2 | 2,3 | 2,4)')
@click.option('--width', '-w', type=int, help='Display width in characters')
@click.option('--height', '-h', type=int, help='Display height in characters')
@click.option('--delay', '-d', type=int, help='Animation delay in ms (for GIFs)')
@click.version_option(version="0.1.0")
@click.pass_context
def main(ctx, image_file: Optional[Path], basis: str, width: Optional[int], height: Optional[int], delay: Optional[int]):
    """
    catpic - Display images directly in terminal.
    
    Default behavior: Show any image format directly in terminal.
    Use subcommands to generate cat-able .meow files or get info.
    
    Examples:
      catpic photo.jpg                    # Display image directly
      catpic animation.gif                # Play animation directly  
      catpic generate photo.jpg           # Create photo.meow file
      catpic convert animation.gif        # Create animation.meow file
    """
    # If no subcommand and no file, show help
    if ctx.invoked_subcommand is None and image_file is None:
        click.echo(ctx.get_help())
        return
    
    # If file provided without subcommand, display directly
    if ctx.invoked_subcommand is None and image_file is not None:
        try:
            basis_enum = parse_basis(basis)
        except click.BadParameter as e:
            click.echo(f"Error: {e}", err=True)
            return
        
        # Check if it's a MEOW file
        if image_file.suffix.lower() == '.meow':
            # Check if it's animated
            try:
                with open(image_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('MEOW-ANIM/'):
                        player = CatpicPlayer()
                        player.play_file(image_file, delay=delay)
                    else:
                        decoder = CatpicDecoder()
                        decoder.display_file(image_file)
            except Exception as e:
                click.echo(f"Error reading .meow file: {e}", err=True)
        else:
            # Display standard image format directly in terminal
            display_image_directly(image_file, basis_enum, width, height, delay)


def display_image_directly(
    image_file: Path,
    basis: BASIS,
    width: Optional[int],
    height: Optional[int],
    delay: Optional[int]
):
    """Display any standard image format directly in terminal."""
    try:
        from PIL import Image
        with Image.open(image_file) as img:
            is_animated = getattr(img, 'is_animated', False)
    except Exception as e:
        click.echo(f"Error reading image file: {e}", err=True)
        return
    
    try:
        encoder = CatpicEncoder(basis=basis)
        
        if is_animated:
            # Generate MEOW animation content and play directly
            meow_content = encoder.encode_animation(image_file, width, height, delay)
            player = CatpicPlayer()
            player.play(meow_content, delay=delay)
        else:
            # Generate MEOW content and display directly
            meow_content = encoder.encode_image(image_file, width, height)
            decoder = CatpicDecoder()
            decoder.display(meow_content)
            
    except Exception as e:
        click.echo(f"Error displaying image: {e}", err=True)


@main.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--basis', '-b', default='2,2', help='BASIS level (1,2 | 2,2 | 2,3 | 2,4)')
@click.option('--width', '-w', type=int, help='Output width in characters')
@click.option('--height', '-h', type=int, help='Output height in characters')
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output file path')
def generate(
    input_file: Path,
    basis: str,
    width: Optional[int],
    height: Optional[int],
    output: Optional[Path]
):
    """Generate cat-able .meow file from static image."""
    try:
        basis_enum = parse_basis(basis)
    except click.BadParameter as e:
        click.echo(f"Error: {e}", err=True)
        return
    
    # Verify it's not animated
    try:
        from PIL import Image
        with Image.open(input_file) as img:
            if getattr(img, 'is_animated', False):
                click.echo("Error: Use 'convert' command for animated images", err=True)
                return
    except Exception as e:
        click.echo(f"Error reading input file: {e}", err=True)
        return
    
    encoder = CatpicEncoder(basis=basis_enum)
    
    try:
        result = encoder.encode_image(input_file, width, height)
        
        # Determine output path
        if output is None:
            output = input_file.with_suffix('.meow')
        
        # Write output
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        
        click.echo(f"Generated '{output}' from '{input_file}'")
        click.echo(f"Display with: cat {output}")
        
    except Exception as e:
        click.echo(f"Error during generation: {e}", err=True)


@main.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--basis', '-b', default='2,2', help='BASIS level (1,2 | 2,2 | 2,3 | 2,4)')
@click.option('--width', '-w', type=int, help='Output width in characters')
@click.option('--height', '-h', type=int, help='Output height in characters')
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output file path')
@click.option('--delay', '-d', type=int, help='Animation delay in ms')
def convert(
    input_file: Path,
    basis: str,
    width: Optional[int],
    height: Optional[int],
    output: Optional[Path],
    delay: Optional[int]
):
    """Convert animated image to cat-able .meow file."""
    try:
        basis_enum = parse_basis(basis)
    except click.BadParameter as e:
        click.echo(f"Error: {e}", err=True)
        return
    
    # Verify it's animated
    try:
        from PIL import Image
        with Image.open(input_file) as img:
            if not getattr(img, 'is_animated', False):
                click.echo("Error: Use 'generate' command for static images", err=True)
                return
    except Exception as e:
        click.echo(f"Error reading input file: {e}", err=True)
        return
    
    encoder = CatpicEncoder(basis=basis_enum)
    
    try:
        result = encoder.encode_animation(input_file, width, height, delay)
        
        # Determine output path
        if output is None:
            output = input_file.with_suffix('.meow')
        
        # Write output
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        
        click.echo(f"Converted '{input_file}' to '{output}'")
        click.echo(f"Display with: cat {output}")
        click.echo(f"Or play directly with: catpic {output}")
        
    except Exception as e:
        click.echo(f"Error during conversion: {e}", err=True)


@main.command()
@click.argument('meow_file', type=click.Path(exists=True, path_type=Path))
def info(meow_file: Path):
    """Display MEOW file information."""
    try:
        with open(meow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        decoder = CatpicDecoder()
        parsed = decoder.parse_meow(content)
        
        click.echo(f"File: {meow_file}")
        click.echo(f"Format: {parsed.get('format', 'Unknown')}")
        click.echo(f"Dimensions: {parsed.get('width', '?')}×{parsed.get('height', '?')}")
        click.echo(f"BASIS: {parsed.get('basis', '?')}")
        
        if parsed['format'].startswith('MEOW-ANIM/'):
            click.echo(f"Frames: {parsed.get('frames_count', len(parsed.get('frames', [])))}")
            click.echo(f"Delay: {parsed.get('delay', '?')}ms")
        
        # File size
        file_size = meow_file.stat().st_size
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        
        click.echo(f"File size: {size_str}")
        
    except Exception as e:
        click.echo(f"Error reading file: {e}", err=True)


if __name__ == '__main__':
    main() ---

"""Command-line interface for TIMG."""

from pathlib import Path
from typing import Optional

import click

from .core import BASIS
from .decoder import TIMGDecoder, TIMGPlayer
from .encoder import TIMGEncoder


def parse_basis(basis_str: str) -> BASIS:
    """Parse BASIS string to BASIS enum."""
    basis_map = {
        "1,2": BASIS.BASIS_1_2,
        "2,2": BASIS.BASIS_2_2, 
        "2,3": BASIS.BASIS_2_3,
        "2,4": BASIS.BASIS_2_4,
    }
    
    if basis_str not in basis_map:
        raise click.BadParameter(
            f"Invalid BASIS '{basis_str}'. Must be one of: {', '.join(basis_map.keys())}"
        )
    
    return basis_map[basis_str]


@click.group(invoke_without_command=True)
@click.argument('image_file', type=click.Path(exists=True, path_type=Path), required=False)
@click.option('--basis', '-b', default='2,2', help='BASIS level (1,2 | 2,2 | 2,3 | 2,4)')
@click.option('--width', '-w', type=int, help='Display width in characters')
@click.option('--height', '-h', type=int, help='Display height in characters')
@click.option('--delay', '-d', type=int, help='Animation delay in ms (for GIFs)')
@click.version_option(version="0.1.0")
@click.pass_context
def main(ctx, image_file: Optional[Path], basis: str, width: Optional[int], height: Optional[int], delay: Optional[int]):
    """
    TIMG - Display images directly in terminal.
    
    Default behavior: Show any image format directly in terminal.
    Use subcommands to generate cat-able files or get info.
    
    Examples:
      timg photo.jpg                    # Display image directly
      timg animation.gif                # Play animation directly  
      timg generate photo.jpg           # Create photo.timg file
      timg convert animation.gif        # Create animation.tima file
    """
    # If no subcommand and no file, show help
    if ctx.invoked_subcommand is None and image_file is None:
        click.echo(ctx.get_help())
        return
    
    # If file provided without subcommand, display directly
    if ctx.invoked_subcommand is None and image_file is not None:
        try:
            basis_enum = parse_basis(basis)
        except click.BadParameter as e:
            click.echo(f"Error: {e}", err=True)
            return
        
        # Check if it's a TIMG/TIMA file
        if image_file.suffix.lower() in ['.timg', '.tima']:
            if image_file.suffix.lower() == '.tima':
                player = TIMGPlayer()
                player.play_file(image_file, delay=delay)
            else:
                decoder = TIMGDecoder()
                decoder.display_file(image_file)
        else:
            # Display standard image format directly in terminal
            display_image_directly(image_file, basis_enum, width, height, delay)


def display_image_directly(
    image_file: Path,
    basis: BASIS,
    width: Optional[int],
    height: Optional[int],
    delay: Optional[int]
):
    """Display any standard image format directly in terminal."""
    try:
        from PIL import Image
        with Image.open(image_file) as img:
            is_animated = getattr(img, 'is_animated', False)
    except Exception as e:
        click.echo(f"Error reading image file: {e}", err=True)
        return
    
    try:
        encoder = TIMGEncoder(basis=basis)
        
        if is_animated:
            # Generate TIMA content and play directly
            tima_content = encoder.encode_animation(image_file, width, height, delay)
            player = TIMGPlayer()
            player.play(tima_content, delay=delay)
        else:
            # Generate TIMG content and display directly
            timg_content = encoder.encode_image(image_file, width, height)
            decoder = TIMGDecoder()
            decoder.display(timg_content)
            
    except Exception as e:
        click.echo(f"Error displaying image: {e}", err=True)


@main.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--basis', '-b', default='2,2', help='BASIS level (1,2 | 2,2 | 2,3 | 2,4)')
@click.option('--width', '-w', type=int, help='Output width in characters')
@click.option('--height', '-h', type=int, help='Output height in characters')
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output file path')
def generate(
    input_file: Path,
    basis: str,
    width: Optional[int],
    height: Optional[int],
    output: Optional[Path]
):
    """Generate cat-able .timg file from static image."""
    try:
        basis_enum = parse_basis(basis)
    except click.BadParameter as e:
        click.echo(f"Error: {e}", err=True)
        return
    
    # Verify it's not animated
    try:
        from PIL import Image
        with Image.open(input_file) as img:
            if getattr(img, 'is_animated', False):
                click.echo("Error: Use 'convert' command for animated images", err=True)
                return
    except Exception as e:
        click.echo(f"Error reading input file: {e}", err=True)
        return
    
    encoder = TIMGEncoder(basis=basis_enum)
    
    try:
        result = encoder.encode_image(input_file, width, height)
        
        # Determine output path
        if output is None:
            output = input_file.with_suffix('.timg')
        
        # Write output
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        
        click.echo(f"Generated '{output}' from '{input_file}'")
        click.echo(f"Display with: cat {output}")
        
    except Exception as e:
        click.echo(f"Error during generation: {e}", err=True)


@main.command()
@click.argument('input_file', type=click.Path(exists=True, path_type=Path))
@click.option('--basis', '-b', default='2,2', help='BASIS level (1,2 | 2,2 | 2,3 | 2,4)')
@click.option('--width', '-w', type=int, help='Output width in characters')
@click.option('--height', '-h', type=int, help='Output height in characters')
@click.option('--output', '-o', type=click.Path(path_type=Path), help='Output file path')
@click.option('--delay', '-d', type=int, help='Animation delay in ms')
def convert(
    input_file: Path,
    basis: str,
    width: Optional[int],
    height: Optional[int],
    output: Optional[Path],
    delay: Optional[int]
):
    """Convert animated image to cat-able .tima file."""
    try:
        basis_enum = parse_basis(basis)
    except click.BadParameter as e:
        click.echo(f"Error: {e}", err=True)
        return
    
    # Verify it's animated
    try:
        from PIL import Image
        with Image.open(input_file) as img:
            if not getattr(img, 'is_animated', False):
                click.echo("Error: Use 'generate' command for static images", err=True)
                return
    except Exception as e:
        click.echo(f"Error reading input file: {e}", err=True)
        return
    
    encoder = TIMGEncoder(basis=basis_enum)
    
    try:
        result = encoder.encode_animation(input_file, width, height, delay)
        
        # Determine output path
        if output is None:
            output = input_file.with_suffix('.tima')
        
        # Write output
        with open(output, 'w', encoding='utf-8') as f:
            f.write(result)
        
        click.echo(f"Converted '{input_file}' to '{output}'")
        click.echo(f"Display with: cat {output}")
        click.echo(f"Or play directly with: timg {output}")
        
    except Exception as e:
        click.echo(f"Error during conversion: {e}", err=True)


@main.command()
@click.argument('timg_file', type=click.Path(exists=True, path_type=Path))
def info(timg_file: Path):
    """Display TIMG/TIMA file information."""
    try:
        with open(timg_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        decoder = TIMGDecoder()
        parsed = decoder.parse_timg(content)
        
        click.echo(f"File: {timg_file}")
        click.echo(f"Format: {parsed.get('format', 'Unknown')}")
        click.echo(f"Dimensions: {parsed.get('width', '?')}×{parsed.get('height', '?')}")
        click.echo(f"BASIS: {parsed.get('basis', '?')}")
        
        if parsed['format'].startswith('TIMA/'):
            click.echo(f"Frames: {parsed.get('frames_count', len(parsed.get('frames', [])))}")
            click.echo(f"Delay: {parsed.get('delay', '?')}ms")
        
        # File size
        file_size = timg_file.stat().st_size
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        
        click.echo(f"File size: {size_str}")
        
    except Exception as e:
        click.echo(f"Error reading file: {e}", err=True)


if __name__ == '__main__':
    main()