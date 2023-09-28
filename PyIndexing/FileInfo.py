import os
import hashlib
import datetime


class FileInfo:
    def __init__(self, file_id=None, file_name="", file_size=0, file_type="", creation_time=None,
                 modification_time=None, access_time=None, file_path="", owner="", permissions="",
                 file_tags="", external_link="", notes=""):
        self.file_id = file_id
        self.file_name = file_name
        self.file_size = file_size
        self.file_type = file_type
        self.creation_time = creation_time
        self.modification_time = modification_time
        self.access_time = access_time
        self.file_path = file_path
        self.owner = owner
        self.permissions = permissions
        self.file_tags = file_tags
        self.external_link = external_link
        self.notes = notes


    @classmethod
    def from_file(cls, file_path):
        """
        从文件中获取文件信息并且返回文件信息对象
        :param file_path:文件的路径
        :return:
        文件信息对象, 可以从中获取各种信息
        """
        try:
            file_path = get_full_path(file_path)
            file_name, file_extension = os.path.splitext(os.path.basename(file_path))
            file_id = hashlib.md5(file_path.encode()).hexdigest()
            file_size = os.path.getsize(file_path)
            file_type = file_extension[1:] if file_extension else ""
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))

            try:
                modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            except Exception as e:
                # 如果获取修改时间失败则使用最早记录的时间
                modification_time = datetime.datetime.min

            file_info = cls(
                file_id=file_id,
                file_name=file_name,
                file_size=file_size,
                file_type=file_type,
                creation_time=creation_time,
                modification_time=modification_time,
                file_path=file_path
                # 其他属性赋值同上
            )

        except Exception as e:
            print(f"Error reading file: {e}")
            file_info = cls()

        return file_info


def get_full_path(file_path):
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
