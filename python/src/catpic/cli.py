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
@click.argument(
    "image_file", type=click.Path(exists=True, path_type=Path), required=False
)
@click.option("--basis", "-b", default="2,2", help="BASIS level (1,2 | 2,2 | 2,3 | 2,4)")
@click.option("--width", "-w", type=int, help="Display width in characters")
@click.option("--height", "-h", type=int, help="Display height in characters")
@click.option("--delay", "-d", type=int, help="Animation delay in ms (for GIFs)")
@click.version_option(version="0.1.0")
@click.pass_context
def main(
    ctx: click.Context,
    image_file: Optional[Path],
    basis: str,
    width: Optional[int],
    height: Optional[int],
    delay: Optional[int],
) -> None:
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
            ctx.exit(1)

        # Check if it's a MEOW file
        if image_file.suffix.lower() == ".meow":
            display_meow_file(image_file, delay)
        else:
            # Display standard image format directly in terminal
            display_image_directly(image_file, basis_enum, width, height, delay)


def display_meow_file(meow_file: Path, delay: Optional[int]) -> None:
    """Display or play a .meow file."""
    try:
        with open(meow_file, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line.startswith("MEOW-ANIM/"):
                player = CatpicPlayer()
                player.play_file(meow_file, delay=delay)
            else:
                decoder = CatpicDecoder()
                decoder.display_file(meow_file)
    except Exception as e:
        click.echo(f"Error reading .meow file: {e}", err=True)


def display_image_directly(
    image_file: Path,
    basis: BASIS,
    width: Optional[int],
    height: Optional[int],
    delay: Optional[int],
) -> None:
    """Display any standard image format directly in terminal."""
    try:
        from PIL import Image

        with Image.open(image_file) as img:
            is_animated = getattr(img, "is_animated", False)
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
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option("--basis", "-b", default="2,2", help="BASIS level (1,2 | 2,2 | 2,3 | 2,4)")
@click.option("--width", "-w", type=int, help="Output width in characters")
@click.option("--height", "-h", type=int, help="Output height in characters")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path")
def generate(
    input_file: Path,
    basis: str,
    width: Optional[int],
    height: Optional[int],
    output: Optional[Path],
) -> None:
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
            if getattr(img, "is_animated", False):
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
            output = input_file.with_suffix(".meow")

        # Write output
        with open(output, "w", encoding="utf-8") as f:
            f.write(result)

        click.echo(f"Generated '{output}' from '{input_file}'")
        click.echo(f"Display with: cat {output}")

    except Exception as e:
        click.echo(f"Error during generation: {e}", err=True)


@main.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.option("--basis", "-b", default="2,2", help="BASIS level (1,2 | 2,2 | 2,3 | 2,4)")
@click.option("--width", "-w", type=int, help="Output width in characters")
@click.option("--height", "-h", type=int, help="Output height in characters")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file path")
@click.option("--delay", "-d", type=int, help="Animation delay in ms")
def convert(
    input_file: Path,
    basis: str,
    width: Optional[int],
    height: Optional[int],
    output: Optional[Path],
    delay: Optional[int],
) -> None:
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
            if not getattr(img, "is_animated", False):
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
            output = input_file.with_suffix(".meow")

        # Write output
        with open(output, "w", encoding="utf-8") as f:
            f.write(result)

        click.echo(f"Converted '{input_file}' to '{output}'")
        click.echo(f"Display with: cat {output}")
        click.echo(f"Or play directly with: catpic {output}")

    except Exception as e:
        click.echo(f"Error during conversion: {e}", err=True)


@main.command()
@click.argument("meow_file", type=click.Path(exists=True, path_type=Path))
def info(meow_file: Path) -> None:
    """Display MEOW file information."""
    try:
        with open(meow_file, "r", encoding="utf-8") as f:
            content = f.read()

        decoder = CatpicDecoder()
        parsed = decoder.parse_meow(content)

        click.echo(f"File: {meow_file}")
        click.echo(f"Format: {parsed.get('format', 'Unknown')}")
        click.echo(f"Dimensions: {parsed.get('width', '?')}×{parsed.get('height', '?')}")
        click.echo(f"BASIS: {parsed.get('basis', '?')}")

        if parsed["format"].startswith("MEOW-ANIM/"):
            frame_count = parsed.get("frames_count", len(parsed.get("frames", [])))
            click.echo(f"Frames: {frame_count}")
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


if __name__ == "__main__":
    main()
