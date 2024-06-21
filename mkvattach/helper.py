from collections import defaultdict
from pathlib import Path


def files_in_dir(path: Path, file_types=["*.mkv"]):
    """
    Returns a list of files in the specified directory that match the given file types.

    Args:
        path (Path): The path to the directory.
        file_types (List[str], optional): A list of file types to match. Defaults to ["*.mkv"].

    Returns:
        List[Path]: A list of Path objects representing the files in the directory that match the given file types.
    """

    flist = [f for f_ in [path.rglob(e) for e in file_types] for f in f_]

    return flist


def mimetype_by_extension(file_extension: str) -> str:
    """
    Get appropriate mimetype; mimetype library cannot guess font mimes.

    Parameters
    ----------
    file_extension : str
        The specified font file.

    Returns
    -------
    str
        The mimetype for the corresponding file extension.

    """

    mimes = {
        "ttf": "application/x-truetype-font",
        "otf": "application/vnd.ms-opentype",
        "eot": "application/vnd.ms-fontobject",
    }

    return mimes[file_extension.lower().lstrip(".")]


def combine_arguments_by_batch(*lists):
    combined = defaultdict(dict)

    for lst in lists:
        for item in lst:
            batch = item["batch"]
            combined[batch].update(item)

    # Convert defaultdict back to a list of dictionaries
    result = [value for key, value in combined.items()]

    return result
