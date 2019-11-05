# proto-erl-define
导出proto文件中的协议号宏定义及配置

```text
proto 文件格式 

syntax = "proto3";          .......... proto2 or proto3
package test;               .......... package名
// base 100                 .......... 协议号前缀, 协议号为uint16, 使用十进制, 前缀从100开始, 支持00-99号(即100 00 - 100 99)协议

// 测试协议1                 .......... 注释
// 10001                    .......... 协议号
message c2s_test1 {         .......... 协议体
    int32 int_v = 1;
    string string_v = 2;
    value value_v = 3;
}

// 结构体
message value {             .......... 内部无协议号结构体
    int32 int_v = 1;
}
```
