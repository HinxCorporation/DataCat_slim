import os


class IndexFolder:
    """
    遍历的文件夹
    """
    def __init__(self, path):
        self.path = path
        self.files = []
        self.folders = []

    def index_folder(self):
        for entry in os.scandir(self.path):
            if entry.is_file():
                self.files.append(entry.name)
            elif entry.is_dir():
                subFolder = IndexFolder(entry.path)
                subFolder.index_folder()
                self.folders.append(subFolder)
