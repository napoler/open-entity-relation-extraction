import tkitFile
import tkitDb
import tkitText
from tqdm import tqdm

class KgDatabase:
    def __init__(self):
        tkitFile.File().mkdir("../tdata")
        
        self.tdb= tkitDb.LDB(path="../tdata/lv.db")

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
        self.tdb.load("kg")
        tt=tkitText.Text()
        for item in tqdm(self.read_kg()):
            key=tt.md5(item["句子"]+'，'.join(item['知识']))
            data={
                "sentence":item["句子"],
                "kg":item['知识']
            }
            self.tdb.put_data([(key,data)])
            # self.tdb.put_data([item])
    def mark_sentence(self,key,data):
        """
        将json版本保存到数据
        data={
        "sentence":item["句子"],
        "kg":item['知识'],
        "label":1
        }
           
        """
        self.tdb.load("kg_mark")
        # tt=tkitText.Text()
        # key=tt.md5(item["sentence"]+'，'.join(item['kg']))
        self.tdb.put_data([(key,data)])
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
        self.tdb.load("kg_mark")
        kg=self.tdb.get(key)
        if kg==None:
            return False
        else:
            return True



    def save_to_json(self):
        kgjson_t=tkitFile.Json("../tdata/train.json")
        kgjson_d=tkitFile.Json("../tdata/dev.json")
        kgjson_l=tkitFile.Json("../tdata/labels.json")
        self.tdb.load("kg_mark")
        data=[]
        for k,v in self.tdb.get_all():
            try: 
                it=self.tdb.str_dict(v)
                one={}
                one['sentence']=" [kg] "+",".join(it['kg'])+" [/kg] "+it['sentence']
                one['label']=it['label']-1
                if int(one['label']) in [0,1]:
                   data.append(one)
                else:
                    print(it)
            except:
                self.tdb.load("kg")
                continue
        c=int(len(data)*0.85)
        kgjson_t.save(data[:c])
        kgjson_d.save(data[c:])
        # labels=[{"label": 0, "sentence": "Bad"},{"label": 1, "sentence": "Good"}]
        # kgjson_l.save(labels)
        print("已经将数据导出到 ../tdata")
        
    def auto_label(self,label,new):
        if label=="O":
            return new
        else:
            # return label+'_'+new
            return new
    def mark_word_label(self,text,label_b,word,tp="实体"):
        p=word
        start_p =text.find(p)
        end_p=text.find(p)+len(p)-1
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
        self.tdb.load("kg_mark")
        tt=tkitText.Text()
        i=-1
        for k,v in self.tdb.get_all():
            try: 
                it=self.tdb.str_dict(v)
                if it['label']-1!=1:
                    continue
            except:
                # self.tdb.load("kg")
                continue
                        # print(it)
            kgs=[]
            key = tt.md5(it['sentence']+str(it['kg'][0])+str(it['kg'][1]))
            self.tdb.load("kg_mark_unique_data")
            kg=self.tdb.get(key)

            if kg==None:
                kgs.append(it['kg'])
                # print('111')
            else:
                # print("222222222222")
                try:
                    # print('kgs',kg) 
                    kg=self.tdb.str_dict(kg) 
                    kgs=kg['kgs']
                    kgs.append(it['kg'])
                except:
                    pass
            # print(kgs)
            one={'sentence':it['sentence'],'kgs':kgs}
            print(one)
            self.tdb.put(key,one)
            self.tdb.load("kg_mark")
            i=i+1
        print("总共",i)
    def clear_unique_data(self):
        self.tdb.load("kg_mark_unique_data")
        for k,v in self.tdb.get_all():
            try:
                self.tdb.delete(k)
            except:
                print("删除失败")

   
    def save_to_json_ner(self):
        tkitFile.File().mkdir("../tdata/ner")
        kgjson_t=tkitFile.Json("../tdata/ner/train.json")
        kgjson_d=tkitFile.Json("../tdata/ner/dev.json")
        # kgjson_l=tkitFile.Json("../tdata/labels.json")
        self.tdb.load("kg_mark_unique_data")
        data=[]
        all_data_id=[]
        for k,v in self.tdb.get_all():
            # print("k",k)
            try: 
                it=self.tdb.str_dict(v)
                # print("it",it)
                label=['O']*len(it['sentence'])
                for one in it['kgs']:
                    # print(one)
                    label,s1=self.mark_word_label(it['sentence'],label,one[0],"实体")
                    label,s1=self.mark_word_label(it['sentence'],label,one[1],"关系")
                # print(label)
                d={'text':list(it['sentence']),'label':label}
                # print(d)
                # print(d)
                data.append(d)
            except:
                # self.tdb.load("kg")
                continue
        c=int(len(data)*0.85)
        kgjson_t.save(data[:c])
        kgjson_d.save(data[c:])
        print("总共生成数据",len(data))

        print("已经将数据导出到 ../tdata")
   
    def save_to_json_kg(self):
        """
        保存知识提取训练集
        https://www.kaggle.com/terrychanorg/albert-bilstm-crf-pytorch/data
        """
        tkitFile.File().mkdir("../tdata/kg")
        kgjson_t=tkitFile.Json("../tdata/kg/train.json")
        kgjson_d=tkitFile.Json("../tdata/kg/dev.json")
        # kgjson_l=tkitFile.Json("../tdata/labels.json")
        
        self.tdb.load("kg_mark_unique_data")
        data=[]
        all_data_id=[]
        for k,v in self.tdb.get_all():
            # print("k",k)
            try: 
                it=self.tdb.str_dict(v)
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
        print("已经将数据导出到 ../tdata")
if __name__ == '__main__':

    while True:
        
        print("""
        支持以下命令：
        1 将json版本保存到数据
        2 保存json为训练数据
        3 创建独特数据    
        4 清空独特数据库 unique_data
        5 创建ner于关系标记数据集
        6 保存知识提取数据集
        
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
            kg.save_to_json_ner()
        elif x==6:
            kg.save_to_json_kg()
        else:
            print("输入有误")
            
            



    # kg=KgDatabase()
    # kg.json_lv() #将json版本保存到数据




