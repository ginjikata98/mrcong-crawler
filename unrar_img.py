import os
import re
import shutil
import threading
import time

import rarfile
from PIL import Image

XPATH = 'C:\\project\\mrcong\\out'
DPATH = 'C:\\project\\mrcong\\src'
PASSWORD = 'mrcong.com'

rarfile.UNRAR_TOOL = 'C:\\Program Files (x86)\\WinRAR\\WinRar'

start_time = time.time()


def setup():
    if os.path.exists(XPATH):
        shutil.rmtree(XPATH)
    os.makedirs(XPATH)


def unrar(rar_file):
    filepath = os.path.join(DPATH, rar_file)
    opened_rar = rarfile.RarFile(filepath)
    for f in opened_rar.infolist():
        print(f.filename, f.file_size)
    opened_rar.extractall(XPATH, pwd=PASSWORD)


def rename(folder_path):
    for root1, dirs1, files1 in os.walk(folder_path):
        for img in files1:
            filepath = os.path.join(root1, img)
            new_path = os.path.join(XPATH, img)

            image = Image.open(filepath)
            new_name = re.sub(r'MrCong', 'dopaminegirls', new_path)
            image.save(new_name)


def clean():
    for root1, dirs1, files1 in os.walk(XPATH):
        for folder in dirs1:
            shutil.rmtree(os.path.join(XPATH, folder))


def join_thread(threads):
    for thread in threads:
        thread.join()


setup()

unrar_threads = []
for rar in os.listdir(DPATH):
    unrar_thread = threading.Thread(target=unrar, args=[rar])
    unrar_threads.append(unrar_thread)
    unrar_thread.start()

join_thread(unrar_threads)

rename_threads = []
dirs = os.listdir(XPATH)
for directory in dirs:
    rename_thread = threading.Thread(target=rename, args=[os.path.join(XPATH, directory)])
    rename_threads.append(rename_thread)
    rename_thread.start()
join_thread(rename_threads)

clean()
print("--- %s seconds ---" % (time.time() - start_time))
