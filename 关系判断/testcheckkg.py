from mark import *
from TEntityRel import *
from config import *
import tkitFile

def pre(data):
    """
    获取预测结果
    """
    p = Tclass.pre(data['sentence'], data['sentence_b'])
    softmax = Tclass.softmax()
    # Tclass.release()
    return p, softmax[1]
kgjson=tkitFile.Json("../tdata/kg_check/dev.json")
i=0
all=0
for item in kgjson.auto_load():
    # print(item)


    label,rank=pre(item)
    if label==item['label']:
        i=i+1
    all=all+1
    # print(pre(item))
    if all%100==0:
        print(i/all)   
print(i,all)

