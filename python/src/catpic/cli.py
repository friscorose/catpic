"""Command-line interface for catpic."""

from pathlib import Path
from typing import Optional

import click

from .core import BASIS, get_default_basis
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


@click.command()
@click.argument(
    "image_file", type=click.Path(exists=True, path_type=Path), required=True
)
@click.option("--basis", "-b", default=None, help="BASIS level (1,2 | 2,2 | 2,3 | 2,4). Defaults to CATPIC_BASIS env var or 2,2")
@click.option("--width", "-w", type=int, help="Output width in characters")
@click.option("--height", "-h", type=int, help="Output height in characters (for encoding)")
@click.option("--delay", "-d", type=int, help="Animation delay in ms (override)")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Save to .meow file instead of displaying")
@click.option("--force", "-f", is_flag=True, help="Force full-size animation (disable auto-truncation)")
@click.option("--info", "-i", is_flag=True, help="Show file information instead of displaying")
@click.version_option(version="0.5.0")
def main(
    image_file: Path,
    basis: Optional[str],
    width: Optional[int],
    height: Optional[int],
    delay: Optional[int],
    output: Optional[Path],
    force: bool,
    info: bool,
) -> None:
    """
    catpic - Display images in terminal using Unicode mosaics.

    Displays any image format directly in terminal, or saves to .meow format.

    Examples:
      catpic photo.jpg                     # Display image
      catpic animation.gif                 # Play animation
      catpic photo.jpg -o photo.meow       # Save to file
      catpic animation.gif > anim.meow     # Save via redirect
      catpic image.meow                    # Display saved file
      catpic image.meow --info             # Show file info
      
    Environment:
      CATPIC_BASIS - Default BASIS level (e.g., "2,4")
    """
    # Get BASIS (from flag, env var, or default)
    if basis is None:
        basis_enum = get_default_basis()
    else:
        try:
            basis_enum = parse_basis(basis)
        except click.BadParameter as e:
            click.echo(f"Error: {e}", err=True)
            raise SystemExit(1)

    # Handle info command
    if info:
        show_info(image_file)
        return

    # Check if it's already a MEOW file
    if image_file.suffix.lower() == ".meow":
        if output:
            click.echo("Error: Cannot re-encode .meow files", err=True)
            raise SystemExit(1)
        display_meow_file(image_file, delay, force)
        return

    # Encode image/animation
    try:
        from PIL import Image

        with Image.open(image_file) as img:
            is_animated = getattr(img, "is_animated", False)
    except Exception as e:
        click.echo(f"Error reading image: {e}", err=True)
        raise SystemExit(1)

    try:
        encoder = CatpicEncoder(basis=basis_enum)

        if is_animated:
            meow_content = encoder.encode_animation(image_file, width, height, delay)
        else:
            meow_content = encoder.encode_image(image_file, width, height)

        # Save or display
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(meow_content)
            click.echo(f"Saved to {output}")
        else:
            # Display directly
            if is_animated:
                player = CatpicPlayer()
                player.play(meow_content, delay=delay, force=force)
            else:
                decoder = CatpicDecoder()
                decoder.display(meow_content)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


def display_meow_file(meow_file: Path, delay: Optional[int], force: bool) -> None:
    """Display or play a .meow file."""
    try:
        with open(meow_file, "r", encoding="utf-8") as f:
            content = f.read()

        first_line = content.split("\n")[0].strip()
        if first_line.startswith("MEOW-ANIM/"):
            player = CatpicPlayer()
            player.play(content, delay=delay, force=force)
        else:
            decoder = CatpicDecoder()
            decoder.display(content)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


def show_info(file_path: Path) -> None:
    """Display file information."""
    try:
        # Check if it's a MEOW file
        if file_path.suffix.lower() != ".meow":
            # Show image file info
            from PIL import Image

            with Image.open(file_path) as img:
                click.echo(f"File: {file_path}")
                click.echo(f"Format: {img.format}")
                click.echo(f"Size: {img.width}×{img.height} pixels")
                click.echo(f"Mode: {img.mode}")
                if getattr(img, "is_animated", False):
                    click.echo(f"Animated: Yes ({getattr(img, 'n_frames', '?')} frames)")
                    if 'duration' in img.info:
                        click.echo(f"Frame delay: {img.info['duration']}ms")
        else:
            # Show MEOW file info
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            decoder = CatpicDecoder()
            parsed = decoder.parse_meow(content)

            click.echo(f"File: {file_path}")
            click.echo(f"Format: {parsed.get('format', 'Unknown')}")
            click.echo(f"Dimensions: {parsed.get('width', '?')}×{parsed.get('height', '?')} characters")
            click.echo(f"BASIS: {parsed.get('basis', '?')}")

            if parsed["format"].startswith("MEOW-ANIM/"):
                frame_count = parsed.get("frames_count", len(parsed.get("frames", [])))
                click.echo(f"Frames: {frame_count}")
                click.echo(f"Delay: {parsed.get('delay', '?')}ms")

            # File size
            file_size = file_path.stat().st_size
            if file_size < 1024:
                size_str = f"{file_size} bytes"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"

            click.echo(f"File size: {size_str}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
