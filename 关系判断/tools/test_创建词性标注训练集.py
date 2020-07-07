from mark import *
from TEntityRel import *
from config import *
import tkitFile
import macropodus

import pkuseg

def cut_kg(kg):
    seg = pkuseg.pkuseg(postag=True)  # 开启词性标注功能
    kg_list=[]
    for it in kg:
        kg_list.append(seg.cut(it) )  # 进行分词和词性标注
    # print(kg_list)
    return kg_list
i=0
all=0
r=0
# ner_list=ner_plus(text)
limit=1000
q={'check': True,"state":'2','label':int(2)}
# print('q',q)
seg = pkuseg.pkuseg(postag=True)  # 开启词性标注功能
for item in DB.kg_mark.find(q):
    print(item)
   
    text = seg.cut(item['sentence'])    # 进行分词和词性标注
    print(text)
    word_list=[]
    tag_list=[]
    for word,tag in text:
        word_list.append(word)
        tag_list.append(tag)
    print(" ".join(word_list)," ".join(tag_list))
    kg_tags=[]
    for one in cut_kg(item['kg']):
        tags=[]
        for word,tag in one:
            # word_list.append(word)
            tags.append(tag)
        kg_tags.append(' '.join(tags))
    print(kg_tags)
        
            

