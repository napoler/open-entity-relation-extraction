# from memory_profiler import profile
import gc

import tkitNlp
from albert_pytorch import classify
from TEntityRel import *
from tkitMarker import *
import pymongo

def get_p():
    # import tkitFile
    P = Pre()
    P.args['conf'] = "tkitfiles/v0.1/config.json"
    P.args['load_path'] = "tkitfiles/v0.1/pytorch_model.bin"
    P.args['vocab'] = "tkitfiles/v0.1/vocab.txt"
    P.args['label_file'] = "tkitfiles/v0.1/tag.txt"
    P.args['max_length'] = 50
    P.setconfig()
    return P


def get_tner():
    # 初始化提取关系词
    TNer = Pre()
    TNer.args['conf'] = "tkitfiles/ner_rel/config.json"
    TNer.args['load_path'] = "tkitfiles/ner_rel/pytorch_model.bin"
    TNer.args['vocab'] = "tkitfiles/ner_rel/vocab.txt"
    TNer.args['label_file'] = "tkitfiles/ner_rel/tag.txt"
    TNer.args['albert_path'] = "tkitfiles/ner_rel"
    TNer.args['albert_embedding'] = 312
    TNer.args['rnn_hidden'] = 400

    TNer.model_version = 'ner_rel'
    TNer.args['max_length'] = 50
    TNer.setconfig()
    return TNer


def get_ner():
    # 初始化提取实体

    Ner = Pre()
    Ner.args['conf'] = "tkitfiles/ner/config.json"
    Ner.args['load_path'] = "tkitfiles/ner/pytorch_model.bin"
    Ner.args['vocab'] = "tkitfiles/ner/vocab.txt"
    Ner.args['label_file'] = "tkitfiles/ner/tag.txt"
    Ner.args['albert_path'] = "tkitfiles/ner"
    Ner.args['albert_embedding'] = 312
    Ner.args['rnn_hidden'] = 400

    Ner.model_version = 'ner'
    Ner.args['max_length'] = 50
    Ner.setconfig()
    return Ner


TNer = get_tner()

Ner = get_ner()
P = get_p()

Tclass = classify(model_name_or_path='tkitfiles/checkkg')
# 检查是不是知识
Check_kg = classify(model_name_or_path='../tdata/albert_check_kg')
# check_pet=classify(model_name_or_path='../tdata/albert-chinese-pytorch-pet')


# ie=tkitNlp.TripleExtractor()

# 基于已存在的词典获取关系词
Terry_er = TEntityRel()

ttht = tkitText.Text()
ttht.load_ht()
HT = ttht.ht



#这里定义mongo数据
client = pymongo.MongoClient("localhost", 27017)
DB = client.openkg
print(DB.name)
# DB.my_collection
# Collection(Database(MongoClient('localhost', 27017), u'test'), u'my_collection')
# print(DB.my_collection.insert_one({"x": 10}).inserted_id)