# 这是一个示例 Python 脚本。
from PyIndexing.IndexUtil import IndexUtil
from tqdm import tqdm
import PyIndexing.IndexUtil as indexUtil
import DAO.DaoUtil
import yaml
import sqlutil


def test_connection():
    # 测试数据库链接
    connected = DAO.DaoUtil.test_db_connection()
    if connected:
        print("链接成功")
    else:
        print("连接失败, o(╯□╰)o , 去看看配置和权限是否正确 'config.ini")
    print('bye')


def main():
    """
    程序入口
    :return:
    """
    # 测试读取一个文件信息, 并且将其转成Yaml输出
    # testfile = 'config.ini'
    # info = indexUtil.read_file_info_from_file(testfile)
    # print(yaml.dump(info))

    # 读Path List
    configFile = "folder_paths.txt"
    with open(configFile, 'r', encoding='utf-8') as ffile:
        lines = ffile.readlines()
    util = IndexUtil()
    util.process_folders(lines)
    folder_infos = util.index_folders

    print(f'Success read assets {len(folder_infos)} , then will run gen db one time')
    # for dir in tqdm(folder_infos,unit='fs',desc='Travel folders'):
    for dir in folder_infos:
        s_dir = folder_infos[dir]
        sqlutil.create_db(s_dir)


if __name__ == "__main__":
    main()
