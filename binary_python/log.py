# -*- coding: utf-8 -*-
"""
Created Date: 2021-03-22 Am
@author: XiaoQingLin
"""
import logging
import sys

# set up logging
logger = logging.getLogger("binary-encrypt")

format_string = (
    "%(asctime)s|%(filename)s|%(funcName)s|line:%(lineno)d|%(levelname)s| %(message)s"
)
formatter = logging.Formatter(format_string, datefmt="%Y-%m-%dT%H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.stream = sys.stdout

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
