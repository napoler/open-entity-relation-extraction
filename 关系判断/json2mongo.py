import json
import tkitJson
import pymongo
import os
import tqdm
"""
将json导入到mongo数据库
"""
client = pymongo.MongoClient('localhost')
db = client['gpt2Write'] #数据库名
# collection = db['images']
def add_col(name,path):
    """
    name：表名字
    path:json文件目
    
    """
    Tjson=tkitJson.Json(path)
    collection = db[name]
    for it in tqdm.tqdm(Tjson.load()):
        # print(it)
        collection.insert_one(it)
    # with open(path, encoding="utf-8") as jf:
    #     str = jf.read()
    #     data = []
    #     data.extend(json.loads(str))
    #     collection = db[name]
    #     if len(data)>0:
    #         collection.insert_many(data)
    



# 数据所在目录
path='../tdata/data'
for pathname,dirnames,filenames in os.walk(path):
    for filename in filenames:
        file=os.path.join(pathname,filename)
        if filename.endswith("json"):
            print(file,filename.replace(".json",''))
            name=filename.replace(".json",'')
            add_col(name,file)
print("已经全部导入！")
client.close() #写完关闭连接