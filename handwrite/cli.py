import os
import shutil
import argparse
import tempfile

from handwrite import SHEETtoPNG
from handwrite import PNGtoSVG
from handwrite import SVGtoTTF


def run(sheet, output_directory, characters_dir, config, metadata):
    SHEETtoPNG().convert(sheet, characters_dir, config)
    PNGtoSVG().convert(directory=characters_dir)
    SVGtoTTF().convert(characters_dir, output_directory, config, metadata)


# this is the fourth issue
# "4. Temp directory leaked on failure"
def converters(sheet, output_directory, directory=None, config=None, metadata=None):
    if config is None:
        config = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "default.json"
        )
    if os.path.isdir(config):
        raise IsADirectoryError("Config parameter should not be a directory.")

    if os.path.isdir(sheet):
        raise IsADirectoryError("Sheet parameter should not be a directory.")

    os.makedirs(output_directory, exist_ok=True)

    is_tempdir = not directory
    if is_tempdir:
        directory = tempfile.mkdtemp()

    try:
        # This line calls the run function to perform the conversion process.
        # It takes the input sheet, output directory, temporary or specified directory for intermediate files, configuration file, and metadata as arguments.
        run(sheet, output_directory, directory, config, metadata)
    finally:
        if is_tempdir:
            # This line ensures that the temporary directory is removed after the conversion process, even if an error occurs during the conversion.
            shutil.rmtree(directory)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Path to sample sheet")
    parser.add_argument("output_directory", help="Directory Path to save font output")
    parser.add_argument(
        "--directory",
        help="Generate additional files to this path (Temp by default)",
        default=None,
    )
    parser.add_argument("--config", help="Use custom configuration file", default=None)
    parser.add_argument("--filename", help="Font File name", default=None)
    parser.add_argument("--family", help="Font Family name", default=None)
    parser.add_argument("--style", help="Font Style name", default=None)

    args = parser.parse_args()
    metadata = {"filename": args.filename, "family": args.family, "style": args.style}
    converters(
        args.input_path, args.output_directory, args.directory, args.config, metadata
    )
