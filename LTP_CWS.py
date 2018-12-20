#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import codecs
import gc

model_path = "E:\YanJiuSheng-download\\2a\ltp_data_v3.4.0\ltp_data_v3.4.0"
cws_model = "E:\YanJiuSheng-download\\2a\ltp_data_v3.4.0\ltp_data_v3.4.0\cws.model"
pos_model = "E:\YanJiuSheng-download\\2a\ltp_data_v3.4.0\ltp_data_v3.4.0\pos.model"
ner_model = "E:\YanJiuSheng-download\\2a\ltp_data_v3.4.0\ltp_data_v3.4.0\\ner.model"
parser_model = "E:\YanJiuSheng-download\\2a\ltp_data_v3.4.0\ltp_data_v3.4.0\\parser.model"
from pyltp import Segmentor
from pyltp import SentenceSplitter
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser

print("+==============")
# 初始化实例
# segmentor = Segmentor()
# # 加载LTP模型
# segmentor.load(cws_model)
# # 分句子
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
    # for word in words_list:
        # print(word)
    # 释放模型
    segmentor.release()
    return words_list

# 词性标注. words:已经切分好的词
def word_tag(words):
    # 定义词典count: key：str, value相应str统计出的个数
    count = {}
    # 初始化词典
    for word in words:
        count[word] = 0

    # 初始化实例
    postagger = Postagger()
    # 加载模型
    postagger.load(pos_model)
    # 进行词性标注
    postags = postagger.postag(words)
    for i in range(0, len(words)-1):
        # print(words[i], postags[i])

        if postags[i] == 'n' or postags[i] == 'v':
            count[words[i]] += 1
        # 名词+名词
        if postags[i] == 'n' and postags[i+1] == 'n':
            write_file('event.txt', words[i] + words[i+1])
            # print(words[i] + words[i+1])
        # 动词+名词
        if postags[i] == 'v' and postags[i+1] == 'n':
            write_file('event.txt', words[i] + words[i + 1])
            # print(words[i] + words[i+1])
        # 副词+名词
        if postags[i] == 'd' and postags[i+1] == 'v':
            write_file('event.txt', words[i] + words[i + 1])
            # print(words[i] + words[i+1])
        # 其他名词修饰+动词
        if postags[i] == 'b' and postags[i+1] == 'v':
            write_file('event.txt', words[i] + words[i + 1])
            # print(words[i] + words[i + 1])
        # else:
        #     count[words[i]] = 1

    # for word, tag in zip(words, postags):
    #     print(word+'/'+tag)
    # 释放模型
    print(count)
    postagger.release()
    return postags

# 命名实体识别,words:分词结果；postags:标注
def name_recognition(words, postags):
    # 初始化实例
    recognizer = NamedEntityRecognizer()
    # 加载模型
    recognizer.load(ner_model)
    netags = recognizer.recognize(words, postags)
    for word, ntag in zip(words, netags):
        print(word+'/'+ntag)
    # 释放模型
    recognizer.release()
    return netags

# 依存句法分析
def parse(words, postags):
    # 初始化实例
    parser = Parser()
    # 加载模型
    parser.load(parser_model)
    # 句法分析
    arcs = parser.parse(words, postags)
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    # 释放模型
    parser.release()

# 读文件
def read_file(file_path):
    sen_list = []
    with open(file_path, 'r', encoding='utf') as f:
        for each_line in f:
            sen_list.append(each_line)
    return sen_list

# 写文件
def write_file(file_path,text):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')

if __name__ == '__main__':
    sen = "我驾驶摩托车直行，被转弯来的轿车撞倒，受了轻伤，治疗后没什么大问题，交警认定她是全责，可也私聊吗？私聊她改赔尚我的那些费用\
4月30号下午，我父亲被车撞了。肇事车是全则。他开的车是报废车`牌照是套牌，醉酒。肇事后还想逃逸。事情过去5天他们想私了，只拿了3000元。我想告他，我该怎么做。到底是告他对我有利，还是立案对我有利\
律师你好，我们七个朋友在一起喝酒，喝完酒后有个朋友非要开车去打麻将，劝阻不听，我和另外一个朋友一起上了车，在路上发生了交通事故，致使一名老人当场死亡，一辆轿车被撞坏，肇事车辆在一公里外停下，并给交通队打电话，被认定投案自首，请问我和一起在车上的朋友，还有一起喝酒的朋友有民事连带责任吗，肇事司机能否追究我们赔偿死者的赔偿金。{他家里人说我们也有责任}麻烦您在百忙之中给予答复，谢谢。\
你好我骑电瓶车的过程中我走的是逆向行驶由此道路交通事故认定书认定我的是全部责任对方无责"
    # parse(words, tags)
    file_path = '交通事故2018-12-19.txt'
    output_file = read_file(file_path)
    for sen in output_file:
        words = sen_word(sen)
        tags = word_tag(words)
        # name_recognition(words, tags)
    # sen_spliter(output_file)
    # words = sen_word(sen)
    # tags = word_tag(words)
    # name_recognition(words, tags)
    gc.collect()
