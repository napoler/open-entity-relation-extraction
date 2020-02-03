import tkitFile
import tkitDb
import tkitText
import tkitNlp
import tkitSearch

from tqdm import tqdm
import os
import shutil
import json

from  config import *
class KgDatabase:
    def __init__(self):
        tkitFile.File().mkdir("../tdata")
        
        self.tdb= tkitDb.LDB(path="../tdata/lv.db")
        self.ss=tkitSearch.Search()
        pass
    def read_kg(self):
        kgjson=tkitFile.Json("../data/knowledge_triple.json")
        for item in kgjson.auto_load():
            # print(item)
            yield item
    
    def json_lv(self):
        """
        将json版本保存到数据
        """
        # self.tdb.load("kg")
        # Db.kg
        tt=tkitText.Text()
        for item in tqdm(self.read_kg()):
            key=tt.md5(item["句子"]+'，'.join(item['知识']))
            data={
                "sentence":item["句子"],
                "kg":item['知识']
            }
            # self.tdb.put_data([(key,data)])
        data['_id']=key
        try:
            DB.kg.insert_one(data)
        except:
            pass
            # self.tdb.put_data([item])
    def auto_sentence(self,key,data):
        """
        自动储存知识
        data={
        "sentence":item["句子"],
        "kg":item['知识'],
        "label":1
        }
           
        """
        # self.tdb.load("kg_auto_sentence")
        data['_id']=key
        try:
           DB.kg_auto_sentence.insert_one(data)
        except:
            print('保存失败',key)
            DB.kg_auto_sentence.update_one(data)
            pass
        # self.tdb.put_data([(key,data)])
    def index_one(self,k,item):
        """
        添加一个索引
        """
        
        data=[{'title':",".join(item.get("kg")),'content':item.get("sentence"),'path':k}]
        # print(data)
        self.ss.add(data) 
    def mark_sentence(self,key,data):
        """
        将json版本保存到数据
        data={
        "sentence":item["句子"],
        "kg":item['知识'],
        "label":1
        }
           
        """
        # self.tdb.load("kg_mark")
        # tt=tkitText.Text()
        # key=tt.md5(item["sentence"]+'，'.join(item['kg']))
        # self.index_one(key,data)
        # self.tdb.put_data([(key,data)])
        data['_id']=key
        # DB.kg_mark(data)
        # print(DB.kg_mark.insert_one(data).inserted_id)
        # db.kg_mark.update({'_id': '0f6f5f0a108dc5536ca16c8d994b6773'},   {"$set" : {"check" : False}})
        
        old=DB.kg_mark.find_one({"_id":key})
        if old==None:
            print("新数据",key)
            try:
                DB.kg_mark.insert_one(data)
                # DB.kg_mark.update_one(data)  
                pass
            except:
                print("保存失败",key)
                pass
        else:
            new_filed={}
            for k in data:
                if old.get(k)==None:
                    new_filed[k]=data[k]
                
            if len(new_filed)>=0:
                print("更新",key)
                try:
                    # DB.kg_mark.insert_one(data)
                    DB.kg_mark.update_one({'_id': key},   {"$set" :new_filed})  
                    pass
                except:
                    print("保存失败",key)
                    pass   
            else:
                pass

            
    def get_unmarked_auto_sentence(self):
        """
        获取没有标记的数据
        自动标记数据
        """
        # self.tdb.load("kg_auto_sentence")
        
        for v in DB.kg_auto_sentence.find():
            # print(k)
            # self.tdb.load("kg_mark")
            if self.tdb.get(k)==None:
                pass
            else:
                self.tdb.load("kg_auto_sentence")
                continue
            # print(self.tdb.get(k))  
            try: 
                yield k,self.tdb.str_dict(v)
            except:
                self.tdb.load("kg_auto_sentence")
                continue
            self.tdb.load("kg_auto_sentence")
    def get_unmarked(self):
        """
        获取没有标记的数据
        """
        self.tdb.load("kg")
        for k,v in self.tdb.get_all():
            # print(k)
            self.tdb.load("kg_mark")
            if self.tdb.get(k)==None:
                pass
            else:
                self.tdb.load("kg")
                continue
            # print(self.tdb.get(k))  
            try: 
                yield k,self.tdb.str_dict(v)
            except:
                self.tdb.load("kg")
                continue
            self.tdb.load("kg")

    def recheck_all(self):
        """
        重新标记数据
        """
        self.tdb.load("kg_mark")
        for k,v in self.tdb.get_all():
            try: 
                yield k,self.tdb.str_dict(v)
            except:
                pass




    def check_marked(self,key):
        # self.tdb.load("kg_mark")
        # kg=self.tdb.get(key)
        # print("检查重复",kg)
        # print("检查重复",DB.kg_mark.find_one({"_id":key}))
        if DB.kg_mark.find_one({"_id":key}):
            return True
        else:
            return False

    def json_remove_duplicates(self,json_file):
        print("尝试移除重复数据")
        origin_json=tkitFile.Json(json_file)
        temp=tkitFile.Json(json_file+".tmp.json")
        tt=tkitText.Text()
        temp_keys=[]
        data=[]
        num_duplicates=0
        for i, item in enumerate(origin_json.auto_load()):

            # if i%10000==0:
                # print("~~~~"*10)
                # print('已经处理',i)
                # temp.save(data)
                # data=[]
            # key=tt.md5(str(item))
            # if key in temp_keys:
            #     # print("重复数据",item)
            #     num_duplicates=num_duplicates+1
            #     pass
            # else:
            #     temp_keys.append(key)
            #     data.append(item)
            data.append(json.dumps(item))
        new=list(set(data))
        print("原始长度",len(data))
        new_json=[]
        for item in new:
            new_json.append(json.loads(item))
        print("新长度",len(new_json))
        temp.save(new_json)
        print("移除重复内容",num_duplicates)
        #覆盖之前文件
        shutil.move(json_file+".tmp.json",json_file)

    def save_to_json_backup(self):
        """
        将数据保存为json版本
        """
        kgjson_t=tkitFile.Json("../tdata/data/train.json")
        # kgjson_d=tkitFile.Json("../tdata/kg_check/dev.json")
        # kgjson_l=tkitFile.Json("../tdata/kg_check/labels.json")
        # self.tdb.load("kg_mark")
        data=[]
        i=0
        n=0
        self.tdb.load("kg_mark")
        tt=tkitText.Text()
        i=-1
        for k,v in self.tdb.get_all():
            i=i+1
            # print(v)
            if v==None:
                n += 1
            else:
                try: 
                    it=self.tdb.str_dict(v)
                    one={}
                    one['sentence']=" [kg] "+",".join(it['kg'])+" [/kg] "+it['sentence']
                    one['label']=it['label']-1
                    
                    if int(one['label']) in [0,1] and len(it['kg'])==3:
                        data.append(it)
                    else:
                        # print(it)
                        pass
                except:
                    # self.tdb.load("kg")
                    continue
        # c=int(len(data)*0.85)
        print("总数据",len(data),i,n)
        kgjson_t.save(data)
        # kgjson_d.save(data[c:])
        #自动处理重复标记问题
        self.json_remove_duplicates("../tdata/data/train.json")
        print("已经将数据导出到 ../tdata/data")

    def save_to_json(self):
        """
        可以用于测试知识是否是合理的
        """
        kgjson_t=tkitFile.Json("../tdata/kg_check/train.json")
        kgjson_d=tkitFile.Json("../tdata/kg_check/dev.json")
        kgjson_l=tkitFile.Json("../tdata/kg_check/labels.json")
        # self.tdb.load("kg_mark")
        data=[]
        i=0
        n=0
        # self.tdb.load("kg_mark")
        tt=tkitText.Text()
        i=-1
        for it in DB.kg_mark.find():
        # for k,v in self.tdb.get_all():
            k=it["_id"]
            i=i+1
            # print(v)
            # if v==None:
            #     n += 1
            # else:
            try: 
                # it=self.tdb.str_dict(v)
                one={}
                one['sentence']=" [kg] "+",".join(it['kg'])+" [/kg] "+it['sentence']
                one['label']=it['label']-1
                
                if int(one['label']) in [0,1] and len(it['kg'])==3  and it.get('check')!=None and it.get('state')=='2':
                    data.append(one)
                else:
                    # print(it)
                    pass
            except:
                # self.tdb.load("kg")
                continue
        c=int(len(data)*0.85)
        print("总数据",len(data),i,n)
        kgjson_t.save(data[:c])
        kgjson_d.save(data[c:])
        #自动处理重复标记问题
        self.json_remove_duplicates("../tdata/kg_check/train.json")
        self.json_remove_duplicates("../tdata/kg_check/dev.json")
        print("已经将数据导出到 ../tdata/kg_check")
        
    def auto_label(self,label,new):
        if label=="O":
            return new
        else:
            # return label+'_'+new
            return new
    def mark_word_label(self,text,label_b,word,tp="实体"):
        # print("pp",text,label_b,word)
        
        #自动搜索最大匹配单词
        tt=tkitText.Text()
        c,r=tt.find_match(text,word)
        if r>50:
            p=c
        else:
            p=word

        # a="嘉朵能够帮助或带领丹恩·萧完成许多事，如逛商店；牠在完成一天的工作后便待在马厩里"
        # b="帮助丹恩"

        start_p =text.find(p)
        end_p=text.find(p)+len(p)-1
        # print("start_p",start_p)
        if start_p>=0:
            if len(p)>3:
                label_b[start_p]=self.auto_label(label_b[start_p],'B-'+tp)
                label_b[end_p]=self.auto_label(label_b[end_p],'E-'+tp)
                for n in range(start_p+1,end_p):
                    label_b[n]=self.auto_label(label_b[n],'M-'+tp)
                    pass
            elif len(p)==3:
                label_b[start_p]=self.auto_label(label_b[start_p],'B-'+tp)
                label_b[end_p]=  self.auto_label(label_b[end_p],'E-'+tp)
                label_b[start_p+1]=  self.auto_label(label_b[start_p+1],'M-'+tp)
            elif len(p)==1:
                label_b[start_p]=self.auto_label(label_b[start_p],'S-'+tp)
            elif len(p)==2:
                label_b[start_p]=self.auto_label(label_b[start_p],'B-'+tp)
                label_b[end_p]=  self.auto_label(label_b[end_p],'E-'+tp)
        return label_b,start_p
    def unique_data(self):
        """
        值保存标记为yes的数据
        并且对数据进行合并 
        """
        # self.tdb.load("kg_mark")
        tt=tkitText.Text()
        i=-1
        for it in DB.kg_mark.find():
        # for k,v in self.tdb.get_all():
            k=it["_id"]
            try: 
                # it=self.tdb.str_dict(v)
                # if it['label']-1!=1 or it['state']!='2':
                if it['label']-1!=1 or it['state']!='2' or  it.get('check')==None or len(it['kg'])!=3:
                    continue
                else:
                    # print("状态为2")
                    pass
            except:
                # self.tdb.load("kg")
                continue
                        # print(it)
            kgs=[]
            key = tt.md5(it['sentence']+str(it['kg'][0])+str(it['kg'][1]))
            # self.tdb.load("kg_mark_unique_data")
            # kg=self.tdb.get(key)

            kg=DB.kg_mark_unique_data.find_one({"_id":key})
            # print("kg",kg)
            if kg==None:
                # 新建
                print("新建")
                if len(it['kg'])==3:
                    kgs.append(it['kg'])
                    one={"_id":key,'sentence':it['sentence'],'kgs':kgs}
                    DB.kg_mark_unique_data.insert_one(one)
            else:
                # 更新
                print("更新")
                kgs=kg['kgs']
                if len(it['kg'])==3 and it['kg'] not in kgs:
                    kgs.append(it['kg'])
                one={"_id":key,'sentence':it['sentence'],'kgs':kgs}
                # print(one)
                # self.tdb.put(key,one)
                # self.tdb.load("kg_mark")
                DB.kg_mark_unique_data.update_one({"_id":key},{"$set" :one})
            i=i+1
        print("总共",i)
    def clear_unique_data(self):
        DB.kg_mark_unique_data.drop()


    def get_key(self,data):
        tt=tkitText.Text()
        key=tt.md5(data["sentence"]+'，'.join(data['kg']))
        return key
    def updata_key(self):
        """
        自动更新key
        
        """
        kg_mark=0
        kg_mark_all=0
        self.tdb.load("kg_mark")
        for k,v in self.tdb.get_all():
            try:
                kg_mark_all=kg_mark_all+1
                it=self.tdb.str_dict(v)
                if len(it['kg'])==3:
                    print("可以更新")
                    key=self.get_key(it)
                    it['_id']=key
                    print("key",key)
                    print(DB.kg_mark.insert_one(it).inserted_id)
                    # # print('old',k,"new",key)
                    # if key!=k:
                    #     self.tdb.delete(k)
                    #     self.mark_sentence(key, it)
                    #     # print("更新")
                    #     kg_mark=kg_mark+1
            except:
                pass
        kg_auto_sentence=0
        kg_auto_sentence_all=0
        self.tdb.load("kg_auto_sentence")
        for k,v in self.tdb.get_all():
            try:
                kg_auto_sentence_all=kg_auto_sentence+1
                it=self.tdb.str_dict(v)
                if len(it['kg'])==3:
                    # print("可以更新")
                    key=self.get_key(it)
                    it['_id']=key
                    print(DB.kg_auto_sentence.insert_one(it).inserted_id)
                    # # print('old',k,"new",key)
                    # if key!=k:
                    #     self.tdb.delete(k)
                    #     self.mark_sentence(key, it)
                    #     # print("更新")
                    #     kg_auto_sentence=kg_auto_sentence+1
            except:
                pass
        kg=0
        kg_all=0
        self.tdb.load("kg")
        for k,v in self.tdb.get_all():
            try:
                kg_all=kg_all+1
                it=self.tdb.str_dict(v)
                if len(it['kg'])==3:
                    # print("可以更新")
                    key=self.get_key(it)
                    it['_id']=key
                    print(DB.kg.insert_one(it).inserted_id)
                    # # print('old',k,"new",key)
                 
                    # if key!=k:
                    #     self.tdb.delete(k)
                    #     self.mark_sentence(key, it)
                    #     # print("更新")
                    #     kg=kg+1
            except:
                pass
        # print("kg_mark",kg_mark_all,kg_mark)
        # print("kg",kg_all,kg)
        # print("kg_auto_sentence",kg_auto_sentence_all,kg_auto_sentence)
    def save_to_json_ner_rel(self):
        tkitFile.File().mkdir("../tdata/ner")
        kgjson_t=tkitFile.Json("../tdata/ner_rel/train.json")
        kgjson_d=tkitFile.Json("../tdata/ner_rel/dev.json")
        # kgjson_l=tkitFile.Json("../tdata/labels.json")
        # self.tdb.load("kg_mark_unique_data")
        data=[]
        all_data_id=[]
        # for k,v in self.tdb.get_all():
        for it in DB.kg_mark_unique_data.find():
            # print("k",k)
            k=it['_id']
            try: 
                # it=self.tdb.str_dict(v)
                # print("it",it)
                
                ner={}
                for one in it['kgs']:
                    # print(one)
                    # label,s1=self.mark_word_label(it['sentence'],label,one[0],"实体")
                    # label,s1=self.mark_word_label(it['sentence'],label,one[1],"关系")
                    try:
                        if one[1] not in ner[one[0]]:
                            ner[one[0]].append(one[1])
                    except:
                        ner[one[0]]=[one[1]]
                # print(ner)
                
                for nr in ner:
                    s=0
                    label=['O']*len(it['sentence'])
                    # print(ner[nr])
                    for n in ner[nr]:
                        # print(n)
                        # print("label",label)
                        # print(it['sentence'])
                        label,s1=self.mark_word_label(it['sentence'],label,n,"关系")
                        # print(label,s1)
                        if s1>=0:
                            s=s+1
                    if s>0:
                        one_ner={'text':list(nr+'#'+it['sentence']),'label':['K']*len(nr)+['X']+label}
                        data.append(one_ner)
                        # print(one_ner)




                # # print(label)
                # d={'text':list(it['sentence']),'label':label}
                # # print(d)
                # # print(d)
                # data.append(d)
            except:
                # self.tdb.load("kg")
                continue
        c=int(len(data)*0.85)
        kgjson_t.save(data[:c])
        kgjson_d.save(data[c:])
        print("总共生成数据",len(data))
        #自动处理重复标记问题
        self.json_remove_duplicates("../tdata/ner_rel/train.json")
        self.json_remove_duplicates("../tdata/ner_rel/dev.json")
        print("已经将数据导出到 ../tdata/ner_rel")
  
    def save_to_json_ner(self):
        tkitFile.File().mkdir("../tdata/onlyner")
        kgjson_t=tkitFile.Json("../tdata/onlyner/train.json")
        kgjson_d=tkitFile.Json("../tdata/onlyner/dev.json")
        # kgjson_l=tkitFile.Json("../tdata/labels.json")
        self.tdb.load("kg_mark_unique_data")
        data=[]
        all_data_id=[]
        nlp_plus=tkitNlp.Plus()
        nlp_plus.load_tlp()
        flags={}
        for it in DB.kg_mark_unique_data.find():
            # print("k",k)
            k=it['_id']
            try: 
                # it=self.tdb.str_dict(v)
                text=it['sentence']
                # print("it",it)
                label= ["O"]*len(text)
                ner={}
                for one in it['kgs']:
                    # print(one)
                    # label,s1=self.mark_word_label(it['sentence'],label,one[0],"实体")
                    # label,s1=self.mark_word_label(it['sentence'],label,one[1],"关系")
                    try:
                        if one[1] not in ner[one[0]]:
                            ner[one[0]].append(one[1])
                    except:
                        ner[one[0]]=[one[1]]
                # print("++++++"*10)
                # print('text',text)                
                ner_list =[tmp for  tmp in ner.keys() ]
                # print('ner_list',ner_list)   
                # print(ner_list)
                # fner =[word for word,flag in nlp_plus.ner(text)]
                fner=[]
                for word,flag in nlp_plus.ner(text):
                    flags[flag]=0
                    fner.append(word)
                ner_list=list(set(ner_list+fner))
                ner_list = sorted(ner_list,key = lambda i:len(i),reverse=False)

                # print('ner_list',ner_list)
                s=0
                for nr in ner_list:
                
                    # print(nr)
                    label,s1=nlp_plus.mark_word_label(text,label,nr,"实体")
                    if s1>=0:
                        s=s+1
                if s>0:
                    one={'text':list(text),'label':label}
                    data.append(one)
                    
                    # print(flags)
            except:
                pass
        nlp_plus.release()
 
        c=int(len(data)*0.85)
        kgjson_t.save(data[:c])
        kgjson_d.save(data[c:])
        print("总共生成数据",len(data))
        #自动处理重复标记问题
        self.json_remove_duplicates("../tdata/onlyner/train.json")
        self.json_remove_duplicates("../tdata/onlyner/dev.json")
        print("已经将数据导出到 .../tdata/onlyner/")
   
    def save_to_json_kg(self):
        """
        保存知识提取训练集
        https://www.kaggle.com/terrychanorg/albert-bilstm-crf-pytorch/data
        """
        tkitFile.File().mkdir("../tdata/kg")
        kgjson_t=tkitFile.Json("../tdata/kg/train.json")
        kgjson_d=tkitFile.Json("../tdata/kg/dev.json")
        # kgjson_l=tkitFile.Json("../tdata/labels.json")
        
        # self.tdb.load("kg_mark_unique_data")
        data=[]
        all_data_id=[]
        for it in DB.kg_mark_unique_data.find():
            # print("k",k)
            k=it['_id']
            try: 
                # it=self.tdb.str_dict(v)
                # print("it",it)
                label=['O']*len(it['sentence'])
                s=0
                for one in it['kgs']:
                    label,s1=self.mark_word_label(it['sentence'],label,one[2],"描述")
                    if s1>=0:
                        s=s+1
                    # label,s1=self.mark_word_label(it['sentence'],label,one[1],"关系")
                # print(label)
                d={'text':list(one[0]+'#'+one[1]+'#'+it['sentence']),'label':['K']*len(one[0])+['X']+['P']*len(one[1])+['X']+label}
                # print(d)
                # print(d)
                if s>0:
                    # print(s)
                    data.append(d)
            except:
                # self.tdb.load("kg")
                continue
        c=int(len(data)*0.85)
        kgjson_t.save(data[:c])
        kgjson_d.save(data[c:])
        print("总共生成数据",len(data))
        #自动处理重复标记问题
        self.json_remove_duplicates("../tdata/kg/train.json")
        self.json_remove_duplicates("../tdata/kg/dev.json")
        print("已经将数据导出到 ../tdata/kg")
if __name__ == '__main__':

    while True:
        
        print("""
        支持以下命令：
        1 将json版本保存到数据
        2 保存json为训练数据 可以用于测试知识是否是合理的
        3 创建独特数据    
        4 清空独特数据库 unique_data
        5 创建ner于关系标记数据集
        6 保存知识提取数据集
        7 保存ner数据集      
        8 将所有数据保存为json 备份  
        9 更新key
        """)
        x=input("输入命令：")
        try:
            x= int(x)
        except:
            pass
        kg=KgDatabase()    
        if x==1:
            # kg=KgDatabase()
            kg.json_lv() #将json版本保存到数据
        elif x==2:
            # kg=KgDatabase()
            kg.save_to_json()
        elif x==3:

            kg.unique_data()
            # kg.tdb.close()
        elif x==4:
            kg.clear_unique_data()
        elif x==5:
            kg.save_to_json_ner_rel()
        elif x==6:
            kg.save_to_json_kg()
        elif x==7:
            kg.save_to_json_ner()
        elif x==8:
            kg.save_to_json_backup()
        elif x==9:
            kg.updata_key()
        else:
            print("输入有误")
            
            



    # kg=KgDatabase()
    # kg.json_lv() #将json版本保存到数据




