# python module\Lesson6\HW6\sorter2.py D:\sorter
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


def main_function(some_path, known_formats, unknown_formats):
    """Створює потрібні папки. Якщо вони вже існують, то помилка не виникає.
        Викликає основну функцію. Повертає відоомі і невідомі формати"""
    for k in suffix.keys():
        try:
            os.mkdir(os.path.join(some_path, k))
        except FileExistsError:
            continue
    listdirs(some_path)
    if not known_formats:
        known_formats = None
    if not unknown_formats:
        unknown_formats = None
    return f"Known formats: {known_formats}; Unknown formats: {unknown_formats}"


def listdirs(rootdir):
    """Основна функція, перебирає вказану папку"""
    for list_path in rootdir.iterdir():
        if list_path.is_dir():
            is_reserved = False
            for k in suffix.keys():
                if list_path.name == k:
                    is_reserved = True
            if is_reserved:
                continue
            listdirs(Path(list_path))
        else:
            move_and_rename(list_path)
    if rootdir != path:
        os.rmdir(rootdir)


def normalize(name):
    """Нормалізує ім'я файлу"""
    name_obj = Path(name)
    cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    cyrillic_codes = []
    for char in cyrillic_symbols:
        cyrillic_codes.append(ord(char))
    trans = dict(zip(cyrillic_codes, translation))
    trans.update({ord(chr(c).upper()): l.upper() for c, l in trans.items()})
    clean_name = re.sub(name_obj.suffix, '', name_obj.name)
    new_name = clean_name.translate(trans)
    return re.sub("[^a-zA-Z0-9]", "_", new_name)


def move_and_rename(string_path):
    """Тепер спочатку переміщує файл, а потім змінює його ім'я вже у папці призначення"""
    string_path_obj = Path(string_path)
    flag = True
    for k, v in suffix.items():
        if v.find(string_path_obj.suffix) != -1:
            known_formats.add(string_path_obj.suffix[1:])
            new_location = os.path.join(root_str_path, k)
            shutil.move(str(string_path_obj), new_location)  # Перемещаем файл по ключу
            old = os.path.join(new_location, string_path_obj.name)
            new = os.path.join(new_location, normalize(string_path_obj.name) + string_path_obj.suffix)
            os.rename(old, new)
            if k == "archives":
                unpack_archive(new)
            flag = False
            break
    if flag:
        unknown_formats.add(string_path_obj.suffix[1:])
        new_location = os.path.join(root_str_path, "other")
        shutil.move(str(string_path_obj), new_location)  # Перемещаем файл в папку other
        old = os.path.join(new_location, string_path_obj.name)
        new = os.path.join(new_location, normalize(string_path_obj.name) + string_path_obj.suffix)
        os.rename(old, new) 


def unpack_archive(archive_location_string_path):
    """Розпаковує архів у папку з ідентичною назвою і видаляє його"""
    obj_path = Path(archive_location_string_path)
    folder = re.sub(obj_path.suffix, '', archive_location_string_path)
    os.mkdir(folder)
    shutil.unpack_archive(archive_location_string_path, folder)
    os.remove(archive_location_string_path)


known_formats = set()
unknown_formats = set()

suffix = {
    "images": '.jpeg .png .jpg .svg',
    "video": '.avi .mp4 .mov .mkv',
    "documents": '.doc .docx .txt .pdf .xlsx .pptx',
    "audio": '.mp3 .ogg .wav .amr',
    "archives": '.zip .gz .tar',
    "other": ''
}


if __name__ == "__main__":
    try:
        root_str_path = sys.argv[1]
    except IndexError:
        input("You did not specify a folder path. Press 'Enter' key to quit")
        quit()
    path = Path(root_str_path)
    is_full(path)
    print(main_function(path, known_formats, unknown_formats))
    input("Press 'Enter' key to quit")
