#encoding=utf-8
from kg_lvdb import KgDatabase
from albert_pytorch import classify
import jiagu
import tkitFile
import tkitText
from harvesttext import HarvestText
def one(item): 
    key=tt.md5(item["sentence"]+'，'.join(item['kg']))
    print(key)
    if kg.check_marked(key)==True:
        print("已经标记")
        return
    else:
        pass
    s=item['sentence']
    for w in item['kg']:
        s=s.replace(w,"<<█"+w+"█>>")
    print("--------------------------------------------------------")
    print("句子：",s)
    print("知识：",item['kg'])
    print("--------------------------------------------------------")
    # print( tclass.pre(item['sentence']))
    tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
    p=tclass.pre(tkg)
    ckg="#u#".join(item['kg'])
    ckg=check_kg.pre(ckg)
    print("判断是不是知识",ckg+1)
    # print()
    # print(p+1)
    if int(p)==0:
        print("Ai预测：No(1)")
        pass
    elif int(p)==1 and int(ckg)==1:
        print("Ai预测：Yes(2)")
        if item['kg'][1] in ["负责管辖",'生于','位于']:
            x=2
        else:
            # print("输入1(No)或者2(Yes)")
            x = input("输入1(No)或者2(Yes) 默认1:")
        # print
        try:
            x= int(x)
        except:
            pass
            x=1
        if x==1:
            print("选择No")
        else:
            print("选择Yes")
        data=item
        data["label"]=x
     
        kg.mark_sentence(key,data)
        # i=i+1
        # exit()
    else:
        print("Ai预测：No(1)")
        if item['kg'][1] in ["负责管辖",'生于','位于']:
            x=2
        else:
            # print("输入1(No)或者2(Yes)")
            x = input("输入1(No)或者2(Yes) 默认1:")
        # print
        try:
            x= int(x)
        except:
            pass
            x=1
        if x==1:
            print("选择No")
        else:
            print("选择Yes")
        data=item
        data["label"]=x
        kg.mark_sentence(key,data)
        # i=i+1
        # exit()



kg=KgDatabase()
ht0 = HarvestText()
tfile=tkitFile.File()
tt=tkitText.Text()
i=0
tclass=classify(model_name_or_path='/mnt/data/dev/github/albert_pytorch/albert_pytorch/albert_chinese_pytorch/outputs/terry_rank_output')
#检查是不是知识
check_kg=classify(model_name_or_path='../tdata/albert_check_kg')
# check_pet=classify(model_name_or_path='../tdata/albert-chinese-pytorch-pet')

def run_mark():
    for key,item in kg.get_unmarked():
        print("#################标记数据######")
        # print("本次已经标注：",i)
        print(key)
        if len(item['sentence'])>50:
            continue
        #判断是不是宠物
        # if check_pet(item['sentence'])==0:
        #     continue

        # print("ht知识：",ht0.triple_extraction(sent=item['sentence']))
        ht_kg=ht0.triple_extraction(sent=item['sentence'])
        jiagu_kg = jiagu.knowledge(item['sentence'])
        c_kg=[item['kg']]
        all_kg=ht_kg+jiagu_kg+c_kg
        end_kg=[]
        print("所有知识:",all_kg)
    
        for k in all_kg:
            if k in end_kg:
                continue
            new={
                'sentence':item['sentence'],
                'kg':k
            }
            one(new)
            end_kg.append(k)


    
        # print(knowledge)
        # # print("句子：",s)
        

        # one(item)

def run_text():

    for f in tfile.file_List(path="/mnt/data/dev/github/数据处理工具/tool_data_processing/data/text"):
        t=tfile.open_file(f)
        for s in tt.sentence_segmentation_v1(t):
        # for key,item in kg.get_unmarked():
            print("#################标记数据######")
            # print("本次已经标注：",i)
            # print(key)
            if len(s)>50:
                continue
            #判断是不是宠物
            # if check_pet(item['sentence'])==0:
            #     continue

            # print("ht知识：",ht0.triple_extraction(sent=item['sentence']))
            ht_kg=ht0.triple_extraction(sent=s)
            jiagu_kg = jiagu.knowledge(s)
            # c_kg=[item['kg']]
            all_kg=ht_kg+jiagu_kg
            end_kg=[]
            print("所有知识:",all_kg)

            for k in all_kg:
                if k in end_kg:
                    continue
                new={
                    'sentence':s,
                    'kg':k
                }
                one(new)
                end_kg.append(k)




def run_recheck():
    """
    重新标记之前的数据
    
    """

    for k,item in kg.recheck_all():
        if item.get("state")==None:
            print("###########################################")
            # print(k,item)
            print("-------------------------------------------------------------------")
            tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
            # print(tkg)
        
            s=item['sentence']
            for w in item['kg']:
                s=s.replace(w,"<<█"+w+"█>>")
            print('句子:',s)
            print("知识:",item['kg'])
            p=tclass.pre(tkg)
            p=p+1
            print("手动标记",item['label'])
            if item['label']==p:
                print("Ai判断一致 建议保留")
            else:
                print("Ai判别不一致 请人工判别")
            x = input("输入1(No)或者2(Yes) Ai默认"+str(p)+":")
            # print
            try:
                x= int(x)
            except:
                pass
                x=p
            if x==1:
                print("选择No")
                kg.tdb.delete(k)
            else:
                print("选择Yes")
            data=item
            data["label"]=x
            data['state']='1'
            # key=tt.md5(item["sentence"]+'，'.join(item['kg']))
            kg.mark_sentence(k,data)


run_text()
# run_recheck()
# key="4d72f13470e8dfd82f35db8rerbb4881154"
# print(kg.check_marked(key))