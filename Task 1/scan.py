import hashlib as h 
import os
from datetime import datetime
import json
import sys
import argparse

def get_info_file(filePath):
    size_file = os.path.getsize(filePath)
    date_last_mod = datetime.fromtimestamp(os.path.getmtime(filePath))
    return size_file, date_last_mod

def get_json_file(file, type_hash):
    size_f, modt = get_info_file(file)
    json_for_file = {"type": "file",
                     "size": size_f, 
                     "modt": str(modt)[:19]}
    if type_hash != None:
        json_for_file["hash"] = get_hash_file(file, type_hash)
    return json_for_file

def get_hash_file(filepath, type_hash):
    with open(filepath, "rb") as f:
        digest = h.file_digest(f, type_hash)
    return digest.hexdigest()  

def get_manual():
    return """Используйте: scan [path] [-h alghoritm]
              Вы можете использовать следующий набор алгоритмов хеширования: md5, sha256, sha512
              Для получения справки запустите эту программу без параметров: scan [press enter]
              Если необходимо получить структуру каталога без вычисления хеша используйте конструкцию: scan [path]."""

def get_dir_json(dir, type_hash):
    d = dict()
    if not os.listdir(dir):
        return {}
    for elem in os.listdir(dir):
        entry_path = os.path.join(dir, elem)
        if os.path.isdir(entry_path):
            d[elem] = {'type':'dir'}
            d[elem]['entries'] = get_dir_json(entry_path, type_hash)
        else:
            d[elem] = get_json_file(entry_path, type_hash)
    return d 
   
def main(filepath, type_hash=None):
    json_ = dict()
    json_["path"] = filepath
    if type_hash != None:
        json_["hash"] = type_hash
    json_["scan"] = dict()
    start = str(datetime.now())[:19]
    try:
        if os.path.isdir(filepath): 
            json_["scan"] = get_dir_json(filepath, type_hash)
        else:
            json_["scan"][os.path.basename(filepath)] = get_json_file(filepath, type_hash)
    except Exception as error:
        json_["scan"]["error"] = str(error)
    end = str(datetime.now())[:19]
    json_["startDate"] = start
    json_["finishDate"] = end
    return json_

    
def get_data():

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("path", help="Путь к файлу или каталогу", nargs="?", default=None, )
    parser.add_argument("-h", choices=["md5", "sha256", "sha512"], help="Указывает ключ типа использзуемого hash")
    s = parser.parse_args()
    try:
        if s.path == None:
            print(get_manual())
        if os.path.exists(s.path) and s.h != None:
            return main(s.path, s.h)
        if os.path.exists(s.path) and s.h == None:
            return main(s.path)
    except Exception as error:
        print(file=sys.stderr)

if __name__ == "__main__":
    res = get_data()
    if res:
        print(json.dumps(res, indent=4, ensure_ascii=False))





print("влад ребенек не мой, пущай грязный будет")