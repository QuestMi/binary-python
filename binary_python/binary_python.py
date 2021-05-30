# -*- coding: utf-8 -*-
"""
Created Date: 2021-03-22 Am
binary python:
    1、windows -> pyd;
    2、linux -> so .
@author: XiaoQingLin
"""
import os
import re
import shutil
import tempfile
from distutils.command.build_py import build_py
from distutils.core import setup
from typing import Union, List

from Cython.Build import cythonize

from binary_python.log import logger


def get_package_dir(*args, **kwargs):
    return ""


# 重写get_package_dir， 否则生成的so文件路径有问题
build_py.get_package_dir = get_package_dir


class TemporaryDirectory(object):
    def __enter__(self):
        self.name = tempfile.mkdtemp()
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.name)


def search(content, regexs):
    if isinstance(regexs, str):
        return re.search(regexs, content)

    for regex in regexs:
        if re.search(regex, content):
            return True


def walk_file(file_path):
    if os.path.isdir(file_path):
        for current_path, sub_folders, files_name in os.walk(file_path):
            for file in files_name:
                file_path = os.path.join(current_path, file)
                yield file_path

    else:
        yield file_path


def copy_files(src_path, dst_path):
    if os.path.isdir(src_path):
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)

        def call_able(src, names: list):
            if search(src, dst_path):
                return names
            return ["binary", ".git", "venv", ".idea", "__pycache__"]

        shutil.copytree(src_path, dst_path, ignore=call_able)
    else:
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        shutil.copyfile(src_path, os.path.join(dst_path, os.path.basename(src_path)))


def get_py_files(files, ignore_files: Union[List, str, None] = None):
    """
    @param files: 文件列表
    # param ignore_files: 忽略文件，支持正则
    @result:
    """
    for file in files:
        if file.endswith(".py"):
            if ignore_files and search(file, regexs=ignore_files):  # 该文件是忽略的文件
                pass
            else:
                yield file


def filter_not_binary_encrypt_file(files, except_main_file):
    """
    过滤掉不需加密的文件，如 log.py __main__.py 以及包含 if __name__ == "__main__": 的文件
    Args:
        files:

    Returns:

    """
    _files = []
    for file in files:
        if search(file, regexs="__.*?.py"):
            continue

        if except_main_file:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                if search(content, regexs="__main__"):
                    continue

        _files.append(file)

    return _files


def encrypt_py(py_files: list):
    encrypted_py = []

    with TemporaryDirectory() as td:
        total_count = len(py_files)
        for i, py_file in enumerate(py_files):
            try:
                dir_name = os.path.dirname(py_file)
                file_name = os.path.basename(py_file)
                os.chdir(dir_name)
                logger.info(f"ENCRYPTING {i + 1}/{total_count},  {file_name}")
                setup(
                    ext_modules=cythonize([file_name], quiet=True, language_level=3),
                    script_args=["build_ext", "-t", td, "--inplace"])
                encrypted_py.append(py_file)
                logger.info(f"ENCRYPT SUCCESS {file_name}")
            except Exception as e:
                logger.exception("ENCRYPT FAILED {} , ERROR {}".format(py_file, e))
                temp_c = py_file.replace(".py", ".c")
                if os.path.exists(temp_c):
                    os.remove(temp_c)
        return encrypted_py


def delete_files(files_path):
    """
    删除python、c文件
    @param files_path: 文件路径 py 及 c 文件
    @result:
    """
    try:
        for file in files_path:
            os.remove(file)
            os.remove(file.replace(".py", ".c"))
    except Exception as e:
        pass


def rename_excrypted_file(output_file_path):
    for file in walk_file(output_file_path):
        if file.endswith(".pyd") or file.endswith(".so"):
            new_filename = re.sub("(.*)\..*\.(.*)", r"\1.\2", file)
            os.rename(file, new_filename)


def start_binary_encrypt(
        input_file_path,
        output_file_path: str = None,
        ignore_files: Union[List, str, None] = None,
        except_main_file: int = 1,
):
    assert input_file_path, "input_file_path can't be null"

    assert (input_file_path != output_file_path), "output_file_path must be different with input_file_path"

    if output_file_path and os.path.isfile(output_file_path):
        raise ValueError("output_file_path need a dir path")

    input_file_path = os.path.abspath(input_file_path)
    if not output_file_path:  # 无输出路径
        if os.path.isdir(input_file_path):  # 如果输入路径是文件夹 则输出路径为input_file_path/binary/project_name
            output_file_path = os.path.join(
                input_file_path, "binary", os.path.basename(input_file_path))
        else:
            output_file_path = os.path.join(os.path.dirname(input_file_path), "binary")
    else:
        output_file_path = os.path.abspath(output_file_path)

    copy_files(input_file_path, output_file_path)
    files = walk_file(output_file_path)
    py_files = get_py_files(files, ignore_files)
    need_encrypted_py = filter_not_binary_encrypt_file(py_files, except_main_file)
    encrypted_py = encrypt_py(need_encrypted_py)
    delete_files(encrypted_py)
    rename_excrypted_file(output_file_path)

    logger.debug(
        f"ENCRYPT END TOTAL_COUNT={len(need_encrypted_py)}, "
        f"SUCCESS_COUNT={len(encrypted_py)}, "
        f"ENCRYPT FILE PATH: {output_file_path}")
