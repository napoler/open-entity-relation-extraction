#encoding=utf-8
from kg_lvdb import KgDatabase
from albert_pytorch import classify
import jiagu
import tkitFile
import tkitText
import tkitNlp

from tkitMarker import *
# import tkitFile
P=Pre()
P.args['conf']="tkitfiles/v0.1/config.json"
P.args['load_path']="tkitfiles/v0.1/pytorch_model.bin"
P.args['vocab']="tkitfiles/v0.1/vocab.txt"
P.args['label_file']="tkitfiles/v0.1/tag.txt"
P.args['max_length']=50
P.setconfig()


TNer=Pre()
TNer.args['conf']="tkitfiles/ner/config.json"
TNer.args['load_path']="tkitfiles/ner/pytorch_model.bin"
TNer.args['vocab']="tkitfiles/ner/vocab.txt"
TNer.args['label_file']="tkitfiles/ner/tag.txt"
TNer.args['albert_path']="tkitfiles/ner"
TNer.args['albert_embedding']=312
TNer.args['rnn_hidden']=400

TNer.model_version='ner'
TNer.args['max_length']=50
TNer.setconfig()

from harvesttext import HarvestText

import pkuseg

from pprint import pprint



import os
LTP_DATA_DIR = '/mnt/data/dev/model/ltp/ltp_data_v3.4.0'  # ltp模型目录的路径
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`

from pyltp import Parser
from pyltp import SementicRoleLabeller
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer



def ner(text):
    """
    """
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型
    words = segmentor.segment(text)  # 分词
    # print ('\t'.join(words))
    segmentor.release()  # 释放模型

    postagger = Postagger() # 初始化实例
    postagger.load(pos_model_path)  # 加载模型

    # words = ['元芳', '你', '怎么', '看']  # 分词结果
    postags = postagger.postag(words)  # 词性标注
    print("##"*30)
    # print ('\t'.join(postags))
    postagger.release()  # 释放模型

    recognizer = NamedEntityRecognizer() # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型
    # words = ['元芳', '你', '怎么', '看']
    # postags = ['nh', 'r', 'r', 'v']
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    recognizer.release()  # 释放模型
    words_list=[]
    for word, flag in zip(words, netags):
        # print(word,flag)
        if flag.startswith("B-"):
            one=[]
            one.append(word)
        elif flag.startswith("I-"):
            one.append(word)
        elif flag.startswith("E-"):
            one.append(word)
            words_list.append("".join(one))
        elif flag.startswith("S-"):
            words_list.append(word)
    # print(words_list)
    # return words_list,words, postags,netags
    return words_list
# text="在中国的任何一个小区里，你都有机会发现流浪猫的身影。"
# print(ner(text))























def one(item): 

    # print(key)
    # 检查知识是否是已经标记的
    key=tt.md5(item["sentence"]+'，'.join(item['kg']))
    if kg.check_marked(key)==True:
        return
    

    # print("--------------------------------------------------------")
    # print("句子：",s)
    # print("知识：",item['kg'])


    # tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
    # p=tclass.pre(tkg)
    # if p==0:
    #     return
    # mark_sentence=item['kg'][0]+"#"+item['kg'][1]+"#"+item['sentence']
    # result=P.pre([mark_sentence])
    # # 
    # print(result)
    # if len(result[0][1])>0:
    #     print("tkitMarker预测:",result[0][1][0])
    #     b=item
    #     b['kg'][2]=result[0][1][0]['words'].replace("[UNK]",'')
    #     print("1或者2",b['kg'])
    #     pass

    # print("3或者4",item['kg'])


    # 忽略掉指代词
    if item['kg'][0] in ["她",'它们','她们','它','我','你','我们','这','他们','牠们','大家','牠','他','人们']:
        return

    #检查知识是否是符合知识规则
    ckg="#u#".join(item['kg'])
    ckg=check_kg.pre(ckg)
    if ckg+1==1:
        return

    print("--------one------------------------------------------------")



    tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
    p=tclass.pre(tkg)

    
    #展现句子
    s=item['sentence']
    for w in item['kg']:
        s=s.replace(w,"<<█"+w+"█>>")
    pprint(item)
    print('句子:',s)
    print('知识:',item['kg'])
    print("Ai判断:",ckg+1)

    data=item
    print("1-2:使用tkitMarker预测 5:进入手动修正")
    x = input("输入1(No)或者2(Yes) 默认1:")
    # print
    try:
        x= int(x)
    except:
        pass
        x=1
    if x==1:
        print("选择No")
        data["label"]=x
    elif x==2:
        print("选择Yes")
        tt.add_words([item['kg'][0]])
        data=item
        data["label"]=x

    elif x==5:
        print("手动修正")
        x = input("描述:")
        data=item
        if len(x) > 0:
            data["label"]=2
            print("手动标记")
            if len(data['kg']) >2:
                data['kg'][2]=x
                pass
            else:
                data['kg'].append(x)
            tt.add_words([item['kg'][0]])
            print("选择Yes")
            key=tt.md5(item["sentence"]+'，'.join(item['kg']))
        else:
            # 无法标记设为拉圾
            data["label"]=1
            # return
    print(data)
    kg.mark_sentence(key,data)

    print("--------oneEnd------------------------------------------------")
    # i=i+1
    # exit()



kg=KgDatabase()
ht0 = HarvestText()
tfile=tkitFile.File()
tt=tkitText.Text()
# tt=tkitText.Text()
tt.load_ht(ht_model="tkitfiles/ht.model")
i=0
tclass=classify(model_name_or_path='tkitfiles/checkkg')
#检查是不是知识
check_kg=classify(model_name_or_path='../tdata/albert_check_kg')
# check_pet=classify(model_name_or_path='../tdata/albert-chinese-pytorch-pet')

def run_mark():
    i=0
    for key,item in kg.get_unmarked():
        print("#################标记数据######")
        # print("本次已经标注：",i)
        print(item)
        s=item['sentence']
        print(key)
        if len(s)>50:
                continue
        # ner_list,vs=get_w_v(s)
        # ner_list=ner(s)+ner_list
        ner_list=ner(s)
        ner_s=tt.named_entity_recognition(s)
        print("提取实体")
        for key in ner_s:
            # print(key)
            ner_list.append(key)
            
        vs=[]
        print('预测成功',i)
        print("句子",s)
        print("实体",ner_list)

        ht_kg=tt.ht.triple_extraction(sent=s)
        # print(ht_kg)
        # ht_kg=ht0.triple_extraction(sent=s)
        # print(ht_kg)
        jiagu_kg = jiagu.knowledge(s)
        # c_kg=[item['kg']]
        all_kg=ht_kg+jiagu_kg
        end_kg=[]
        # print("所有知识:",all_kg)
        
        for k in all_kg:
            if k in end_kg:
                continue
            if k[0] in ner_list and k[1] in vs:
                new={
                    'sentence':s,
                    'kg':k
                }
                if  k[0] in ner_list:
                    one(new)
                    end_kg.append(k)

        if item['kg'][0] in ner_list:
            one(item)

def run_mark_pred():
    """
    对自动标记的数据进行筛查
    """
    i=0
    for key,item in kg.get_unmarked_auto_sentence():
        print("#################标记数据######")
        print(item)
        one(item)
        kg.tdb.load("kg_auto_sentence")
        kg.tdb.delete(key)
def get_w_v(text):
  seg = pkuseg.pkuseg(postag=True)           # 以默认配置加载模型
  text = seg.cut(text)  # 进行分词
  w=''
  ws=[]
  v=''
  vs=[]

  for it,p in text:
    if p.startswith("n"):
      # print(it)
      w=w+it
      
    else:
      # print(w)
      if len(w)>0:
        ws.append(w)
      w=''
      #动词
    if p.startswith("v"):
      # print(it)
    #   v=v+it
        vs.append(it)

    # else:
    #   # print(w)
    #   if len(v)>0:
    #     vs.append(v)
    #   v='' 
#   print(ws)
#   print(vs)
  return ws,vs
# print(get_w_v(text))

def ner_plus(text):
    ner_list=ner(text)
    ner_s=tt.named_entity_recognition(text)

    words = jiagu.seg(text) # 分词
    # print(words)

    # pos = jiagu.pos(words) # 词性标注
    # print(pos)

    # ner_jiagu = jiagu.ner(words) # 命名实体识别
    # print(ner_jiagu)
    # ner_list=[]
    # print("提取实体")
    for key in ner_s:
        # print(key)
        if key in ner_list:
            pass
        else:
            ner_list.append(key)
    
    # for key in ner_jiagu:
    #     # print(key)
    #     if key in ner_list:
    #         pass
    #     else:
    #         ner_list.append(key)
    return ner_list
def pre_kg(text):
    """
    自动预测补全信息
    只提取知识
    """
    ner_list=ner_plus(text)

    kgs=[] #返回提取的知识列表
    for n in ner_list:
        vs=get_Relationship(text,n)
        # print("动词",n,vs)
        for v in vs:
            item={
                'sentence':text,
                'kg':[n,v]
            }
            s=item['sentence']
            mark_sentence=item['kg'][0]+"#"+item['kg'][1]+"#"+item['sentence']
            result=P.pre([mark_sentence])
            # 
            if len(result[0][1])>0:
                # print("tkitMarker预测:",result[0][1][0])
                item['kg'].append(result[0][1][0]['words'].replace("[UNK]",''))
                # print(result)
                # print(item['kg'])
                
                #添加kg
                kgs.append(item['kg'])

                # if item['kg'][0]==item['kg'][2]:
                #     key=tt.md5(item["sentence"]+'，'.join(item['kg']))
                #     data=item
                #     data["label"]=1
                #     print("保存为数据",key,data)
                #     kg.mark_sentence(key,data)
                #     # return
                #     kgs.append(item['kg'])
                #     continue
                
                # key=tt.md5(item["sentence"]+'，'.join(item['kg']))
                # if kg.check_marked(key)==True:
                #     # print("已经标记")
                #     kgs.append(item['kg'])
                #     # return
                #     continue    
                # else:
                #     pass
                # print("--------------------------------------------------------")
                # tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
                # p=tclass.pre(tkg)
                # ckg="#u#".join(item['kg'])
                # ckg=check_kg.pre(ckg)

                # if ckg+1==1:
                #     # return
                #     kgs.append(item['kg'])
                #     continue
            #     print("Ai判断:",ckg+1)

            #     print("1-2:使用tkitMarker预测 输入3进入手动编辑模式")
            #     x = input("输入1(No)或者2(Yes) 默认1:")
            #     # print
            #     try:
            #         x= int(x)
            #     except:
            #         pass
            #         x=1
            #     if x==1:
            #         print("选择No")

                    
            #         data=item
            #         data["label"]=x
            #     elif x==2:
            #         print("选择Yes")
            #         tt.add_words([item['kg'][0]])
            #         data=item
            #         data["label"]=x
            #     elif x==3:
            #         print("手动修正")
            #         x = input("描述:")
            #         data=item
            #         if len(x) > 0:
            #             data["label"]=2
            #             print("手动标记")
            #             if len(data['kg']) >2:
            #                 data['kg'][2]=x
            #                 pass
            #             else:
            #                 data['kg'].append(x)
            #             tt.add_words([item['kg'][0]])
            #             print("选择Yes")
            #             key=tt.md5(item["sentence"]+'，'.join(item['kg']))
            #         else:
            #             # 无法标记设为拉圾
            #             data["label"]=1
            #             # return
        
            # else:
            #     data=item
            #     data["label"]=1
            #     # print("--------------------------------------------------------")
            #     # print(s)
            #     # print(item['kg'])

            #     # print("没有预测结果请手动输入")
            #     # x = input("描述:")
            #     # data=item
            #     # if len(x) > 0:
            #     #     data["label"]=2
            #     #     print("手动标记")
            #     #     print("选择Yes")
            #     #     key=tt.md5(item["sentence"]+'，'.join(item['kg']))
            #     # else:
            #     #     # 无法标记设为拉圾
            #     #     data["label"]=1
            #     #     # return


        

            # print("保存为数据",key,data)
            # kg.mark_sentence(key,data)
            # key=tt.md5(item["sentence"])
            # kg.mark_sentence(key,data)
                # i=i+1
                # exit()
    return kgs


def auto_text_pre(path="/mnt/data/dev/github/数据处理工具/tool_data_processing/data/text"):
    """
    使用模型推断描述 来标记数据
    """
    i=0
    for f in tfile.file_List(path):
        t=tfile.open_file(f)
        for s in tt.sentence_segmentation_v1(t):
        # for key,item in kg.get_unmarked():

            # 检查句子是否是标记过的
            key=tt.md5(s)
            if kg.check_marked(key)==True:
                print("已经标记句子")
                continue

            print(i,"#################标记数据######")

            kgs=pre_kg(s)
            print('pre的Kgs',kgs)


            #判断是不是宠物
            # if check_pet(item['sentence'])==0:
            #     continue

            # print("ht知识：",ht0.triple_extraction(sent=item['sentence']))
            ht_kg=tt.ht.triple_extraction(sent=s)
            # print(ht_kg)
            # ht_kg=ht0.triple_extraction(sent=s)
            # print(ht_kg)
            jiagu_kg = jiagu.knowledge(s)
            # c_kg=[item['kg']]
            all_kg=ht_kg+jiagu_kg
            all_kg=ht_kg
            # end_kg=[]
            # print("所有知识:",all_kg)
            ner_list=ner_plus(s)
            for k in all_kg:

                if k in kgs or k[0] not in ner_list:
                    continue
                    
                new={
                    'sentence':s,
                    'kg':k
                }
                i=i+1
                #自动提取知识
                key=tt.md5(new['sentence']+",".join(new['kg']))
                kg.auto_sentence(key,new)
                print('自动提取',i,new)


            #     one(new)
            #     kgs.append(k)
            # print('本次已经标记的Kgs',kgs)

            #将标记过的句子记录下
            key=tt.md5(s)
            data={'sentence':s,'kg':[]} 
            kg.mark_sentence(key,data)


def run_text(path="/mnt/data/dev/github/数据处理工具/tool_data_processing/data/text"):

    for f in tfile.file_List(path):
        t=tfile.open_file(f)
        for s in tt.sentence_segmentation_v1(t):
        # for key,item in kg.get_unmarked():
            print("#################标记数据######")
            # print("本次已经标注：",i)
            # print(key)
            if len(s)>50:
                continue
            ner_list,vs=get_w_v(s)
            ner_list=ner(s)+ner_list
            print("实体",ner_list)
            #判断是不是宠物
            # if check_pet(item['sentence'])==0:
            #     continue
         

            # print("ht知识：",ht0.triple_extraction(sent=item['sentence']))
            # tt.ht.triple_extraction(sent=sentence)
            ht_kg=tt.ht.triple_extraction(sent=s)
            jiagu_kg = jiagu.knowledge(s)
            # c_kg=[item['kg']]
            all_kg=ht_kg+jiagu_kg
            end_kg=[]
            # print("所有知识:",all_kg)
         
            for k in all_kg:
                if k in end_kg:
                    continue
                if k[0] in ner_list and k[1] in vs:
                    new={
                        'sentence':s,
                        'kg':k
                    }
                    one(new)
                    end_kg.append(k)


def get_Relationship(text,ner):
    """
    获取关系词
    """
    pre_re=ner+"#"+text
    result=TNer.pre([pre_re])
    # print("预测的关系词::",result)
    words_list=[]
    for item in result[0][1]:
        if item['type']=="关系" and item['type'] not in words_list:
            words_list.append(item['words'])
    return words_list
             

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


print("""
1:自动标记文本 进行初步筛选
2:开始手动标记 对自动标记的数据进行筛查


""")
x = input("输入你要执行的命令:")
x=int(x)
if x==1:
    auto_text_pre()
elif x==2:
    print("运行2")
    run_mark_pred()

# run_mark()
# run_text()
# run_text_pre()
# run_text_pre()
# run_recheck()
# key="4d72f13470e8dfd82f35db8rerbb4881154"
# print(kg.check_marked(key))