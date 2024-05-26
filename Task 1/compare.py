import json
import sys
import os

def compare_files(file1, file2):

    modified = []
    deleted = []
    created = []
    
    # Проверяем существование файлов
    if not os.path.exists(file1) or not os.path.exists(file2):
        print("Один из файлов не существует.", file=sys.stderr)
        sys.exit(1)
    
    # Загружаем результаты из файлов
    with open(file1, 'r', encoding="UTF-8") as f1, open(file2, 'r', encoding="UTF-8") as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
    
    def fun(dict_1, dict_2, p):
        path = p
        if dict_2.keys() - dict_1.keys():
            for key in dict_2.keys() - dict_1.keys():
                created.append(os.path.join(path, key))
                if dict_2[key]["type"] == "dir":
                    fun({}, dict_2[key]["entries"], os.path.join(path, key))
        for key1 in dict_1.keys():
            if key1 in dict_2.keys():
                if isinstance(dict_1[key1], dict):
                    if dict_1[key1]["type"] == "file":
                        if dict_1[key1]["modt"] != dict_2[key1]["modt"] and dict_1[key1]["hash"] != dict_2[key1]["hash"]:
                            modified.append(os.path.join(path, key1))
                    else:
                        fun(dict_1[key1]["entries"], dict_2[key1]["entries"], os.path.join(path, key1))
            else:
                deleted.append(os.path.join(path, key1))
                if dict_1[key1]["type"] == "dir":
                    serch_in_folder(dict_1[key1]["entries"], os.path.join(path, key1))
        return None
    
    def serch_in_folder(dict_, p):
        path = p
        for i in dict_.keys():
            deleted.append(os.path.join(path, i))
            if dict_[i]["type"] == "dir":
                serch_in_folder(dict_[i]["entries"], os.path.join(path, i))
                
    fun(data1["scan"], data2["scan"], os.path.normpath(data2["path"]))

    res_json = {
        "modified": modified,
        "created": created,
        "deleted": deleted
    }
    print(json.dumps(res_json, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: compare.py file1 file2", file=sys.stderr)
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    result = compare_files(file1, file2)
    json.dumps(result, indent=4)