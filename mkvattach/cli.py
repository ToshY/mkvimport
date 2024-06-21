from pathlib import Path
import click
from mkvattach.banner import cli_banner
from mkvattach.args import (
    files_in_dir,
    InputPathChecker,
    OutputPathChecker,
    OptionalValueChecker,
)
from rich import print
from langcodes import standardize_tag

from mkvattach.helper import combine_arguments_by_batch, mimetype_by_extension
from mkvattach.process import ProcessDisplay
from loguru import logger  # noqa


def mkvmerge_remux_attachments(
    input_file: Path, output_path: Path, new_file_suffix: str = " (1)"
):
    """
    Remuxing file with specified fonts.

    Parameters
    ----------
    input_file : Path
        The specified input file as Path object.
    output_path : Path
        The specified output directory as Path object.
    new_file_suffix : str, optional
        Suffix used for filenaming. The default is ' (1)'.

    Returns
    -------
    None
        This function does not return anything.

    Raises
    ------
    Exception
        If the file does not have a corresponding directory, or if there is no `attachments` folder in the file
        attachments directory.

    Notes
    -----
    This function assumes that the input file has a corresponding directory with the same name, and that there is an
    `attachments` folder in that directory containing font files.
    """

    # Output argument
    output_file_name = input_file.stem + new_file_suffix + input_file.suffix

    # File attachments/subtitles directory
    file_attachments_dir = input_file.with_suffix("")
    if file_attachments_dir.as_posix().endswith("_stripped"):
        file_attachments_dir = Path(
            remove_suffix_from_string(file_attachments_dir.as_posix(), "_stripped")
        )
        output_file_name = (
            file_attachments_dir.stem + new_file_suffix + input_file.suffix
        )

    if not file_attachments_dir.exists():
        raise Exception(
            f"The file does not have a corresponding directory `{file_attachments_dir}`!"
        )

    file_attachments_font_dir = file_attachments_dir.joinpath("attachments")
    if not file_attachments_font_dir.exists():
        raise Exception(
            f"No `attachments` folder found in `{file_attachments_dir}`! Please put your fonts in an `attachments` "
            f"folder."
        )

    fonts = files_in_dir(file_attachments_font_dir, ["*.ttf", "*.otf", "*.eot"])
    mkv_fonts = mkvmerge_fonts(fonts)

    subtitles = files_in_dir(file_attachments_dir, ["*.ssa", "*.ass", "*.srt"])
    mkv_subtitles = mkvmerge_subtitles(subtitles)

    chapter = files_in_dir(file_attachments_dir, ["chapters.xml"])
    mkv_chapter = mkvmerge_chapter(chapter)

    # note: explicitly no tags are getting merged back

    if output_path.is_dir():
        output_file = output_path.joinpath(output_file_name).as_posix()
    else:
        output_file = output_path.with_suffix("").as_posix()

    mkvremux_attachments_command = (
        [
            "mkvmerge",
            "--output",
            output_file,
            "(",
            input_file.as_posix(),
            ")",
        ]
        + mkv_subtitles
        + mkv_fonts
        + mkv_chapter
    )

    process = ProcessDisplay(logger)
    process.run("MKVmerge remux", mkvremux_attachments_command)

    return mkvremux_attachments_command


def strip_file_attachments(input_file: Path) -> Path:
    """
    This function takes an input file as a Path object and strips attachments, subtitles, tags, and chapters from it.
    It creates a temporary file with the stripped content.

    Parameters:
        input_file (Path): The input file from which attachments, subtitles, tags, and chapters are stripped.

    Returns:
        Path: The path to the temporary file with the stripped content.

    Raises:
        Exception: If there is an error while stripping the attachments, subtitles, tags, and chapters, an exception is raised.
    """

    temporary_file = input_file.parent.joinpath(
        input_file.stem + "_stripped" + input_file.suffix
    )

    mkvmerge_temporary_file_command = [
        "mkvmerge",
        "--output",
        temporary_file.as_posix(),
        "--no-subtitles",
        "--no-attachments",
        "--no-chapters",
        "--no-track-tags",
        "--no-global-tags",
        "(",
        input_file.as_posix(),
        ")",
    ]

    process = ProcessDisplay(logger)
    process.run("MKVmerge strip", mkvmerge_temporary_file_command)

    return temporary_file


def mkvmerge_fonts(fonts_list: list) -> list[str]:
    """
    Generate a list of MKVmerge attachment commands for adding fonts to an MKV file.

    Parameters:
        fonts_list (list): A list of font objects.

    Returns:
        list[str]: A list of MKVmerge attachment commands for adding fonts.
    """

    mkv_fonts: list[str] = []
    for font in fonts_list:
        mkv_fonts = mkv_fonts + [
            "--attachment-name",
            font.name,
            "--attachment-mime-type",
            mimetype_by_extension(font.suffix),
            "--attach-file",
            font.as_posix(),
        ]

    return mkv_fonts


def mkvmerge_subtitles(subtitle_list: list) -> list[str]:
    """
    Generate a list of MKVmerge attachment commands for adding subtitles to an MKV file.

    Parameters:
        subtitle_list (list): A list of subtitle Path objects.

    Returns:
        list[str]: A list of MKVmerge attachment commands for adding subtitles.
    """

    mkv_subtitles: list[str] = []
    for subtitle in subtitle_list:
        mkv_subtitles = mkv_subtitles + [
            "--language",
            "0:" + standardize_tag(subtitle.with_suffix("").as_posix()[-3:]),
            "(",
            subtitle.as_posix(),
            ")",
        ]

    return mkv_subtitles


def mkvmerge_chapter(chapter_list: list) -> list[str]:
    """
    Generate a list of MKVmerge attachment commands for adding chapters to an MKV file.

    Parameters:
        chapter_list (list): A list of chapter Path objects.

    Returns:
        list[str]: A list of MKVmerge attachment commands for adding chapters.
    """

    mkv_chapter: list[str] = []
    for chapter in chapter_list:
        mkv_chapter = mkv_chapter + [
            "--chapters",
            chapter.as_posix(),
        ]

    return mkv_chapter


def remove_suffix_from_string(input_string: str, suffix: str) -> str:
    """
    Remove a suffix from a string.

    Args:
        input_string (str): The input string.
        suffix (str): The suffix to be removed.

    Returns:
        str: The string with the suffix removed.
    """

    if suffix and input_string.endswith(suffix):
        return input_string[: -len(suffix)]

    return input_string


@logger.catch
@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog="Repository: https://github.com/ToshY/mkvattach",
)
@click.option(
    "--input-path",
    "-i",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
    required=True,
    multiple=True,
    callback=InputPathChecker(),
    help="Path to input file or directory",
)
@click.option(
    "--output-path",
    "-o",
    type=click.Path(dir_okay=True, file_okay=True, resolve_path=True),
    required=True,
    multiple=True,
    callback=OutputPathChecker(),
    help="Path to output file or directory",
)
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["add", "replace"], case_sensitive=False),
    required=False,
    multiple=True,
    callback=OptionalValueChecker(),
    show_default=True,
    default=["replace"],
    help="Mode to add attachments to existing file ('add') or remove all existing attachments and add new attachments ("
    "'replace')",
)
def main(input_path, output_path, mode):
    combined_result = combine_arguments_by_batch(input_path, output_path, mode)

    for item in combined_result:
        current_mode = item.get("mode")
        current_output = item.get("output").get("resolved")
        current_input_files = item.get("input").get("resolved")

        for current_file_path_index, current_file_path in enumerate(
            current_input_files
        ):
            if current_mode == "replace":
                current_file_path = strip_file_attachments(current_file_path)

            mkvmerge_remux_attachments(current_file_path, current_output)

            if current_mode == "replace":
                current_file_path.unlink()


def cli():
    """
    A tool for embedding attachments (subtitles, fonts and chapters) to MKV files.

    Documentation: https://github.com/ToshY/mkvattach
    """

    cli_banner("mkvattach")

    # Stop execution at keyboard input
    try:
        main()
    except KeyboardInterrupt:
        print("\r\n\r\n> [red]Execution cancelled by user[/red]")
        exit()
