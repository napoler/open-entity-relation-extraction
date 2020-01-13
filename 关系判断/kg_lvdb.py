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
        

if __name__ == '__main__':

    while True:
        
        print("""
        支持以下命令：
        1 将json版本保存到数据
        2 保存json为训练数据
        

        
        
        """)
        x=input("输入命令：")
        try:
            x= int(x)
        except:
            pass
        
        if x==1:
            kg=KgDatabase()
            kg.json_lv() #将json版本保存到数据
        elif x==2:
            kg=KgDatabase()
            kg.save_to_json()
        else:
            print("输入有误")
            
            



    # kg=KgDatabase()
    # kg.json_lv() #将json版本保存到数据




