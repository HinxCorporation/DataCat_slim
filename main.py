from tqdm import tqdm
import DAO.DaoUtil
import PyIndexing.IndexUtil as indexUtil
import sqlutil


def test_connection():
    # 测试数据库链接
    connected = DAO.DaoUtil.test_db_connection()
    if connected:
        print("链接成功")
    else:
        print("连接失败, o(╯□╰)o , 去看看配置和权限是否正确 'config.ini")
    print('bye')


def collect_folders():
    configFile = "folder_paths.txt"
    with open(configFile, 'r', encoding='utf-8') as ffile:
        lines = ffile.readlines()
    folders = []
    for line in tqdm(iterable=lines, unit='dir', desc='trip'):
        su, j_dir = indexUtil.get_abs_folder(line)
        if su:
            folders.append(j_dir)
    return folders


def main():
    """
    程序入口
    :return:
    """

    # 读Path List
    folders = collect_folders()
    for folder in folders:
        sqlutil.create_db(folder)


if __name__ == "__main__":
    main()
