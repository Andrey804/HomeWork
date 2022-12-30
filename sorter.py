
import re, sys, shutil, os
from pathlib import Path


def is_full(rootdir):
    """Перевіряє кореневу папку на її порожність"""
    count = 0
    for i in rootdir.iterdir():
        count = 1
        break
    if not count:
        input("The folder is empty. Press 'Enter' key to quit")
        quit()


def new_folders():
    """Створює потрібні папки, якщо вони вже існують, то помилка не виникає"""
    for k in suffix.keys():
        try:
            os.mkdir(root_str_path + "\\" + k)
        except FileExistsError:
            continue


def listdirs(rootdir):
    """Основна функція, перебирає вказану папку"""
    for string_path in rootdir.iterdir():
        if string_path.is_dir():
            is_reserved = False
            for k in suffix.keys():
                if string_path.name == k:
                    is_reserved = True
            if is_reserved:
                continue
            listdirs(Path(string_path))
        else:
            move_and_rename(string_path)
    if rootdir != path:
        os.rmdir(rootdir)


def normalize(name):
    """Переводить назви на латинницю, та нормалізує їх"""
    name = Path(name)
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    CYRILLIC_CODES = []
    for char in CYRILLIC_SYMBOLS:
        CYRILLIC_CODES.append(ord(char))
    TRANS = dict(zip(CYRILLIC_CODES, TRANSLATION))
    TRANS.update({ord(chr(c).upper()): l.upper() for c, l in TRANS.items()})
    clean_name = re.sub(name.suffix, '', name.name)
    new_name = clean_name.translate(TRANS)
    return re.sub("[^a-zA-Z0-9]", "_", new_name)


def move_and_rename(string_path):
    """Спочатку переміщує файл, а потім змінює його ім'я вже у папці призначення"""
    string_path_obj = Path(string_path)
    flag = True
    for k, v in suffix.items():
        if v.find(string_path_obj.suffix) != -1:
            file_formats.add(string_path_obj.suffix[1:])
            new_location = root_str_path + "\\" + k
            shutil.move(str(string_path_obj), new_location)  # Перемещаем файл по ключу
            old = new_location + "\\" + string_path_obj.name
            new = new_location + "\\" + normalize(string_path_obj.name) + string_path_obj.suffix
            os.rename(old, new)
            if k == "archives":
                unpack_archive(new)
            flag = False
            break
    if flag:
        unknown_formats.add(string_path_obj.suffix[1:])
        new_location = root_str_path + "\\" + "other"
        shutil.move(str(string_path_obj), new_location)  # Перемещаем файл в папку other
        old = new_location + "\\" + string_path_obj.name
        new = new_location + "\\" + normalize(string_path_obj.name) + string_path_obj.suffix
        os.rename(old, new) 


def unpack_archive(archive_location_string_path):
    """Розпаковує архів та видаляє його"""
    obj_path = Path(archive_location_string_path)
    folder = re.sub(obj_path.suffix, '', archive_location_string_path)
    os.mkdir(folder)
    shutil.unpack_archive(archive_location_string_path, folder)
    os.remove(archive_location_string_path)


"""Словник використовуваних розширень"""
suffix = {
    "images": '.jpeg .png .jpg .svg',
    "video": '.avi .mp4 .mov .mkv',
    "documents": '.doc .docx .txt .pdf .xlsx .pptx',
    "audio": '.mp3 .ogg .wav .amr',
    "archives": '.zip .gz .tar',
    "other": ''
}


"""Основний код програми"""
if __name__ == "__main__":
    root_str_path = sys.argv[1]
    path = Path(root_str_path)
    file_formats = set()
    unknown_formats = set()
    is_full(path)
    new_folders()
    listdirs(path)
    if not file_formats:
        file_formats = None
    if not unknown_formats:
        unknown_formats = None
    print("Known formats:", file_formats)
    print("Unknown formats:", unknown_formats)
    input("Press 'Enter' key to quit")
    