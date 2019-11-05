%%%-------------------------------------------------------------------
%%% proto文件导出, 根据协议号和协议名分别获取对应信息
%%%-------------------------------------------------------------------
-module(data_proto).
-include("hrl_logs.hrl").

%% API
-export([get/1]).
-export([get_c2s/1]).
-export([get_s2c/1]).


%% test.proto get
get(c2s_test1) -> {00001, test_pb};
get(c2s_test2) -> {00002, test_pb};
get(s2c_test1) -> {00001, test_pb};
get(s2c_test2) -> {00002, test_pb};

%% hello.proto get
get(c2s_hello) -> {01001, hello_pb};
get(s2c_hello) -> {01001, hello_pb};

get(_ID) ->
    ?WARNING("Cannot get ~p, ~p", [_ID, util:get_call_from()]),
    undefined.


%% test.proto get_c2s
get_c2s(00001) -> {c2s_test1, test_pb};
get_c2s(00002) -> {c2s_test2, test_pb};

%% hello.proto get_c2s
get_c2s(01001) -> {c2s_hello, hello_pb};

get_c2s(_ID) ->
    ?WARNING("Cannot get_c2s ~p, ~p", [_ID, util:get_call_from()]),
    undefined.


%% test.proto get_s2c
get_s2c(00001) -> {s2c_test1, test_pb};
get_s2c(00002) -> {s2c_test2, test_pb};

%% hello.proto get_s2c
get_s2c(01001) -> {s2c_hello, hello_pb};

get_s2c(_ID) ->
    ?WARNING("Cannot get_s2c ~p, ~p", [_ID, util:get_call_from()]),
    undefined.
