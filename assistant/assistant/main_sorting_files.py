import shutil
import sys
import time
from pathlib import Path

from colorama import Fore, Style
from tqdm import tqdm

import normalize
import scan


def handle_file(path, root_folder, dist):
    """
    Move and normalize a file to a specific directory.

    :param path: The path to the file.
    :param root_folder: The root folder where the target folder will be created.
    :param dist: The sub-folder where the file will be moved
    :return: None
    """
    # Creates the target folder if it doesn't exist
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    # Normalize the file name and combine this with origin extension
    new_path = target_folder / (normalize.normalize(path.name) + path.suffix)

    # Move the file to the new path
    path.replace(new_path)


def handle_archive(path, root_folder):
    """
    Handle the extraction and organization of an archive file.

    This function takes an archive file path and a root folder path as input. It creates a normalized sub-folder name
    using the base name of the archive file (without extension) and attempts to unpack the contents of the archive
    into the newly created sub-folder within the specified root folder. If the unpacking is successful, the original
    archive file is removed. If any errors occur during unpacking or folder creation, the function handles them
    gracefully by removing any newly created sub-folders and ignoring the error.

    :param path: The path to the file.
    :param root_folder: The root folder where the target folder will be created.
    :return: None
    """
    #
    new_name = normalize.normalize(path.with_suffix("").name)

    # Creates the archive folder if it doesn't exist
    archive_folder = root_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        # Unpack the archive into the sub-folder
        shutil.unpack_archive(str(path.resolve()), str(archive_folder))

        # Handle any potential errors during unpacking or folder operations
        # by removing the sub-folder and ignoring the error
    except shutil.ReadError:
        archive_folder.rmdir()
    except FileNotFoundError:
        archive_folder.rmdir()
    except OSError:
        pass

    # Remove the original archive file
    path.unlink()


def remove_empty_folders(path):
    """
    Recursively remove empty folders within a given path.

    This function traverses the specified path and its subdirectories to identify and remove empty folders. It first
    recursively calls itself to ensure that all subdirectories are processed before their parent directories. If an
    empty folder is encountered, it attempts to remove it using the 'rmdir' method. If the folder is not empty or if
    an error occurs during removal, the function continues to the next iteration.

    :param path: The root path to start the search for empty folders.
    :return: None
    """
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_object(root_path):
    """
    Recursively remove empty folders and specific folders within a given root path.

    This function traverses the specified root path to identify and remove specific folders that were created during
    the organization process but remain empty or no longer needed. It uses the 'remove_empty_folders' function to
    perform the removal of empty folders. If the folder is not empty or if an error occurs during removal, the
    function continues to the next iteration.

    :param root_path: The root path to start the search for empty folders.
    :return: None
    """
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass


def main(folder_path):
    scan.scan(folder_path)

    categories = [
        ("Images", scan.images_files),
        ("Documents", scan.documents_files),
        ("Audio", scan.audio_files),
        ("Video", scan.video_files),
        ("Others", scan.others),
        ("Unknown", scan.unknown),
    ]

    # Iterate through the categories and process their respective files
    for category_name, category_files in categories:
        if category_files:
            with tqdm(
                total=len(category_files), desc=f"Processing {category_name}"
            ) as pbar:
                for file in category_files:
                    file = Path(file)
                    handle_file(file, folder_path, category_name)
                    pbar.update(1)

    # Process the "Archives" category if it contains files
    if scan.archives_files:
        with tqdm(total=len(scan.archives_files), desc="Processing Archives") as pbar:
            for file in scan.archives_files:
                file = Path(file)
                handle_archive(file, folder_path)
                pbar.update(1)

    get_folder_object(folder_path)

    # Add a small delay to ensure the final message is displayed correctly
    time.sleep(0.1)

    print(Fore.BLUE + "Sorting folder successfully completed." + Style.RESET_ALL)


if __name__ == "__main__":
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    main(arg.resolve())
