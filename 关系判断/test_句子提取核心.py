from mark import *
from TEntityRel import *
from config import *
import tkitFile
import macropodus
from cocoNLP.extractor import extractor
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
ex = extractor()
seg = pkuseg.pkuseg(postag=True)  # 开启词性标注功能
for item in DB.kg_mark.find(q):
    # print(item)
   
    text = seg.cut(item['sentence'])    # 进行分词和词性标注
    
    print("==="*20)
    word_list=[]
    tag_list=[]
    time_list=[]
    for word,tag in text:
        if tag not in ['u','p','r','c','w']:
            word_list.append(word)
            tag_list.append(tag)
        # elif tag in ['t']:
        #     time_list.append(word)
        else:
            word_list.append('     ')

    keyword = macropodus.keyword(item['sentence'])
    print('keyword',keyword)
    locations = ex.extract_locations(item['sentence'])
    print('地址',locations)
    times = ex.extract_time(item['sentence'])
    print('时间',times)
    name = ex.extract_name(item['sentence'])
    print("姓名",name)
    print('time_list',time_list)
    print("原句子:",item['sentence'])
    print('新句子:',"".join(word_list))
    print(text)
    new=[]
    for w,t in zip(word_list,tag_list):
        new.append((w,t))
    print("新的数据",new)
    # kg_tags=[]
    # for one in cut_kg(item['kg']):
    #     tags=[]
    #     for word,tag in one:
    #         # word_list.append(word)
    #         tags.append(tag)
    #     kg_tags.append(' '.join(tags))
    # print(kg_tags)
        
            

