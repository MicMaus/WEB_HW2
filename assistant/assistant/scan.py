import sys
from pathlib import Path

images_files = list()
video_files = list()
documents_files = list()
audio_files = list()
archives_files = list()
folders = list()
others = list()
unknown = list()
extensions = set()

registered_extensions = {
    "JPEG": images_files,
    "PNG": images_files,
    "JPG": images_files,
    "SVG": images_files,
    "AVI": video_files,
    "MP4": video_files,
    "MOV": video_files,
    "MKV": video_files,
    "DOC": documents_files,
    "DOCX": documents_files,
    "TXT": documents_files,
    "PDF": documents_files,
    "XLSX": documents_files,
    "PPTX": documents_files,
    "MP3": audio_files,
    "OGG": audio_files,
    "WAV": audio_files,
    "AMR": audio_files,
    "GZ": archives_files,
    "TAR": archives_files,
    "ZIP": archives_files,
    "": unknown,
}


def get_extensions(file_name):
    """
    Extracts the file extension from the given file name and converts it to uppercase.

    :param file_name: The name of the file.
    :return: The uppercase file extension.
    """
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    """
    This function iterates through the items within the specified folder. If an item is a directory,
    it recursively scans its subdirectories. If an item is a file, it uses the `get_extensions`
    function to extract its file extension. The file is then categorized into appropriate lists
    based on its extension, using the `registered_extensions` dictionary. The function also keeps
    track of different file extensions in the `extensions` set.

    :param folder:
    :return:
    """
    for item in folder.iterdir():
        if item.is_dir():
            # If the item is a directory and not one of the special folders, continue scanning
            if item.name not in (
                "Images",
                "Documents",
                "Audio",
                "Video",
                "Archives",
                "Others",
                "Unknown",
            ):
                folders.append(item)
                scan(item)
            continue

        # Get the file extension using the `get_extensions` function
        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name
        try:
            # Use the `registered_extensions` dictionary to categorize the file
            container = registered_extensions[extension]
            extensions.add(extension)
            container.append(new_name)
        except KeyError:
            # If the extension is not found in the dictionary, categorize it as 'Others'
            others.append(new_name)
            extensions.add(extension)


if __name__ == "__main__":
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

    print(f"Images: {images_files}\n")
    print(f"Video: {video_files}\n")
    print(f"Documents: {documents_files}\n")
    print(f"Audio: {audio_files}\n")
    print(f"Archive: {archives_files}\n")
    print(f"Folders: {folders}\n")
    print(f"Others: {others}\n")
    print(f"Unknown extensions: {unknown}\n")
    print(f"All extensions: {extensions}\n")
