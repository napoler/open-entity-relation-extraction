
from relation_extraction import getRelation
from utils import readFile
import tkitFile
import  gc
# from albert_pytorch import classify
tfile=tkitFile.File()
# Tclass = classify(model_name_or_path='tkitfiles/checkkg')
# def pre(data):
#     """
#     获取预测结果
#     """
#     # tkg = "[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
#     data['sentence_b']=",".join(data['kg'])
#     p = Tclass.pre(data['sentence'], data['sentence_b'])
#     softmax = Tclass.softmax()
#     Tclass.release
#     print("分类", "|", '概率')
#     pre = []
#     for ck, rank in zip([1, 2], softmax):
#         print(ck, "|", rank)
#         pre.append([ck, round(rank, 4)])
#     # del Tclass
#     gc.collect()
#     return p+1, pre

path="/mnt/data/dev/tdata/wiki_zh"
relations_all=[]
for f in tfile.all_path(path):
    # para = readFile('./wiki_00')
    print(f)
    para = readFile(f)
    relations, dict_DSNF = getRelation(para)
    relations_all=relations_all+relations
    
print("Finished !")
print("Final result: ")
# print(relations)
for i,it in enumerate(relations_all):
    print(i,it)
# print(dict_DSNF)

