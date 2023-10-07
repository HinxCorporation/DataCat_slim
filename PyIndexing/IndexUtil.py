import os
import logging
import string
from PyIndexing.FileInfo import FileInfo
from PyIndexing.IndexFolder import IndexFolder


def get_abs_folder(folder_path):
    """
    获取指定路径的绝对位置
    :param folder_path:
    :return:
    """
    # 处理相对路径、绝对路径和环境变量
    folder_path = folder_path.strip()
    processed_path = os.path.expandvars(os.path.expanduser(folder_path))

    if not os.path.isabs(processed_path):
        processed_path = os.path.abspath(processed_path)
    try:
        # 检测路径是否可读
        if os.path.isdir(processed_path) and os.access(processed_path, os.R_OK):
            return True, processed_path
        else:
            return False, processed_path
    except Exception as e:
        return False, e.args


class IndexUtil:
    def __init__(self):
        self.errors: string = []
        self.index_folders = {}

    def process_folders(self, folder_list):
        """
        处理文件夹列表,扫描每个指定的文件夹
        :param folder_list:
        :return:
        """
        for folder_path in folder_list:
            self.process_folder(folder_path)

    def process_folder(self, folder_path):
        """
        处理单个文件夹
        :param folder_path:
        :return:
        """
        # 处理相对路径、绝对路径和环境变量
        folder_path = folder_path.strip()
        processed_path = os.path.expandvars(os.path.expanduser(folder_path))

        if not os.path.isabs(processed_path):
            processed_path = os.path.abspath(processed_path)
        try:
            # 检测路径是否可读
            if os.path.isdir(processed_path) and os.access(processed_path, os.R_OK):
                index_folder = IndexFolder(processed_path)
                index_folder.index_folder()
                # self.index_folders.append(index_folder)
                self.index_folders[processed_path] = index_folder
            else:
                error_msg = f" 不可读或者不存在: {folder_path} ({processed_path})"
                self.errors.append(error_msg)
                logging.error(error_msg)
        except Exception as e:
            error_msg = f"Error in path: {folder_path}\nerror={str(e)}"
            self.errors.append(error_msg)
            logging.exception(error_msg)


def read_file_info_from_file(filename):
    """
    從已有的文件中生成文件信息對象
    :param filename:
    :return:
    """
    return FileInfo.from_file(filename)
