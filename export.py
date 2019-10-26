#!/usr/bin/env python2
# -*- coding: utf-8 -*-

' exprot erlang define module '

__author__ = 'Daniel'

import re
import sys
import os

proto_path = './proto/'
include_path = './include/'


def _write_proto_hrl(file_name):
    text = '\n%% ' + file_name + ' 协议号宏定义\n'
    file_name = proto_path + file_name
    rfile = open(file_name)
    print('协议文件: ' + file_name)
    while 1:
        line = rfile.readline()
        if not line:
            break
        line = re.sub('\\s', '', line)
        if line[0:2] == '//':
            define_value = line[2:8]
            try:
                int(define_value)
                next_line = rfile.readline()
                next_line = re.sub('\\s', '', next_line)
                next_line = re.sub('{', '', next_line)
                if not next_line:
                    print('有未用到的协议号:' + define_value)
                    sys.exit(0)
                if next_line[0:7] == 'message':
                    if next_line[7:10] == 'c2s' or next_line[7:10] == 's2c':
                        define_name = next_line[7:]
                        line_text = '-define(' + define_name + \
                            ', ' + define_value + ').\n'
                        # print line_text
                        text = text + line_text
                    else:
                        print('协议号:' + define_value + ' 后跟的message: ' +
                              next_line[7:-1] + ' 名字错误! ')
                        sys.exit(0)
                else:
                    print('协议号:' + define_value + ' 未跟着message!')
                    sys.exit(0)
            except ValueError:
                pass
    rfile.close()
    print text
    return text


def _mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def _find_and_write():
    text = '%% proto协议中的协议名对应协议号宏定义\n'
    files = os.listdir(proto_path)
    for file in files:
        if os.path.splitext(file)[1] == '.proto':
            text = text + _write_proto_hrl(file)
    wfile = open('./include/test.hrl', 'w')
    wfile.write(text)
    wfile.close()
    print('导出成功!!!')


if __name__ == '__main__':
    _mkdir(include_path)
    _find_and_write()
