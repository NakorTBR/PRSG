import os
from pathlib import Path
import shutil

__public_path = Path().cwd() / "public/"
__static_path = Path().cwd() / "static/"
__content_path = Path().cwd() / "content/"

def check_read_write_dirs() -> bool:
    """Checks the public and static directories to ensure they are present.
    Standard practice should be to immediately create the directories if they
    are not present and then run this check again.  If it fails after that, 
    we have a serious problem.

    Returns
    -------
    bool
        Returns true if both directories are present, and false if not.
    """
    # __public_path = Path.cwd() / "public/"
    # __static_path = Path.cwd() / "static/"

    pub_dir_exists = os.path.exists(__public_path)
    stat_dir_exists = os.path.exists(__static_path)

    if not pub_dir_exists:
        return False
    if not stat_dir_exists:
        return False
    
    return True


def __get_all_static_files() -> list:
    return list(__static_path.iterdir())

def clean_public_directory():
    if not os.path.exists(__public_path):
        return
    shutil.rmtree(__public_path)
    

def get_all_files_for_given_path(path):
    return list(path.iterdir())

def push_public(files=None, path=None):
    if not files:
        files = __get_all_static_files()

    if not os.path.exists(__public_path):
        os.mkdir(__public_path)

    if not path:
        path = __public_path
    
    for file in files:
        if os.path.isfile(file):
            # TODO: Copy files
            dest = path / file.name
            try:
                shutil.copy(file, dest)
                print("File copied successfully.")
            
            # If source and destination are same
            except shutil.SameFileError:
                print("Source and destination represents the same file.")
            
            # If there is any permission issue
            except PermissionError:
                print("Permission denied.")
            
            # For other errors
            except:
                print("Error occurred while copying file.")
        else:
            new_path = Path(file)
            new_folder = __public_path / file.stem
            if not os.path.exists(new_folder):
                print(f"Creating dir: {new_folder}")
                os.mkdir(new_folder)
            else:
                print("Folder already exists.")
            push_public(get_all_files_for_given_path(new_path), new_folder)

def get_file_contents(file_name: str) -> str:
    file_path = __content_path / file_name
    contents = ""

    try:
        contents = file_path.read_text()
    except FileNotFoundError:
        print("No such thing.")

    return contents