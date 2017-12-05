# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/flyshare
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from flyshare.util import log_info
import pymongo

def user_sign_in(name, password, clients=pymongo.MongoClient()):
    coll = clients.flyshares.user_list
    if (coll.find({'username': name, 'password': password}).count() > 0):
        log_info('success login! your username is:' + str(name))
        return True
    else:
        log_info('Failed to login,please check your password ')
        return False


def user_sign_up(name, password, clients=pymongo.MongoClient()):
    coll = clients.flyshares.user_list
    if (coll.find({'username': name}).count() > 0):
        log_info('user name is already exist')
        return False
    else:
        coll.insert({'username': name, 'password': password})
        log_info('Success sign in! please login ')
        return True
