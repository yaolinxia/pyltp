#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
1. 首先进行预处理，过滤掉长度为2
"""
def filter_str2(file_path):
    # 定义一个列表，存放每个分词结果，结果放入列表中
    list = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = ''.join(line).strip()
            if len(line) > 2 and line not in list:
                list.append(line)
            # print(line)
    # print(list)
    return list

# 只保留大于三的
def filter_str3(file_path):
    # 定义一个列表，存放每个分词结果，结果放入列表中
    list = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = ''.join(line).strip()
            if len(line) > 3 and line not in list:
                list.append(line)
            # print(line)
    # print(list)
    return list


def write_file(file_path, content):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(content)
        f.write('\n')


if __name__ == '__main__':
    file_path = 'event.txt'
    output_path2 = 'out_2.txt'
    output_path3 = 'out_3.txt'
    str2_list = filter_str3(file_path)
    for s in str2_list:
        write_file(output_path3, s)


