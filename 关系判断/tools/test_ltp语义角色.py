# -*- coding: utf-8 -*-
import os

from pyltp import SementicRoleLabeller
from pyltp import Postagger
from pyltp import Segmentor
from pyltp import Parser
LTP_DATA_DIR = '/mnt/data/dev/model/ltp/ltp_data_v3.4.0'  # ltp模型目录的路径

srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`

segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  # 加载模型

labeller = SementicRoleLabeller() # 初始化实例
labeller.load(srl_model_path)  # 加载模型

postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型


words = segmentor.segment('威尔士柯基犬是一种小型犬，它们的胆子很大，也相当机警，能高度警惕地守护家园，是最受欢迎的小型护卫犬之一。')  # 分词
print ('\t'.join(words))
postags = postagger.postag(words)  # 词性标注
print ('\t'.join(postags))
parser = Parser() # 初始化实例
parser.load(par_model_path)  # 加载模型
# words = ['元芳', '你', '怎么', '看']
# postags = ['nh', 'r', 'r', 'v']
arcs = parser.parse(words, postags)  # 句法分析
print ("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

# words = ['元芳', '你', '怎么', '看']
# postags = ['nh', 'r', 'r', 'v']
# arcs 使用依存句法分析的结果
roles = labeller.label(words, postags, arcs)  # 语义角色标注
# 打印结果
for role in roles:
    print( role.index, "".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
    print(words[role.index])
    for arg in role.arguments :
        # print(role.index)
        # print(arg.name, arg.range.start, arg.range.end)
        if arg.range.start==arg.range.end:
            print(words[arg.range.start])
        else:
            print(words[arg.range.start:arg.range.end])


segmentor.release()  # 释放模型
postagger.release()  # 释放模型
labeller.release()  # 释放模型
parser.release()  # 释放模型
