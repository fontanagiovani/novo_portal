import os
import shutil
from django.conf import settings


def del_recursive_folder_thumbnails(current):
        if current != settings.__getattr__('FILER_PUBLIC_THUMBNAIL') \
                and os.path.exists(current):
            dad_path, midia = os.path.split(current)
            shutil.rmtree(current)
            del_recursive_folder_thumbnails(dad_path)


def del_recursive_folder(current):
        if current != settings.__getattr__('FILER_PUBLIC') \
                and os.path.exists(current):
            dad_path, folder = os.path.split(os.path.join(current))
            shutil.rmtree(os.path.join(current))
            del_recursive_folder(dad_path)


def del_midia_filer(file_name):
    for root, dirs, files in os.walk(settings.__getattr__('FILER_PUBLIC'), topdown=False):
        for name in files:
            if name.startswith(file_name.lower()):
                dad_path, midia = os.path.split(os.path.join(root, name))
                os.remove(os.path.join(root, name))
                # del_recursive_folder(dad_path)

    for root, dirs, files in os.walk(settings.__getattr__('FILER_PUBLIC_THUMBNAIL'), topdown=False):
        for name in files:
            if name.startswith(file_name.lower()):
                dad_path, midia = os.path.split(os.path.join(root, name))
                os.remove(os.path.join(root, name))
                # del_recursive_folder_thumbnails(dad_path)