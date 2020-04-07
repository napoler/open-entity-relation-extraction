from mark import *
from TEntityRel import *
from config import *
import tkitFile


def get_Relationship_test(item):
    """
    获取关系词
    """

    pre_re=''.join(item['text'])
    print(pre_re)
    result=TNer.pre([pre_re])
    labels=TNer.labels[0]
    words_list=[]
    for item in result[0][1]:
        if item['type']=="关系":
            words_list.append(item['words'])
    return list(set(words_list)),labels


# item={}
# item["text"]="刘诗诗#刘诗诗出生日期1987年"
# words_list,labels=get_Relationship_test(item)
# print(words_list,labels)




q={'check': True,"state":'2','label':int(2)}
# print('q',q)
for item in DB.kg_mark.find(q):
    item['text']=item['kg'][0]+"#"+item['sentence']
    words_list,labels=get_Relationship_test(item)
    print("手动标记:",item['kg'][1])
    print("预测:",words_list)













# ner_reljson=tkitFile.Json("../tdata/ner_rel/test.json")

# i=0
# all=0
# # ner_list=ner_plus(text)
# limit=100000
# for item in ner_reljson.auto_load():
#     # print(item)
#     print("++++"*10)
#     print(''.join(item['text']))
#     words_list,labels=get_Relationship_test(item)
#     word=''
#     for lnum,l in enumerate(labels):
#         if l=="K":
#             word=word+item['text'][lnum]
#     print(word,words_list)
        

#     if item['label']==labels:
#         # print('准确')
#         i=i+1
#     all=all+1
#     print("成功",i,all)
#     if all%100==0:
#         print(i/all)
#     if all==limit:
#         break
# print(i,all)

