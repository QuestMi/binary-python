# -*- coding: utf-8 -*-
"""
Created Date: 2021-03-22 Am
@author: XiaoQingLin
@email: xiaoqinglin2018@gmail.com
"""

from os.path import dirname, join
from sys import version_info

import setuptools

if version_info < (3, 0, 0):
    raise SystemExit("binary_python requires must be python 3.0.0 or later.")

with open(join(dirname(__file__), "VERSION"), "rb") as f:
    version = f.read().decode("ascii").strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = setuptools.find_packages()

setuptools.setup(
    name="binary_python",
    version=version,
    author="XiaoQingLin",
    license="MIT",
    author_email="xiaoqinglin2018@gmail.com",
    description="binary_python encryption",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["Cython==0.29.20"],
    entry_points={"console_scripts": ["binary_python = binary_python.cmdline:execute"]},
    url="",
    packages=packages,
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)
