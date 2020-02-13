#!/usr/bin/env python2
# -*- coding: utf-8 -*-

' exprot erlang define module '

__author__ = 'Daniel'

import re
import sys
import os

proto_path = './proto/'
include_path = './include/'
include_file = 'hrl_proto.hrl'
data_path = './src/net/proto/'
data_file = 'data_proto.erl'
proto_range = 100
module_name_suffix = '_pb'

erl_text_prefix = '''%%%-------------------------------------------------------------------
%%% proto文件导出, 根据协议号和协议名分别获取对应信息
%%%-------------------------------------------------------------------
-module(data_proto).
-include("hrl_logs.hrl").

%% API
-export([get/1]).
-export([get_c2s/1]).
-export([get_s2c/1]).
'''
text_get_suffix = '''
get(_ID) ->
    ?WARNING("Cannot get ~p, ~p", [_ID, util:get_call_from()]),
    undefined.
'''
text_get_c2s_suffix = '''
get_c2s(_ID) ->
    ?WARNING("Cannot get_c2s ~p, ~p", [_ID, util:get_call_from()]),
    undefined.
'''
text_get_s2c_suffix = '''
get_s2c(_ID) ->
    ?WARNING("Cannot get_s2c ~p, ~p", [_ID, util:get_call_from()]),
    undefined.
'''


def _write_hrl(file_name):
    text = '\n%% ' + file_name + ' 协议号宏定义\n'
    file_name = proto_path + file_name
    rfile = open(file_name)
    dict_c2s = {}
    dict_s2c = {}
    while 1:
        line = rfile.readline()
        if not line:
            break
        line = re.sub('\\s', '', line)
        if line[0:6] == '//base':  # 基础协议信息
            base_value = re.sub('//base', '', line)
            ibase_value = int(base_value)
            continue
        if (line[0:2] == '//' and line[0:4] != '////'):   # 排除注释
            define_value = re.sub('//', '', line)
            try:
                idefine_value = int(define_value)
                if (idefine_value / proto_range != ibase_value):
                    print(u'导出失败!!!! 不在本文件的协议号范围内! 文件名:' +
                          file_name + u', 基础段号:' + base_value + u', 协议号:' + define_value)
                    sys.exit(0)
                next_line = rfile.readline()
                next_line = re.sub('\\s', '', next_line)
                next_line = re.sub('{', '', next_line)
                if not next_line:
                    print(u'导出失败!!!! 有未用到的协议号:' + define_value)
                    sys.exit(0)
                if next_line[0:7] == 'message':
                    if next_line[7:10] == 'c2s' or next_line[7:10] == 's2c':
                        # 判断协议号重复
                        if next_line[7:10] == 'c2s':
                            if dict_c2s.has_key(define_value):
                                print(u'导出失败!!!! c2s重复协议号:' + define_value)
                                sys.exit(0)
                            dict_c2s[define_value] = 1
                        else:
                            if dict_s2c.has_key(define_value) == 1:
                                print(u'导出失败!!!! s2c重复协议号:' + define_value)
                                sys.exit(0)
                            dict_s2c[define_value] = 1

                        define_name = next_line[7:]
                        line_text = '-define(' + define_name + \
                                    ', ' + define_value + ').\n'
                        # print line_text
                        text = text + line_text
                    else:
                        print(u'导出失败!!!! 协议号:' + define_value + u' 后跟的message: ' +
                              next_line[7:-1] + u' 名字错误! ')
                        sys.exit(0)
                else:
                    print(u'导出失败!!!! 协议号:' + define_value + u' 未跟着message!')
                    sys.exit(0)
            except ValueError:
                pass
    rfile.close()
    return text


def _write_erl(file_name):  # _write_proto_hrl 中各种判断, 此函数中可以不用再额外判断
    text_get = '\n%% ' + file_name + ' get\n'
    text_get_c2s = '\n%% ' + file_name + ' get_c2s\n'
    text_get_s2c = '\n%% ' + file_name + ' get_s2c\n'
    file_name = proto_path + file_name
    rfile = open(file_name)
    while 1:
        line = rfile.readline()
        if not line:
            break
        line = re.sub('\\s', '', line)
        if line[0:7] == 'package':  # 协议文件package
            package_name = re.sub('package', '', line)
            package_name = re.sub(';', '', package_name)
            package_name = package_name + module_name_suffix

        if (line[0:2] == '//' and line[0:4] != '////'):   # 排除注释
            define_value = re.sub('//', '', line)
            try:
                int(define_value)
                next_line = rfile.readline()
                next_line = re.sub('\\s', '', next_line)
                next_line = re.sub('{', '', next_line)
                define_name = next_line[7:]
                line_text_get = 'get(' + define_name + \
                                ') -> {' + define_value + ', ' + package_name + '};\n'
                text_get = text_get + line_text_get
                if next_line[7:10] == 'c2s':
                    line_text_get_c2s = 'get_c2s(' + define_value + \
                                        ') -> {' + define_name + ', ' + package_name + '};\n'
                    text_get_c2s = text_get_c2s + line_text_get_c2s
                elif next_line[7:10] == 's2c':
                    line_text_get_sc2 = 'get_s2c(' + define_value + \
                                        ') -> {' + define_name + ', ' + package_name + '};\n'
                    text_get_s2c = text_get_s2c + line_text_get_sc2
            except ValueError:
                pass
    rfile.close()
    return text_get, text_get_c2s, text_get_s2c


def _mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def _find_and_write():
    hrl_text = '%% proto协议中的协议名对应协议号宏定义\n'
    erl_text = erl_text_prefix
    erl_text_get = '\n'
    erl_text_get_c2s = '\n'
    erl_text_get_s2c = '\n'
    files = os.listdir(proto_path)
    for file in files:
        if os.path.splitext(file)[1] == '.proto':
            print(u'协议文件: ' + file)
            hrl_text += _write_hrl(file)
            text_get, text_get_c2s, text_get_s2c = _write_erl(file)
            erl_text_get += text_get
            erl_text_get_c2s += text_get_c2s
            erl_text_get_s2c += text_get_s2c

    wfile = open(include_path + include_file, 'w')
    wfile.write(hrl_text)
    wfile.close()

    wfile = open(data_path + data_file, 'w')
    erl_text_get += text_get_suffix
    erl_text_get_c2s += text_get_c2s_suffix
    erl_text_get_s2c += text_get_s2c_suffix
    wfile.write(erl_text + erl_text_get + erl_text_get_c2s + erl_text_get_s2c)
    wfile.close()

    print(u'导出成功!!!')


if __name__ == '__main__':
    _mkdir(include_path)
    _mkdir(data_path)
    _find_and_write()
