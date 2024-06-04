import os
import gzip
import shutil
from demoparser2 import DemoParser
from scoreboardgenerator import ScoreboardGenerator

def check_file_exists(filepath: str) -> bool:
    return os.path.isfile(filepath)

def is_valid_file_type(filepath: str) -> bool:
    _, ext = os.path.splitext(filepath)
    return ext.lower() in {'.dem', '.gz'}

def get_file_type(filepath: str) -> str:
    _, ext = os.path.splitext(filepath)
    if ext.lower() == '.gz':
        # Check for double extensions like .dem.gz
        base, ext2 = os.path.splitext(_)
        if ext2.lower() == '.dem':
            return "gz"
    elif ext.lower() == '.dem':
        return "dem"
    return "invalid"

def extract_dem_from_gz(filepath: str):
    filename = os.path.basename(filepath)
    dem_filename = filename[:-3]
    current_directory = os.getcwd()
    dem_file_path = os.path.join(current_directory, dem_filename)
    with gzip.open(filepath, 'rb') as gz_file:
        with open(dem_file_path, 'wb') as dem_file:
            shutil.copyfileobj(gz_file, dem_file)
    return dem_file_path

def delete_file(filepath: str):
    if check_file_exists(filepath):
        os.remove(filepath)

def open_demo(filepath: str):
    parser = DemoParser(filepath)
    return parser

def export_to_csv(scoreboard: ScoreboardGenerator):
    try:
        scoreboard.ExportScoreboardToCSV()
    except PermissionError:
        return False
    return True

def clean_file_path(file_path: str) -> str:
    if file_path.startswith('"') and file_path.endswith('"'):
        return file_path[1:-1]
    return file_path
            