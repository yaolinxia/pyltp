#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import gc
import re
from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger

"""
完成时间：2018.12.20
1. 把所有的name所在的句子提取出来
2. 对提取的name字段进行分词
3. 对于分词的结果进行统计
"""
cws_model = "F:\pycharm\yao\ltp_data_v3.4.0\cws.model"
parser_model = "F:\pycharm\yao\ltp_data_v3.4.0\parser.model"
pos_model = "F:\pycharm\yao\ltp_data_v3.4.0\pos.model"
def load_json(path):
    with open(path, 'r') as f:
        # 加载json
        load_dict = json.load(f)
    print(load_dict)
    return load_dict

# 读取文件，把每一个name值存放进列表中
def name_to_list(path):
    # 定义一个列表，存放每一句name字段的value值
    name_list = []
    with open(path, 'r', encoding='utf-8') as f:
        # 每个line都是一个字典，提取其中的name值
        for line in f:
            # 转换成字典类型
            line = eval(line)
            name_list.append(line["name"])
    return name_list

# 分句子（没有使用到）
def sen_spliter(sen):
    single_sen = SentenceSplitter.split(sen)
    print('\n'.join(single_sen))

# 分词
def sen_word(sen):
    # 初始化实例
    segmentor = Segmentor()
    # 加载LTP模型
    segmentor.load(cws_model)
    # 分词
    words = segmentor.segment(sen)
    # print('\t'.join(words))
    # 转化成list输出
    words_list = list(words)
    # 释放模型
    segmentor.release()
    return words_list

# 词性标注. words:已经切分好的词
def word_tag(words):
    words_list = []
    # 初始化实例
    postagger = Postagger()
    # 加载模型
    postagger.load(pos_model)
    # 进行词性标注
    postags = postagger.postag(words)
    pos = set(['n', 'nd', 'nh', 'ni', 'nl', 'ns', 'nt', 'nz'])
    for i in range(0, len(words)):
        # print(words[i], postags[i])
        if postags[i] in pos:
            words_list.append(words[i])
            # print(words[i], postags[i])
    postagger.release()
    # print(words_list)
    return words_list

# 保存到json文件中
def to_json(dict, save_path):
    with open(save_path, 'a') as json_file:
        json.dump(dict, json_file, ensure_ascii=False, indent=2)
        json_file.write('\n')

if __name__ == '__main__':
<<<<<<< Updated upstream
    # 原始文件
    txt_path = 'H:\python-workspace\pyltp\split_name\\action_code_data_0.txt'
    # 定义json的输出路径
=======
    json_path = 'action_code_data_0.json'
    txt_path = 'action_code_data_0.txt'
>>>>>>> Stashed changes
    json_out_path = 'namesplit_only_noun.json'
    name_list = name_to_list(txt_path)
    for name_value in name_list:
        name_dict = {}
        name_dict["name"] = name_value
        sen_list = sen_word(name_value)
        words_list = word_tag(sen_list)
        name_dict["word_list"] = words_list
        # print(name_dict)
        to_json(name_dict, json_out_path)
        gc.collect()




        # print(name_dict)
    #     # 把里面每个元素都统一放到一个字典中
    #     for i in sen_list:
    #         if i in name_dict:
    #             name_dict[i] += 1
    #         else:
    #             name_dict[i] = 1
    # print(name_dict)
    # print(len(name_dict))
    # to_json(name_dict, json_out_path)
    # sen_spliter(txt_path)