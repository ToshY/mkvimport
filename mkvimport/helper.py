import collections
from pathlib import Path


def files_in_dir(path: Path, file_types=["*.mkv"]):
    """
    Returns a list of files in the given directory that match the specified file types.

    Parameters:
        path (Path): The path to the directory.
        file_types (List[str], optional): A list of file types to match. Defaults to ["*.mkv"].

    Returns:
        List[Path]: A list of paths to the files in the directory that match the specified file types.
    """

    file_list = [f for f_ in [path.rglob(e) for e in file_types] for f in f_]

    return file_list


def mimetype_by_extension(file_extension: str) -> str:
    """
    Returns the MIME type for the given file extension.

    Parameters:
        file_extension (str): The file extension to get the MIME type for.

    Returns:
        str: The MIME type for the given file extension.
    """

    mimes = {
        "ttf": "application/x-truetype-font",
        "otf": "application/vnd.ms-opentype",
        "eot": "application/vnd.ms-fontobject",
    }

    return mimes[file_extension.lower().lstrip(".")]


def combine_arguments_by_batch(*lists):
    """
    Combine arguments from multiple lists into batches based on the 'batch' key in each item.

    Parameters:
        *lists: Variable number of lists containing dictionaries with a 'batch' key.

    Returns:
        list: A list of dictionaries containing combined items grouped by their 'batch' key.
    """

    combined = collections.defaultdict(dict)

    for lst in lists:
        for item in lst:
            batch = item["batch"]
            combined[batch].update(item)

    result = [value for key, value in combined.items()]

    return result
