from mark import *
from TEntityRel import *
from config import *
import tkitFile
import macropodus

def get_Relationship_test(item):
    """
    获取关系词
    """

    pre_re=''.join(item['text'])
    result=P.pre([pre_re])
    labels=P.labels[0]
    words_list=[]
    for item in result[0][1]:
        if item['type']=="描述":
            words_list.append(item['words'])
    return list(set(words_list)),labels




item={}
item["text"]="犬瘟热#主要危害#犬瘟热：本病是病毒引起的急性传染病，主要危害3—12月龄的幼犬。"
print(len(item["text"]))
words_list,labels=get_Relationship_test(item)
print(words_list,labels)




# ner_reljson=tkitFile.Json("../tdata/kg/dev.json")
# i=0
# all=0
# # ner_list=ner_plus(text)
# limit=1000
# for item in ner_reljson.auto_load():
#     print("++++"*10)
#     print(item)
#     print(''.join(item['text']))
#     print("句子长度",len(item['text']))
#     words_list,labels=get_Relationship_test(item)
#     word=[]
#     for lnum,l in enumerate(labels):
#         if l=="K":
#             word.append(item['text'][lnum])
#         if l=="P":
#             word.append(item['text'][lnum])
#     print(''.join(word),words_list)
        

#     if item['label']==labels:
#         # print('准确')
#         i=i+1
#     all=all+1
#     if all%1==0:
#         print('准确率',i/all)
#     if all==limit:
#         break
# print('统计',i,all)









ner_reljson=tkitFile.Json("../tdata/kg/dev.json")
i=0
all=0
r=0
# ner_list=ner_plus(text)
limit=1000
q={'check': True,"state":'2','label':int(2)}
print('q',q)
for item in DB.kg_mark.find(q):
    item['text']=item['kg'][0]+'#'+item['kg'][1]+'#'+item['sentence']
    words_list,labels=get_Relationship_test(item)

    all=all+1
    if len(words_list)>0:
        if   item['kg'][2] in words_list:
            i=i+1
        else:
            print("<hr>")

            
            # print(item)
            print("<br>")
            print("句子长度",len(item['text']))
            print("<br>")
            print(item['text'])
            print("<br>")
            print("标记为:",item['kg'][2])
            print("<br>")
            print("预测为:",words_list)
            print("<br>")

            # 文本相似度
            for word in words_list:
                    sim = macropodus.sim(word ,item['kg'][2])
                    print("<br>")
                    print('word相似度',sim)
                    # if sim<0.6:
                    print("<br>")
                    print("<a href='http://192.168.1.10:7777/edit_submit/"+item['_id']+"/1'>取消<a/>")
                    print("\n<a href='http://192.168.1.10:7777/add_submit?sentence="+item['sentence']+"&kg1="+item['kg'][0]+"&kg2="+item['kg'][1]+"&kg3="+word+"'>添加知识("+word+")<a/>")


            r=r+1
            print("<br>")
            print('准确率',i/all,i/(i+r))

            print("<br>")
            print('统计',i,r,all) 


