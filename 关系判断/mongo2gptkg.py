import json
import tkitJson
import pymongo
import os
import tqdm
"""
mongo数据库中筛选有效数据导出为gptkg数据库
"""
client = pymongo.MongoClient('localhost')
db = client['gpt2Write'] #数据库名
collection = db['train']
# 创建索引
try:
    db.train.ensure_index([("label",1),("state",1)], background=True)
    pass
except :
    pass


def find_sentence(sentence):
    """
    获取句子对应的所有kg
    """
    data={"sentence":sentence,'kgs':[]}
    kgs=[]
    for it in collection.find({'sentence':sentence,'label':2,'state':'2'}):
        if it['kg'] not in kgs:
            kgs.append(it['kg'])
    data['kgs']=kgs
    return data
# 这里开始
# 写入到文件
filename = '../tdata/gpt2kg_diy.txt'
with open(filename,'w') as f:  
    kgs=[]
    for it in tqdm.tqdm(collection.find({'label':2,'state':'2'})):
        kg=find_sentence(it['sentence'])
        if len(kg['kgs'])>0:
            kg_one=kg['sentence']+" [KGS] "
            for tt in kg['kgs']:
                # print(tt)
                kk=" [S] ".join(tt)
                # print(kk)
                kg_one=kg_one+"[KG] "+kk+" [/KG] "
            kg_one=kg_one+"[/KGS] "

            # print(kg_one)
            kgs.append(kg_one)
            f.write(kg_one+"\n")
    print("知识条数：",len(kgs))


    
print("已经写入到了",filename)

