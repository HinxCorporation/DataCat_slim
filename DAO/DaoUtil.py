import configparser
from PyIndexing.FileInfo import FileInfo
from PyIndexing.IndexFolder import IndexFolder
import pymysql


def read_mysql_config():
    """
    读取配置中的sql数据
    :return:
    mysql配置
    """
    configfile = 'config.ini'
    config = configparser.ConfigParser()
    config.read(configfile)

    mysql_config = {
        'host': config.get('mysql', 'host'),
        'port': config.getint('mysql', 'port'),
        'database': config.get('mysql', 'database'),
        'user': config.get('mysql', 'user'),
        'password': config.get('mysql', 'password')
    }
    return mysql_config

def test_db_connection():
    """
    测试连接指定的数据库
    :return:
    连接成功返回True,否则false
    """
    try:
        conf = read_mysql_config()
        connection = pymysql.connect(
            host=conf['host'],
            port=conf['port'],
            user=conf['user'],
            password=conf['password'],
            database=conf['database']
        )
        connection.close()
        return True
    except pymysql.Error as e:
        return False


