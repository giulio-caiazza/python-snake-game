from os import getenv, path, makedirs
from platform import system as pl_system
from Game import Game

def get_appdata_path():
    system = pl_system()
    if system == "Windows":
        return getenv('APPDATA')
    elif system == "Darwin":  # macOS
        # ~/Library/Application Support/SnakeGame
        return path.join(path.expanduser("~"), "Library", "Application Support")
    else:  # Linux or fallback
        return path.join(path.expanduser("~"), ".local", "share")

def make_right_zone(path_dir, path_score_record):
    makedirs(path_dir, exist_ok=True)

    if not path.exists(path_score_record) or path.getsize(path_score_record) == 0:
        with open(path_score_record, 'w') as f:
                f.write("27")

if __name__ == "__main__":
    appdata_path = get_appdata_path()
    path_dir = path.join(appdata_path, "SnakeGame")
    path_score_record = path.join(path_dir, "score_record.txt")

    make_right_zone(path_dir, path_score_record)

    import cProfile
    cProfile.run("Game(path_score_record).run()")