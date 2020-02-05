#encoding=utf-8
from kg_lvdb import KgDatabase

import jiagu
import tkitFile
import tkitText
import tkitNlp
# import tkitDb
import tkitSearch
import gc
from cocoNLP.extractor import extractor


ex = extractor()
from harvesttext import HarvestText

import pkuseg

from pprint import pprint

from memory_profiler import profile

from config import *








kg=KgDatabase()
# ht0 = HarvestText()
tfile=tkitFile.File()

# tt=tkitText.Text()
# tt.load_ht(ht_model="tkitfiles/ht.model")


# tt.typed_words(ht_model="tkitfiles/ht.model")
i=0












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



def get_key(data):
    tt=tkitText.Text()
    key=tt.md5(data["sentence"]+'，'.join(data['kg']))
    return key

    
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



















#自动处理标记单条数据
def auto_one(item): 
    tt=tkitText.Text()
    
    # print(key)
    # 检查知识是否是已经标记的
    # key=tt.md5(item["sentence"]+'，'.join(item['kg']))
    key=get_key(item)
    if kg.check_marked(key)==True:
        return True

    # 忽略掉指代词
    if item['kg'][0] in ["她",'它们','她们','它','我','你','我们','这','他们','牠们','大家','牠','他','人们']:
        data=item
        data["label"]=1
        data['state']='1'
        kg.mark_sentence(key,data)
        return True

    if item['kg'][0] ==item['kg'][2]:
        data=item
        data["label"]=1
        data['state']='1'
        kg.mark_sentence(key,data)
        return True

    #检查知识是否是符合知识规则
    ckg="#u#".join(item['kg'])
    ckg=Check_kg.pre(ckg)
    Check_kg.release()
    if ckg+1==1:
        data=item
        data["label"]=1
        # data['state']='1'
        kg.mark_sentence(key,data)
        return True
    print("--------one------------------------------------------------")
    print("原始知识",item)
    
    for i,kg_word in enumerate(item['kg']):
    # if len(item['kg'])>2:
        #自动搜索最大匹配单词
        # tt=tkitText.Text()

        #暂时屏蔽自动修正知识
        if i>2:
            try:
                c,r=tt.find_match(item['sentence'],item['kg'][i])
                if r >50:
                    item['kg'][i]=c
                    print("自动修正知识",c)
            except:
                pass
    #展现句子
    s=item['sentence']
    for w in item['kg']:
        s=s.replace(w,"<<█"+w+"█>>")
    pprint(item)
    print("~~~~~"*10)
    print('句子:',s)
    print("~~~~~"*1)
    # times = ex.extract_time(item['sentence'])
    # print("时间",times)
    print("~~~~~"*3)
    print('知识:',item['kg'])
    print("~~~~~"*3)
    #检查是否是合理的知识
    # tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
    # p=Tclass.pre(tkg)
    p = Tclass.pre(item['sentence'],",".join(item['kg']))
    softmax=Tclass.softmax()
    Tclass.release()
    print("------------------")
    print("分类","|",'概率')
    for ck,rank in zip([1,2],softmax):
        print(ck,"|",rank)
        if ck == 1 and rank >=0.8:
            data=item
            data["label"]=1
            data['state']='1'
            kg.mark_sentence(key,data)
            print("分值过低自动设为不合理")
            return True
        elif ck == 2 and rank >=0.8:
            data=item
            data["label"]=2
            data['state']='1'
            kg.mark_sentence(key,data)
            print("自动设为合理")
            return   True      
        else:
            print("不确定进入手动待选")
    print("保存")
    data=item
    data["label"]=0
    # data['state']='0'
    kg.mark_sentence(key,data)
    print("------------------")


    print("--------oneEnd------------------------------------------------")
    # i=i+1
    # exit()





#处理标记单条数据
def one(item): 
    tt=tkitText.Text()
    # print(key)
    # 检查知识是否是已经标记的
    key=get_key(item)
    if kg.check_marked(key)==True:
        return
    

    # print("--------------------------------------------------------")
    # print("句子：",s)
    # print("知识：",item['kg'])


    # tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
    # p=Tclass.pre(tkg)
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
        data=item
        data["label"]=1
        data['state']='1'
        kg.mark_sentence(key,data)
        return

    if item['kg'][0] ==item['kg'][2]:
        data=item
        data["label"]=1
        data['state']='1'
        kg.mark_sentence(key,data)
        return

    #检查知识是否是符合知识规则
    ckg="#u#".join(item['kg'])
    ckg=Check_kg.pre(ckg)
    Check_kg.release()
    if ckg+1==1:
        data=item
        data["label"]=1
        kg.mark_sentence(key,data)
        return

    print("--------one------------------------------------------------")


    print("原始知识",item)
    
    for i,kg_word in enumerate(item['kg']):
    # if len(item['kg'])>2:
        #自动搜索最大匹配单词
        # tt=tkitText.Text()

        #暂时屏蔽自动修正知识
        if i>2:
            try:
                c,r=tt.find_match(item['sentence'],item['kg'][i])
                if r >50:
                    item['kg'][i]=c
                    print("自动修正知识",c)
            except:
                pass
    #展现句子
    s=item['sentence']
    for w in item['kg']:
        s=s.replace(w,"<<█"+w+"█>>")
    pprint(item)
    print("~~~~~"*10)
    print('句子:',s)
    print("~~~~~"*1)
    # times = ex.extract_time(item['sentence'])
    # print("时间",times)
    try:
        locations = ex.extract_locations(item['sentence'])
        print("地点",locations)
        name = ex.extract_name(item['sentence'])
        print("人名",name)
    except:
        pass
    print("~~~~~"*1)
    print("~~~~~"*3)
    print('知识:',item['kg'])
    print("~~~~~"*3)

    #检查是否是合理的知识
    # tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
    # p=Tclass.pre(tkg)
    p = Tclass.pre(item['sentence'],",".join(item['kg']))
    softmax=Tclass.softmax()
    Tclass.release()
    print("分类","|",'概率')
    for ck,rank in zip([1,2],softmax):
        print(ck,"|",rank)
        if ck == 1 and rank >=0.85:
            data=item
            data["label"]=1
            data['state']='1'
            kg.mark_sentence(key,data)
            print("分值过低自动设为不合理")
            return
        elif ck == 2 and rank >=0.85:
            data=item
            data["label"]=2
            data['state']='1'
            kg.mark_sentence(key,data)
            print("自动设为合理")
            return           
    print("------------")

    # print(ck,round(rank, 5) )
    print("Ai判断(提取匹配):",p+1)   
    print("Ai判断(kg合理度):",ckg+1)

    data=item
    print("~~~~~"*10)
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
        data['state']='2'
    elif x==2:
        print("选择Yes")
        tt.add_words([item['kg'][0]],ht_model="tkitfiles/ht.model")
        data=item
        data["label"]=x
        data['state']='2'

    elif x==5:
        print("手动修正")
        x = input("实体:")
        data=item
        if len(x) > 0:
            data["label"]=2
            data['kg'][0]=x
            data['state']='2'
        print("实体",data['kg'][0])
        x = input("关系:")
        data=item
        if len(x) > 0:
            data["label"]=2
            data['kg'][1]=x
            data['state']='2'
        print("关系",data['kg'][1])
        x = input("描述:")
        if len(x) > 0:
            data["label"]=2
            data['state']='2'
            print("手动标记")
            if len(data['kg']) >2:
                data['kg'][2]=x
                pass
            else:
                data['kg'].append(x)
            print("描述",data['kg'][2])
            tt.add_words([item['kg'][0]],ht_model="tkitfiles/ht.model")
            print("选择Yes")
            key=get_key(item)
        else:
            # 无法标记设为拉圾
            data["label"]=1
            # return
    print(data)
    try:
        kg.mark_sentence(key,data)
    except:
        pass

    print("--------oneEnd------------------------------------------------")
    # i=i+1
    # exit()




def run_mark():
    tt=tkitText.Text()
    tt.load_ht()
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
        print("")
        print("")
        print("")
        print("")
        print("")
        print(i,"#################标记数据######")
        i=i+1
        # print(item)
        one(item)
        kg.tdb.load("kg_auto_sentence")
        kg.tdb.delete(key)

def auto_run_mark_pred():
    """
    对自动标记的数据进行筛查
    """
    i=0
    for key,item in kg.get_unmarked_auto_sentence():
        print("\n"*2)

        print(i,"#################标记数据######")
        
        # print(item)
        #运行自动标注
        run_re=auto_one(item)
        if run_re==True:
            kg.tdb.load("kg_auto_sentence")
            kg.tdb.delete(key)
            i=i+1
            print("标注成功",i)

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
    # result=[]
    # ner_list=ner(text)
    # ner_s=tt.named_entity_recognition(text)
    # ws,vs=get_w_v(text)
    


    # try:
    #     times = ex.extract_time(text)
    #     print("时间",times)
    #     locations = ex.extract_locations(text)
    #     print("地点",locations)
    #     name = ex.extract_name(text)
    #     print("人名",name)
    #     if locations!=None:
            
    #         ner_list=ner_list+locations
    #     if name!=None and type(name)==str:
    #         ner_s=ner_list+[name]
    #     if type(name)==list:
    #         ner_s=ner_list+name

    #     if times!=None:
    #         try:
    #             ner_list=ner_list+times
    #         except:
    #             pass
    # except:
    #     pass
    # # words = jiagu.seg(text) # 分词
    # # print(words)

    # # pos = jiagu.pos(words) # 词性标注
    # # print(pos)

    # # ner_jiagu = jiagu.ner(words) # 命名实体识别
    # # print(ner_jiagu)
    # # ner_list=[]
    # # print("提取实体")
    # for key in ner_s:
    #     ner_list.append(key)
    # # print(ner_s.keys())
    # # ner_list=ner_list+ ws
    # ner_list=ner_list
    # # for key in ner_list:
    # #     result.append(key)
    # return list(set(ner_list))

 
    result=[]
    ner_result=Ner.pre([text])
    for ner in ner_result[0][1]:
        result.append(ner['words'])
        
    return result
def pre_kg_clear(text):
    """
    自动预测补全信息
    只提取知识
    """

    tt=tkitText.Text()
    # tt.load_ht()


    print("句子",text)
    ner_list=ner_plus(text)

    #基于已存在的词典获取关系词
    # terry_er=TEntityRel()
    entity_words,rel=Terry_er.get_entity_rel(text)
    # del terry_er
    # gc.collect()
    print("基于词典抽取关系词",rel)

    kgs=[] #返回提取的知识列表
    print('ner_list',ner_list)
    for n in ner_list:
        vs=get_Relationship(text,n)
        print('Ai预测关系词',n,vs)
        vs=rel+vs #累加如关系词
        vs=list(set(vs))
        
        print("关系词",n,vs)
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

    all_kg=kgs
    new_kg=[]
    for item in all_kg:
        for i,kg_word in enumerate( item):
        # if len(item['kg'])>2:
            #自动搜索最大匹配单词
            # tt=tkitText.Text()

            #暂时屏蔽自动修正知识
            if i>2:
                try:
                    c,r=tt.find_match(text,kg_word)
                    if r >50:
                        item[i]=c
                        print("自动修正知识",c)
                except:
                    pass
        new_kg.append(item)

    new_kg_re=[]
    for it in new_kg:
        if it not in new_kg_re:
            new_kg_re.append(it)
        # print(b) 
    return new_kg_re
#@profile
def pre_kg(text):
    """
    自动预测补全信息
    只提取知识
    """

    tt=tkitText.Text()
    # tt.load_ht()


    print("句子",text)
    ner_list=ner_plus(text)


    entity_words,rel=terry_er.get_entity_rel(text)
    # terry_er.release() 
    # del terry_er
    gc.collect()
    print("基于词典抽取关系词",rel)

    kgs=[] #返回提取的知识列表
    for n in ner_list:
        vs=get_Relationship(text,n)
        print('Ai预测关系词',vs)
        vs=rel+vs #累加如关系词
        vs=list(set(vs))
        
        print("关系词",n,vs)
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
    # tt.load_ht()
    # ht_kg=HT.triple_extraction(sent=text)
    # tt.release()
    # del ht_kg
    # del tt
    # gc.collect()
    # jiagu_kg = jiagu.knowledge(text)
    # all_kg=ht_kg+kgs
    # all_kg=ht_kg+jiagu_kg+kgs
    # all_kg=jiagu_kg+kgs
    # tt.ht=None

    # tt=tkitText.Text()
    # all_kg=ht_kg+kgs
    all_kg=kgs
    new_kg=[]
    for item in all_kg:
        for i,kg_word in enumerate( item):
        # if len(item['kg'])>2:
            #自动搜索最大匹配单词
            # tt=tkitText.Text()

            #暂时屏蔽自动修正知识
            if i>2:
                try:
                    c,r=tt.find_match(text,kg_word)
                    if r >50:
                        item[i]=c
                        print("自动修正知识",c)
                except:
                    pass
        new_kg.append(item)
    # all_kg=kgs 
    # new_kg=list(set(new_kg)) 
    # del jiagu
    # gc.collect()
    # del ht_kg
    # del jiagu_kg
    # del tt.ht
    # gc.collect()
    del all_kg
    gc.collect()
    new_kg_re=[]
    for it in new_kg:
        if it not in new_kg_re:
            new_kg_re.append(it)
        # print(b) 
    return new_kg_re

#自动分析文本 预先预测出可能的知识
def auto_text_pre(path="/mnt/data/dev/github/数据处理工具/tool_data_processing/data/text"):
    """
    使用模型推断描述 来标记数据
    """
    tt=tkitText.Text()
    i=0
    auto_i=0
    for f in tfile.file_List(path):
        print("file",f)
        t=tfile.open_file(f)
        for s in tt.sentence_segmentation_v1(t):
        # for key,item in kg.get_unmarked():
            #替换掉中文标点
            s=tt.filterPunctuation(s)

            # 检查句子是否是标记过的
            key=tt.md5(s)
            if kg.check_marked(key)==True:
                print("已经标记句子")
                continue
            print("\n\n\n\n")
            print("发现数据:",i,"auto成功的数据:",auto_i,"#################标记数据######")

            # 使用多种方案获取知识
            try:
                kgs=pre_kg(s)
            except:
                continue
            # ht_kg=tt.ht.triple_extraction(sent=s)
            # jiagu_kg = jiagu.knowledge(s)
            # all_kg=ht_kg+jiagu_kg+kgs
            all_kg=kgs
            ner_list=ner_plus(s)
            for k in all_kg:
                # 限制只提取实体
                # if k in kgs or k[0] not in ner_list:
                #     continue
                if  k[0] not in ner_list:
                    continue
                # print("\n\n")
                # #检查是否是合理的知识
                # tkg="[kg] "+",".join(k)+" [/kg] "+s
                # print(tkg)
                # p=Tclass.pre(tkg)
                # softmax=Tclass.softmax()
                # print('分类','得分')
                # for ck,rank in zip([1,2],softmax):
                #     print(ck,rank)
                new={
                    'sentence':s,
                    'kg':k
                }
                i=i+1
                #自动提取知识
                key=get_key(new)
                kg.auto_sentence(key,new)
                print('自动提取',i,new)

                #运行自动标注
                run_re=auto_one(new)
                if run_re==True:
                    # kg.tdb.load("kg_auto_sentence")
                    DB.kg_auto_sentence.delete_one({"_id":key})
                    # kg.tdb.delete(key)
                    auto_i=auto_i+1
                # if  softmax[0] >=0.5:
                #     print("分值过低 忽略")
                #     continue
                # else:
                #     new={
                #         'sentence':s,
                #         'kg':k
                #     }
                #     i=i+1
                #     #自动提取知识
                #     key=tt.md5(new['sentence']+",".join(new['kg']))
                #     kg.auto_sentence(key,new)
                #     print('自动提取',i,new)

                #     #运行自动标注
                #     run_re=auto_one(new)
                #     if run_re==True:
                #         kg.tdb.load("kg_auto_sentence")
                #         kg.tdb.delete(key)
                #         auto_i=auto_i+1

                #     continue

            #将标记过的句子记录下
            key=tt.md5(s)
            data={'sentence':s,'kg':[]} 
            kg.mark_sentence(key,data)


def run_text(path="/mnt/data/dev/github/数据处理工具/tool_data_processing/data/text"):
    tt=tkitText.Text()
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
        if item['type']=="关系":
            words_list.append(item['words'])
    return list(set(words_list))
             
def statistics():
    """
    统计数据
    """
    tt=tkitText.Text()
    i_m=0
    kg_none=0
    state_1=0
    state_2=0
    state_2_2=0
    other=0
    check=0
    checked=0
    for k,item in kg.recheck_all():
        i_m=i_m+1
        if item.get('kg')==None or len(item.get('kg'))==0:
            kg_none=kg_none+1
        elif  item.get('kg')!=None and item.get('state')=='1':
            state_1=state_1+1
        elif item.get('kg')!=None and item.get('state')=='2':
            state_2=state_2+1
            if item['label']=='2' or item['label']==2:
                state_2_2=state_2_2+1

        else:
            other=other+1
        if  item.get('check')==None and item.get('state')=='2' and  item['label']==2:
            check=check+1
        elif  item.get('state')=='2':
            checked=checked+1



    print("++++++++统计数据++++++++++++")
    print('kg_none',kg_none)
    print("state_1",state_1)
    print("state_2",state_2)
    print("state_2_2",state_2_2)
    print("other",other)
    print("i_m",i_m)
    print("check",check)
    print("checked",checked)




def auto_run_recheck():
    """
    自动重新标记之前的数据
    
    """
    i_m=0
    for k,item in kg.recheck_all():
        i_m=i_m+1
        
        if item.get("state")==None or item.get("state")=='1':
            if item.get('kg')==None:
                pass
            elif len(item.get('kg'))==0:
                item['state']='3'
                kg.mark_sentence(k,item)
                continue
            try:
                auto_one(item)
            except:
                pass
            print("已标记:",i_m)
            item['state']='1'
            # key=tt.md5(item["sentence"]+'，'.join(item['kg']))
            kg.mark_sentence(k,item)
            print(item)
def run_recheck(label=2,state='1',check_type=0):
    """
    重新标记之前的数据
    这里进行手动检查
    check_type=0 标记所有
    check_type=1 只筛选标记和预测不一样的数据 并且自动跳过
    check_type=2 只筛选标记和预测不一样的数据  不自动跳过

    state='1' 0 不确定数据状态 1 自动筛选机率较高 2 最终状态
    
    """
    tt=tkitText.Text()
    i_m=0
    print("""请输入概率阀值(0-1)""")
    limit = float(input("阀值:"))
    if 0<limit <1:
        print("阀值错误 退出")
    else:
        limit=0.95
    for k,item in kg.recheck_all():
        if (item.get("state")==None  and item.get("label")==label) or (item.get("state")==state and item.get("label")==label):
        # if item.get("state")==None or item.get("state")==1:
            if item.get('kg')==None:
                item['state']='3'
                kg.mark_sentence(k,item)
                continue
                pass
            elif len(item.get('kg'))==0:
                item['state']='3'
                kg.mark_sentence(k,item)
                continue
          
            print("\n"*3)
            print("已标记:",i_m)
            #自动修正知识
            for i,kg_word in enumerate( item['kg']):
            # if len(item['kg'])>2:
                #自动搜索最大匹配单词
                # tt=tkitText.Text()

                #暂时屏蔽自动修正知识
                if i>2:
                    try:
                        c,r=tt.find_match(item['sentence'],item['kg'][i])
                        if r >50:
                            item['kg'][i]=c
                            print("自动修正知识",c)
                    except:
                        pass
            print("###########################################")
            print(k,item)
            print("-------------------------------------------------------------------")

            #检查是否是合理的知识
            # tkg="[kg] "+",".join(item['kg'])+" [/kg] "+item['sentence']
            # p=Tclass.pre(tkg)
            p = Tclass.pre(item['sentence'],",".join(item['kg']))
            softmax=Tclass.softmax()
            Tclass.release()
            print("分类","|",'概率')
            for ck,rank in zip([1,2],softmax):
                print(ck,"|",rank)


            s=item['sentence']
            for w in item['kg']:
                s=s.replace(w,"<<█"+w+"█>>")

            # p=Tclass.pre(tkg)
            p=p+1
            print('句子:',s)
            print("知识:",item['kg'])
            print("原来标记label:",item['label'])
            print("Ai标记label:",p)
            if item['label']==p:
                print("Ai判断一致 建议保留")
                if check_type==1 and softmax[1]>=limit:
                    item['state']='2'
                    item["label"]=p
                    kg.mark_sentence(k,item)
                    i_m=i_m+1 
                    continue
                elif check_type==1 and softmax[0]>=limit:
                    item['state']='2'
                    item["label"]=p
                    kg.mark_sentence(k,item)
                    i_m=i_m+1 
                    continue
                elif check_type==2 and softmax[1]>=limit:
                    item['state']='2'
                    item["label"]=p
                    kg.mark_sentence(k,item)
                    i_m=i_m+1 
                    continue
                elif check_type==2 and softmax[0]>=limit:
                    item['state']='2'
                    item["label"]=p
                    kg.mark_sentence(k,item)
                    i_m=i_m+1 
                    continue
            elif p==1:
                #跳过ai判断不是的
                # 自动标记ai判断为不是知识的数据
                if  softmax[0]>=limit:
                    item['state']='2'
                    item["label"]=p
                    kg.mark_sentence(k,item)
                    i_m=i_m+1         
                continue
            else:
                print("Ai判别不一致")
                # if check_type==1 and softmax[0]>=limit:
                #     item['state']='2'
                #     item["label"]=p
                #     kg.mark_sentence(k,item)
                #     i_m=i_m+1 
                #     continue
            if check_type==1:
                continue
            x = input("输入1(No)或者2(Yes) Ai默认"+str(p)+":")
            # print
            try:
                x= int(x)
            except:
                pass
                x=p
            if x==1:
                print("选择No")
                # kg.tdb.delete(k)
                item['state']='2'
                item["label"]=1
                kg.mark_sentence(k,item)
                i_m=i_m+1 
                continue

            else:
                print("选择Yes")
                item["label"]=2
                item['state']='2'
            kg.mark_sentence(k,item)
            i_m=i_m+1 
            print(item)



def run_index():
    tt=tkitText.Text()
    ss=tkitSearch.Search()
    # ss.init_search()
    labels=[1,2]
    states=['1','2']
    i=0
    for k,item in kg.recheck_all():
        if (item.get("state")==None  and item.get("label")  in labels) or (item.get("state") in states and item.get("label") in labels):
            # print(item)
            if i%1000==0:
                print(i)
            i=i+1
            data=[{'title':",".join(item.get("kg")),'content':item.get("sentence"),'path':k}]
            # print(data)
            ss.add(data)

def run_index_task():
    # tt=tkitText.Text()
    ss=tkitSearch.Search()
    # ss.init_search()
    labels=[1,2]
    states=['1','2']
    i=0
    for k,item in kg.recheck_all():
        if (item.get("state")==None  and item.get("label")  in labels) or (item.get("state") in states and item.get("label") in labels):
            # print(item)
            if i%1000==0:
                print(i)
            i=i+1
            data=[{'title':",".join(item.get("kg")),'content':item.get("sentence"),'path':k}]
            # print(data)
            ss.add(data)   
def index_one(k,item):
    """
    添加一个索引
    """
    ss=tkitSearch.Search()
    data=[{'title':",".join(item.get("kg")),'content':item.get("sentence"),'path':k}]
    # print(data)
    ss.add(data)   
# s=Search()
# # s.init_search()
# data=[{'title':'www','content':'223这是我们增加搜索的s第武器篇文档，哈哈 ','path':'https://www.osgeo.cn/whoosh/batch.html'}]
# s.add(data)
# print(s.find('宠物'))
# # print(s.find('文档'))


if __name__ == '__main__':

    print("""
    1:自动标记文本 进行初步筛选
    2:开始手动标记 对自动标记的数据进行筛查
    3: 重新筛查之前数据(纯手动)
    4: 自动处理已经标注的数据
    5:自动重新筛选之前数据
    6:统计已经标记的数据
    7:重新筛查手动标记数据和预测不一致的
    8:重新筛查之前数据(自动,高于阀值自动标记)
    9:重新筛查之前数据(半自动,高于阀值自动放行)
    10:进行搜索索引操作
    11:手动预测
    12:自动索引
    """)
    x = input("输入你要执行的命令:")
    x=int(x)
    if x==1:

        auto_text_pre("/home/terry/pan/github/bert/data/text/")
        auto_text_pre()
        run_index()
    elif x==2:
        print("运行2")
        run_mark_pred()
    elif x==3:
        print("检查label==2的")
        # run_recheck(2,state='2',check_type=1)
        run_recheck(2,state='1',check_type=0)
        print("检查label==1的")
        run_recheck(1)
    elif x==4:
        auto_run_mark_pred()
    elif x==5:
        auto_run_recheck()
    elif x==6:
        statistics()
    elif x==7:
        print("检查label==2的")
        run_recheck(2,state='2',check_type=1)
    elif x==8:
        print("检查label==2的")
        run_recheck(2,state='1',check_type=1)
        #检查低概率的
        run_recheck(0,state='1',check_type=1)
        run_index()
        auto_text_pre()
    elif x==9:
        print("检查label==2的")
        run_recheck(2,state='1',check_type=2)
    elif x==10:
        print("进行搜索索引操作")
        run_index()
    elif x==11:
        text = input("输入需要预测的句子:")
        kgs=pre_kg_clear(text)
        print(kgs)
    elif x==12:
        run_index_task()
    # run_mark()
    # run_text()
    # run_text_pre()
    # run_text_pre()
    # run_recheck()
    # key="4d72f13470e8dfd82f35db8rerbb4881154"
    # print(kg.check_marked(key))