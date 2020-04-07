from mark import *
from TEntityRel import *
from config import *
import tkitFile

import regex as re

import unicodedata
def filterPunctuation(x):
    x = re.sub(r'[‘’]', "'", x)
    x = re.sub(r'[“”]', '"', x)
    x = re.sub(r'[…]', '...', x)
    x = re.sub(r'[—]', '-', x)
    x = re.sub(r"&nbsp", "", x)
    return x
def get_Relationship_test(item):
    """
    获取关系词
    """
    
    pre_re=''.join(item['text'])
    # pre_re=filterPunctuation(pre_re)

    pre_re = unicodedata.normalize('NFKC', pre_re)
    print(pre_re)
    result=Ner.pre([pre_re])
    labels=Ner.labels[0]
    words_list=[]
    for item in result[0][1]:
        if item['type']=="实体":
            words_list.append(item['words'])
    
    return list(set(words_list)),labels


# item={}
# item["text"]="刘诗诗出生日期1987年"
# words_list,labels=get_Relationship_test(item)
# print(words_list,labels)






q={'check': True,"state":'2','label':int(2)}
# print('q',q)
for item in DB.kg_mark.find(q):
    item['text']=item['sentence']
    words_list,labels=get_Relationship_test(item)
    print(words_list)







# ner_reljson=tkitFile.Json("../tdata/onlyner/dev.json")
# i=0
# all=0
# # ner_list=ner_plus(text)
# for item in ner_reljson.auto_load():
#     print(''.join(item['text']))
#     words_list,labels=get_Relationship_test(item)
#     print(words_list)
#     print(item['label'])
#     print(labels)
#     if len(item['label'])!=len(labels):
#         print("不一样!!!!!!!!!!!!!")
#     if item['label']==labels:
#         # print('准确')
#         i=i+1
#     all=all+1
#     if all%100==0:
#         print(i/all)   
# print(i,all)

