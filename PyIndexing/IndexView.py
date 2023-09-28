import json
import os
import datetime
import hashlib
import string


def get_full_path(file_path: object) -> object:
    """
    获取绝对路径
    :param file_path:
    :return:
    """
    # Check if the path is already a full path
    if os.path.isabs(file_path):
        return file_path

    # Get the current working directory
    current_dir = os.getcwd()

    # Join the current directory with the file name to get the full path
    full_path = os.path.abspath(os.path.join(current_dir, file_path))

    return full_path


class IndexViewFolder:
    """
    遍历文件夹的根节点
    """

    def __init__(self, folder):
        self.path = os.path.abspath(folder)
        self.files = []
        self.folders = []
        self.recompute()

    def recompute(self):
        for entry in os.scandir(self.path):
            if entry.is_file():
                self.files.append(IndexViewFile(entry.path))
            elif entry.is_dir():
                fff = IndexViewFolder(entry.path)
                self.folders.append(fff)

    @property
    def recalculate_id(self):
        """
        Calculate storage id for this folder
        :return:
        """
        treeview = view_folder_to_string(self)
        json_string = json.dumps(treeview).encode(encoding='utf-8')
        return hashlib.sha256(json_string).hexdigest()

    def collect_files(self) -> {}:
        """
        收集所有文件
        :return:
        """
        files = self.files
        for folder in self.folders:
            files += folder.collect_files()
        return files

    def count_files(self):
        """
        计算文件夹的文件数
        :return:
        """
        length = len(self.files)
        for f in self.folders:
            length = length + f.count_files()
        return length


class IndexFileInfo:
    file_permissions: string
    owner: string
    last_accessed_by: string

    def __init__(self, filepath):
        file_path = get_full_path(filepath)
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        file_size = os.path.getsize(file_path)
        file_type = file_extension[1:] if file_extension else ""
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        access_time = datetime.datetime.fromtimestamp(os.path.getatime(file_path))

        try:
            modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
        except:
            # 如果获取修改时间失败则使用最早记录的时间
            modification_time = datetime.datetime.min

        self.name = os.path.basename(filepath)
        self.size = file_size
        self.file_type = file_type
        self.path = os.path.abspath(filepath)
        self.creation_date = creation_time
        self.modification_date = modification_time
        self.access_date = access_time
        self.file_permissions = ''
        self.owner = ''
        self.last_accessed_by = ''
        self.storage_id = file_to_storage_id(filepath)
        self.md5 = ''


class IndexViewFile:
    """
    遍历文件夹的文件节点
    """

    def __init__(self, file):
        self.file = file
        self.name = os.path.basename(file)
        self.storage_id = ''

    def recompute_id(self):
        self.storage_id = file_to_storage_id(self.file)

    def create_info(self):
        return IndexFileInfo(self.file)


def view_folder_to_string(folder_root):
    """
    计算根节点的文件变化记录
    :param folder_root:
    :return:
    """
    files = []
    for file in folder_root.files:
        files.append(file.storage_id)
    for folder in folder_root.folders:
        files.append(view_folder_to_string(folder))
    return files


def file_to_storage_id(file):
    """
    从文件计算文件的storage_id
    :param file:
    :return:
    """
    abs_path = os.path.abspath(file)
    file_size = os.path.getsize(abs_path)
    modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(abs_path))
    context = f"{abs_path}|{file_size}|{modification_time}"
    return hashlib.md5(context.encode()).hexdigest()
