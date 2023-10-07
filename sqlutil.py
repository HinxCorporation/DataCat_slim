import json
import os
import string
import time
from PyIndexing.IndexFolder import IndexFolder
from PyIndexing.IndexView import IndexViewFolder
import hashlib
import sqlite3
from tqdm import tqdm


def datas_to_db_files(path, sinfo: IndexFolder):
    start_time = time.time()
    tw = IndexViewFolder(path)
    sid = tw.recalculate_id
    end_time = time.time()
    cost = end_time - start_time
    formatted_cost = "{:.3f} ms".format(cost * 1000)
    print(f'cost={formatted_cost} , folder id={sid} ,folder = {path} , files = {len(sinfo.files)}')

    # print(f"> {path} , files = {len(sinfo.files)} , folder = {len(sinfo.folders)}")
    # if len(sinfo.folders) > 0 :
    #    for suborder in sinfo.folders:
    #        print(f"\t> sub : {suborder.path}")


def folder_to_db_name(folder: string):
    md5 = hashlib.md5()
    md5.update(folder.encode('utf-8'))
    return f'{md5.hexdigest()}_{os.path.basename(folder)}.db'


def create_db_index_folder(folder: IndexFolder):
    full_path = folder.path
    create_db(full_path)


def create_db(full_path):
    db_name = folder_to_db_name(full_path)
    print(f'ready {db_name} , begin indexing .')
    ensure_db(db_name)
    tw = IndexViewFolder(full_path)
    files = tw.collect_files()
    print(f'index {db_name} finished {len(files)} files')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    batch_size = 1000
    batch_count = 0

    with tqdm(total=len(files), ncols=80, unit='file') as pbar:
        for file_res in files:
            file = file_res.create_info()
            insert_query = '''
                           INSERT INTO "files" (
                               file_name,
                               file_size,
                               file_type,
                               file_path,
                               creation_date,
                               modification_date,
                               access_date,
                               file_permissions,
                               owner,
                               last_accessed_by,
                               storage_id,
                               md5
                           )
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       '''

            # Replace the placeholders with the actual values from `file` object
            data = (
                file.name,
                file.size,
                file.file_type,
                file.path,
                str(file.creation_date),
                str(file.modification_date),
                str(file.access_date),
                file.file_permissions,
                file.owner,
                file.last_accessed_by,
                file.storage_id,
                file.md5
            )
            cursor.execute(insert_query, data)
            batch_count += 1
            pbar.update(1)

            if batch_count % batch_size == 0:
                conn.commit()

    conn.close()


def ensure_db(db_file):
    conn = sqlite3.connect(db_file)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS "files" (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            file_size NUMERIC,
            file_type TEXT,
            file_path TEXT,
            creation_date DATETIME,
            modification_date DATETIME,
            access_date DATETIME,
            file_permissions TEXT,
            owner TEXT,
            last_accessed_by TEXT,
            storage_id TEXT,
            md5 TEXT
        )
    ''')

    conn.close()
