#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.1.0'

from .apkinfo import ApkInfo


def getApkInfo(apkPath):
    return ApkInfo(apkPath)
