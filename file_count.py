import os
from watchdog.events import FileSystemEventHandler

class FileCountHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory
        self.file_count = self.get_file_count()

    def get_file_count(self):
        # Count only files (not directories)
        return len(
            [
                f
                for f in os.listdir(self.directory)
                if os.path.isfile(os.path.join(self.directory, f))
            ]
        )

    def on_created(self, event):
        if not event.is_directory:
            self.file_count += 1

    def on_deleted(self, event):
        if not event.is_directory:
            self.file_count -= 1
