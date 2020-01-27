import jiagu
import tkitText
import tkitNlp
import tkitFile
from tqdm import tqdm
"""
构建ner数据集

"""
# nerjson=tkitFile.Json("../tdata/onlyner/train.json")
# for item in nerjson.auto_load():
#     print(item['text'])
#     print(ner("".join(item['text'])))


def build_dataset_ner(train_file,type="all"):
    """
    百度训练集
    转化为标注数据集
    实体标注和关系词抽取训练集
    train_file 文件路径
    type="all" 或者mini 
    mini

    构建数据思路
    多个描述合并到一个训练里

    使用ner提取出句子中的实体

    文本: ner+句子
    label: ['K']*len(ner)+正常标记
    """
    tjson=tkitFile.Json(file_path=train_file)
    # all_save=Tjson(file_path="data/train_all.json")
    # tjson_save=Tjson(file_path="data/ner_train.json")
    # dev_json_save=Tjson(file_path="data/ner_dev.json")
    tjson_save=tkitFile.Json(file_path="../tdata/onlyner/train.json")
    dev_json_save=tkitFile.Json(file_path="../tdata/onlyner/dev.json")
    data=[]
    nlp_plus=tkitNlp.Plus()
    nlp_plus.load_tlp()
    flags={}
    for item in tqdm(tjson.load()):
        text= item['text']
        label= ["O"]*len(text)
        ner={}
        for n in item['spo_list']:
            try:
                ner[n['subject']].append(n['predicate'])
            except:
                ner[n['subject']]=[n['predicate']]
        # for  tmp in ner.keys():
        #     print(tmp)
        ner_list =[tmp for  tmp in ner.keys() ]
        # print(ner_list)
        # fner =[word for word,flag in nlp_plus.ner(text)]
        fner=[]
        for word,flag in nlp_plus.ner(text):
            flags[flag]=0
            fner.append(word)
        ner_list=list(set(ner_list+fner))
        ner_list = sorted(ner_list,key = lambda i:len(i),reverse=False)
        # print(ner_list)
        s=0
        for nr in ner_list:
           
            # print(nr)
            label,s1=nlp_plus.mark_word_label(text,label,nr,"实体")
            if s1>=0:
                s=s+1
            # for n in ner[nr]:
            #     label,s1=mark_word_label(text,label,n,"实体")
            #     if s1>=0:
            #         s=s+1
        if s>0:
            one={'text':list(text),'label':label}
            data.append(one)
            # print(one)
            # print(flags)

    nlp_plus.release()
    if type=="all":
        pass
    elif type=="mini":
        data=data[:200]
    # all_save.save(data)
    print("总共数据",len(data))
    f=int(len(data)*0.85)
    tjson_save.save(data=data[:f])
    dev_json_save.save(data=data[f:])


if __name__ == '__main__':
    # fire.Fire()
    train_files=["/mnt/data/dev/tdata/知识提取/train_data.json","/mnt/data/dev/tdata/知识提取/dev_data.json"]
    # train_file="data/ner_train.json"
    # dev_file="data/ner_dev.json"
    # train_file="data/train.json"
    # dev_file="data/dev.json"
    # if os.path.exists(train_file) or os.path.exists(dev_file):
    #     print("文件已经存在")
    #     print("请手动删除")
    # else:
    for f in train_files:
        # build_dataset(f,type="all")
        ###构建知识提取训练集
        # build_dataset_kg(f,type="all")

        #标记实体
        build_dataset_ner(f,type="all")















# text = '威尔士柯基犬是一种小型犬，它们的胆子很大，也相当机警，能高度警惕地守护家园，是最受欢迎的小型护卫犬之一。李恕权'

# print("ltp ner结果")
# # print(text)
# # ner(text)
# print(ner(text))
# words = jiagu.seg(text) # 分词
# # print(words)

# # pos = jiagu.pos(words) # 词性标注
# # print(pos)

# ner = jiagu.ner(words) # 命名实体识别
# print("甲骨ner结果",ner)



# tt=tkitText.Text()
# # tt.load_ht()
# # tt.typed_words(ht_model="tkitfiles/nerht.model")
# tt.load_ht(ht_model="tkitfiles/nerht.model")
# print("HarvestText ner结果",tt.ht.named_entity_recognition(text))




