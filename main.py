from pathlib import Path
from time import sleep

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from wallpaper import get_current_wallpaper
from colours_class import Colours
from widget import update_widget


CONFIG_DIR = Path.home() / ".config"
CONFIG_FILE = "plasma-org.kde.plasma.desktop-appletsrc"


class WallpaperHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_wallpaper = None

    def update(self):
        path = get_current_wallpaper()

        if path == self.last_wallpaper:
            return

        wallpaper = Colours(path)
        wallpaper.extract_colours()

        cpu_accent, gpu_accent = wallpaper.get_accents()

        update_widget(cpu_accent, gpu_accent)

        self.last_wallpaper = path

    def on_modified(self, event):
        if Path(event.src_path).name == CONFIG_FILE:
            sleep(1)
            self.update()


handler = WallpaperHandler()

handler.update()

observer = Observer()
observer.schedule(handler, str(CONFIG_DIR), recursive=False)
observer.start()

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()