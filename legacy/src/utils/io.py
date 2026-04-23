import zipfile
import os
from typing import Union, List
from pathlib import Path


def unzip_to_directory(zip_file: Path, extract_dir: Path, delete_zip_on_completion: bool = False) -> None:
    """
    Unzips a file to a specified directory
    """
    # Check paths 
    if not zip_file.is_file():
        raise FileNotFoundError(f"Couldn't find a file named: {zip_file}")
    if not zip_file.name.endswith(".zip"):
        raise IOError("File provided is not a .zip file")
    if not extract_dir.is_dir():
        raise NotADirectoryError(f"Could find directory: {extract_dir}")
    
    # Unzip
    print(f"Extracting {zip_file} to {extract_dir}")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        
    # Delete zip if specified
    if delete_zip_on_completion:
        delete_file(zip_file)
        
        
def delete_file(file_path: Path) -> None:
    """
    Simply deletes the given file
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"Couldn't find a file named: {file_path}")
    print(f"Deleting {file_path}")
    os.remove(file_path)
    

def list_files_under_path(base_dir: Path) -> List[Path]:
    """
    Gets all files under a given base directory. 
    """
    # Ensure the input is a Path object
    directory = Path(base_dir)
    
    if not directory.is_dir():
        raise NotADirectoryError(f"The provided path {base_dir} is not a valid directory.")
    
    # List all file paths using pathlib's rglob method
    file_paths = [file for file in directory.rglob("*") if file.is_file()]
    return file_paths
