#encoding=utf-8
from kg_lvdb import KgDatabase
from albert_pytorch import classify
import jiagu
import tkitFile
import tkitText
import tkitNlp

from tkitMarker import *
# import tkitFile
# P=Pre()
# P.args['conf']="tkitfiles/v0.1/config.json"
# P.args['load_path']="tkitfiles/v0.1/pytorch_model.bin"
# P.args['vocab']="tkitfiles/v0.1/vocab.txt"
# P.args['label_file']="tkitfiles/v0.1/tag.txt"
# P.setconfig()


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
    key=tt.md5(item["sentence"]+'，'.join(item['kg']))
    # print(key)
    if kg.check_marked(key)==True:
        print("已经标记")
        return
    else:
        pass
    s=item['sentence']
    for w in item['kg']:
        s=s.replace(w,"<<█"+w+"█>>")
    # print("--------------------------------------------------------")
    # print("句子：",s)
    # print("知识：",item['kg'])


    # tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
    # p=tclass.pre(tkg)
    # if p==0:
    #     return
    mark_sentence=item['kg'][0]+"#"+item['kg'][1]+"#"+item['sentence']
    result=P.pre([mark_sentence])
    # 
    if len(result[0][1])>0:
        print("tkitMarker预测:",result[0][1][0])
        pass
    print(result)
    print(item['kg'])

    print("--------------------------------------------------------")
    print("1-2:使用tkitMarker预测,3-4:使用提取的知识")
    x = input("输入1(No)或者2(Yes) 默认1:")
    # print
    try:
        x= int(x)
    except:
        pass
        x=1
    if x==1:
        print("选择No")
        if len(result[0][1])>0:
           item['kg'][2]=result[0][1][0]['words'].replace("[UNK]",'')
        data=item
        data["label"]=x
    elif x==2:
        print("选择Yes")
        if len(result[0][1])>0:
           item['kg'][2]=result[0][1][0]['words'].replace("[UNK]",'')
        data=item
        data["label"]=x

    elif x==3:
        print("选择No")

        data=item
        data["label"]=x-2
    elif x==4:
        print("选择Yes")
        data=item
        data["label"]=x-2
    print(data)
    kg.mark_sentence(key,data)
    # i=i+1
    # exit()










# def one(item): 
#     key=tt.md5(item["sentence"]+'，'.join(item['kg']))
#     # print(key)
#     if kg.check_marked(key)==True:
#         # print("已经标记")
#         return
#     else:
#         pass
#     s=item['sentence']
#     for w in item['kg']:
#         s=s.replace(w,"<<█"+w+"█>>")
#     # print("--------------------------------------------------------")
#     # print("句子：",s)
#     # print("知识：",item['kg'])
#     mark_sentence=item['kg'][0]+"#"+item['kg'][1]+"#"+item['sentence']
#     result=P.pre([mark_sentence])
#     # 
#     if len(result[0][1])>0:
#         print(result)
#         print("tkitMarker预测:",result[0][1])
#         print("--------------------------------------------------------")
#     # # print( tclass.pre(item['sentence']))
#     # tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
#     # p=tclass.pre(tkg)
#     # ckg="#u#".join(item['kg'])
#     # ckg=check_kg.pre(ckg)
#     # print("判断是不是知识",ckg+1)
#     # # print()
#     # # print(p+1)
#     # if int(p)==0:
#     #     print("Ai预测：No(1)")
#     #     pass
#     # elif int(p)==1 and int(ckg)==1:
#     #     print("Ai预测：Yes(2)")
#     #     if item['kg'][1] in ["负责管辖",'生于','位于']:
#     #         x=2
#     #     else:
#     #         # print("输入1(No)或者2(Yes)")
#     #         x = input("输入1(No)或者2(Yes) 默认1:")
#     #     # print
#     #     try:
#     #         x= int(x)
#     #     except:
#     #         pass
#     #         x=1
#     #     if x==1:
#     #         print("选择No")
#     #     else:
#     #         print("选择Yes")
#     #     data=item
#     #     data["label"]=x
     
#     #     kg.mark_sentence(key,data)
#     #     # i=i+1
#     #     # exit()
#     # else:
#     #     print("Ai预测：No(1)")
#     #     if item['kg'][1] in ["负责管辖",'生于','位于']:
#     #         x=2
#     #     else:
#     #         # print("输入1(No)或者2(Yes)")
#     #         x = input("输入1(No)或者2(Yes) 默认1:")
#     #     # print
#     #     try:
#     #         x= int(x)
#     #     except:
#     #         pass
#     #         x=1
#     #     if x==1:
#     #         print("选择No")
#     #     else:
#     #         print("选择Yes")
#     #     data=item
#     #     data["label"]=x
#     #     kg.mark_sentence(key,data)
#     #     # i=i+1
#     #     # exit()



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
        # print("所有知识:",all_kg)
    
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
def get_w_v(text):
  seg = pkuseg.pkuseg(postag=True)           # 以默认配置加载模型
  text = seg.cut(text)  # 进行分词
#   print(text)
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


def pre_kg(item):
    # print(item['kg'])
    key=tt.md5(item["sentence"]+'，'.join(item['kg']))
    # print(key)
    if kg.check_marked(key)==True:
        print("已经标记")
        return
    else:
        pass
    s=item['sentence']
    for w in item['kg']:
        s=s.replace(w,"<<█"+w+"█>>")
    # print("--------------------------------------------------------")
    # print("句子：",s)
    # print("知识：",item['kg'])


    # tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
    # p=tclass.pre(tkg)
    # if p==0:
    #     return
    mark_sentence=item['kg'][0]+"#"+item['kg'][1]+"#"+item['sentence']
    result=P.pre([mark_sentence])
    # 
    if len(result[0][1])>0:
        print("tkitMarker预测:",result[0][1][0])
        item['kg'].append(result[0][1][0]['words'].replace("[UNK]",''))
        print(result)
        print(item['kg'])

        print("--------------------------------------------------------")
        print("1-2:使用tkitMarker预测")
        x = input("输入1(No)或者2(Yes) 默认1:")
        # print
        try:
            x= int(x)
        except:
            pass
            x=1
        if x==1:
            print("选择No")

            
            data=item
            data["label"]=x
        elif x==2:
            print("选择Yes")
            data=item
            data["label"]=x
   
    else:
        print("--------------------------------------------------------")
        print(s)
        print(item['kg'])

        print("没有预测结果请手动输入")
        x = input("描述:")
        data=item
        if len(x) > 0:
            data["label"]=1
            print("手动标记")
        else:
            return


    print(data)
    key=tt.md5(item["sentence"]+'，'.join(item['kg']))
    kg.mark_sentence(key,data)
        # i=i+1
        # exit()



def run_text_pre():
    """
    使用模型推断描述 来标记数据
    """
    i=0
    for f in tfile.file_List(path="/mnt/data/dev/github/数据处理工具/tool_data_processing/data/text"):
        t=tfile.open_file(f)
        for s in tt.sentence_segmentation_v1(t):
        # for key,item in kg.get_unmarked():
            print("#################标记数据######")
            # print("本次已经标注：",i)
            # print(key)
            if len(s)>50:
                continue
            ner_list,vs=get_w_v(s)
            # ner_list=ner(s)+ner_list
            ner_list=ner(s)
            
            result=TNer.pre([s])
            print('标记ner和关系词',result)
            if len(result[0][1])>0:
                i=i+1
            print('预测成功',i)
            print("句子",s)
            print("实体",ner_list)
            print("动词",vs)
            for n in ner_list:
                for v in vs:
                    new={
                        'sentence':s,
                        'kg':[n,v]
                    }
                    # print(new)
                    # pre_kg(new)


            #判断是不是宠物
            # if check_pet(item['sentence'])==0:
            #     continue

            # # print("ht知识：",ht0.triple_extraction(sent=item['sentence']))
            # ht_kg=ht0.triple_extraction(sent=s)
            # jiagu_kg = jiagu.knowledge(s)
            # # c_kg=[item['kg']]
            # all_kg=ht_kg+jiagu_kg
            # end_kg=[]
            # # print("所有知识:",all_kg)
         
            # for k in all_kg:
            #     if k in end_kg:
            #         continue
            #     if k[0] in ner_list and k[1] in vs:
            #         new={
            #             'sentence':s,
            #             'kg':k
            #         }
            #         one(new)
            #         end_kg.append(k)





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
            ner_list,vs=get_w_v(s)
            ner_list=ner(s)+ner_list
            print("实体",ner_list)
            #判断是不是宠物
            # if check_pet(item['sentence'])==0:
            #     continue

            # print("ht知识：",ht0.triple_extraction(sent=item['sentence']))
            ht_kg=ht0.triple_extraction(sent=s)
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

# run_mark()
# run_text()

run_text_pre()
# run_recheck()
# key="4d72f13470e8dfd82f35db8rerbb4881154"
# print(kg.check_marked(key))