# -*- coding: utf-8 -*-

import glob
import itertools
import os
import random
import re
import shutil
import string
import sys
from urllib.parse import urlparse

from git import Repo


class Filters:
    """
    Basic parent class for get registered in filters functions by a dict key
    """

    def __init__(self):
        self.filters = {}

    def filter_add(self, name: str, value: any):
        """
        Add function to self.filters dict
        :param name:
        :param value:
        :return:
        """
        self.filters[name] = value

    def filter_by(self, key: str, *args, **kwargs):
        """
        Gef function by key from self.filters dict
        :param key: function key
        :param args: *args for returned function
        :param kwargs: **kwargs for returned function
        :return:
        """
        filter_ = self.filters.get(key)
        if not filter_:
            raise ValueError(key)
        return filter_(*args, **kwargs)


def git_clone(git_url: str, working_path: str) -> str:
    repo = Repo.clone_from(url_check(git_url), path_format(working_path))
    return path_format(repo.working_dir)


def url_check(url: str) -> any:
    try:
        check = urlparse(url)
        return url if check else False
    except ValueError:
        return sys.exit('ValueError :: Enter correct url on restart')


def files_paths_get(path: str, files_extensions: list, files_number_limit: int, ) -> list:
    return list(itertools.islice(
        (p for ext in files_extensions for p in glob.glob('{}**/*{}'.format(path, ext), recursive=True) if
         os.path.isfile(p)), files_number_limit))


def path_format(path: str) -> str:
    return path if path.endswith('/') else '{}/'.format(path)


def directory_check_exist_and_permissions(path: str):
    return all([os.access(path, os.F_OK), os.access(path, os.R_OK), os.access(path, os.W_OK), os.path.isdir(path)])


def directory_temp_create(path: str, suffix: str = ''):
    path_temp = '{}{}/'.format(path_format(path),
                               re.sub('[^a-zA-Z_0-9\s+]', '', suffix) if len(suffix) > 0 else random_string())
    if directory_check_exist_and_permissions(path) and not os.path.exists(path_temp):
        os.makedirs(path_temp)
    else:
        if not directory_cleanup(path_temp):
            return False
    return path_temp


def directory_is_not_empty(path):
    return True if directory_check_exist_and_permissions(path) and len(os.listdir(path)) > 0 else False


def directory_cleanup(path):
    if directory_is_not_empty(path):
        shutil.rmtree(path)
        os.makedirs(path)
        return True
    else:
        return False


def extensions_format(s: str) -> list:
    return ['.%s' % ext for ext in re.sub('[^a-zA-Z_0-9\s+]', '', s).split(' ') if len(ext) > 0] if len(s) > 0 else ['']


def list_values_to_str(list_: list) -> list:
    return list(map(str, list_))


def flat_list(l: list) -> list:
    return [item for sublist in list(l) for item in sublist]


def str_split_camelcase(s: str) -> list:
    return re.sub('(?!^)([A-Z][a-z]+)', r' \1', s).split()


def str_split_snakecase(s: str) -> list:
    return [w for w in s.split('_') if len(w) > 0]


def random_string(symbols_count: int = 16):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(symbols_count))
