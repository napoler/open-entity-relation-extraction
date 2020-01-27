#encoding=utf-8
from flask import Flask, render_template, request, json, Response, jsonify,escape,redirect



#encoding=utf-8
from kg_lvdb import KgDatabase
from albert_pytorch import classify
import jiagu
import tkitFile
import tkitText
import tkitNlp
import tkitSearch

from cocoNLP.extractor import extractor
from tkitMarker import *
# import tkitFile
P=Pre()
P.args['conf']="tkitfiles/v0.1/config.json"
P.args['load_path']="tkitfiles/v0.1/pytorch_model.bin"
P.args['vocab']="tkitfiles/v0.1/vocab.txt"
P.args['label_file']="tkitfiles/v0.1/tag.txt"
P.args['max_length']=50
P.setconfig()

#初始化提取关系词
TNer=Pre()
TNer.args['conf']="tkitfiles/ner_rel/config.json"
TNer.args['load_path']="tkitfiles/ner_rel/pytorch_model.bin"
TNer.args['vocab']="tkitfiles/ner_rel/vocab.txt"
TNer.args['label_file']="tkitfiles/ner_rel/tag.txt"
TNer.args['albert_path']="tkitfiles/ner_rel"
TNer.args['albert_embedding']=312
TNer.args['rnn_hidden']=400

TNer.model_version='ner_rel'
TNer.args['max_length']=50
TNer.setconfig()


# 初始化提取实体

Ner=Pre()
Ner.args['conf']="tkitfiles/ner/config.json"
Ner.args['load_path']="tkitfiles/ner/pytorch_model.bin"
Ner.args['vocab']="tkitfiles/ner/vocab.txt"
Ner.args['label_file']="tkitfiles/ner/tag.txt"
Ner.args['albert_path']="tkitfiles/ner"
Ner.args['albert_embedding']=312
Ner.args['rnn_hidden']=400

Ner.model_version='ner'
Ner.args['max_length']=50
Ner.setconfig()


ex = extractor()
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





kg=KgDatabase()
ht0 = HarvestText()
tfile=tkitFile.File()
tt=tkitText.Text()
# tt=tkitText.Text()
# tt.load_ht(ht_model="tkitfiles/ht.model")

tt.load_ht()
# tt.typed_words(ht_model="tkitfiles/ht.model")
i=0
tclass=classify(model_name_or_path='tkitfiles/checkkg')
#检查是不是知识
check_kg=classify(model_name_or_path='../tdata/albert_check_kg')
# check_pet=classify(model_name_or_path='../tdata/albert-chinese-pytorch-pet')













def pre(data):
    """
    获取预测结果
    """
    tkg="[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
    p=tclass.pre(tkg)
    softmax=tclass.softmax()
    print("分类","|",'概率')
    pre=[]
    for ck,rank in zip([1,2],softmax):
        print(ck,"|",rank)
        pre.append([ck,rank])
    return p+1,pre



app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")
# 获取列表的第二个元素
def takeSecond(elem):
    return elem[1]
@app.route('/list/rel')
def kg_list_rel():
    """
    label all 0,1,2
    过滤
    
    
    """
    # label all 0,1,2
    # print(label)
    i=0
    items={}
    kg.tdb.load("kg_mark")

    # ss=tkitSearch.Search()
    # keyword=request.args.get('keyword')
    # start=request.args.get('start')
    label=request.args.get('label')
    state=request.args.get('state')

    if label==None or len(label)==0:
        label="all"
    for k,v in kg.tdb.get_all():
        try: 
            item=kg.tdb.str_dict(v)
        except:
            continue
            pass
        # if i>=20:
        #     break
    
        if item.get('kg')!=None and item.get('state') == state:
            if len(item.get('kg'))==3:
                if label=="all":
                    # items.append(item['kg'][1])
                    if items.get(item['kg'][1])==None:
                       items[item['kg'][1]]=1
                    else:
                        items[item['kg'][1]]= items[item['kg'][1]]+1
                    i=i+1
                elif item.get('label')==label or  item.get('label')==int(label):
                    if items.get(item['kg'][1])==None:
                       items[item['kg'][1]]=1
                    else:
                        # print("1111",item['kg'][1])
                        items[item['kg'][1]]= items[item['kg'][1]]+1
                    i=i+1
    new=[]
    print(items)
    for word in items.keys():
        new.append((word,items[word]))
    new.sort(key=takeSecond,reverse = True)
    items=new
        # if item.get('kg')==None or len(item.get('kg'))==0:
    # items=list(set(items))
    if len(items)>0:
       return render_template("list_rel.html", **locals())
    else:
        return "没有数据"
@app.route('/list')
def kg_list():
    """
    label all 0,1,2
    过滤
    
    
    """
    # label all 0,1,2
    # print(label)
    i=0
    items=[]
    kg.tdb.load("kg_mark")

    ss=tkitSearch.Search()
    keyword=request.args.get('keyword')
    start=request.args.get('start')
    label=request.args.get('label')
    tp=request.args.get('type')
    state=request.args.get('state')
    print(state)
    # states=[]
    if label==None or len(label)==0:
        label="all"
    if keyword==None or len(keyword)==0:
        for k,v in kg.tdb.get_all(start=start):
            try: 
                item=kg.tdb.str_dict(v)
            except:
                pass
            if i>=20:
                break
        
            if item.get('kg')!=None and item.get('state')=='2':
                p,pr=pre(item)
                item['pre']=pr
                item['ai']=p

                s=item['sentence']
                for w in item['kg']:
                    s=s.replace(w,"<<█"+w+"█>>")
                item['sentence_mark']=s

                if label=="all":
                    items.append((k,item))
                    i=i+1
                elif item.get('label')==int(label):
                    items.append((k,item))
                    i=i+1

    else:
        # print("kkk")
        if tp=='title':
            result= ss.find_title(keyword)
        else:
            result= ss.find(keyword)
        # print(result)
        for one in result:
            v=kg.tdb.get(one['path'])
            k=one['path']
            try: 
                item=kg.tdb.str_dict(v)
            except:
                continue
                pass
            # if item.get('kg')!=None and item.get('state')=='2':
            if item.get('kg')!=None and item.get('state') == state:
                # print(item)
                # print(label, item.get('label'))
                p,pr=pre(item)
                item['pre']=pr
                item['ai']=p

                s=item['sentence']
                for w in item['kg']:
                    s=s.replace(w,"<<█"+w+"█>>")
                item['sentence_mark']=s

                if label=="all":
                    items.append((k,item))
                    i=i+1
                elif item.get('label')==label or  item.get('label')==int(label):
                    items.append((k,item))
                    # print("3333")
                    i=i+1
 



        # if item.get('kg')==None or len(item.get('kg'))==0:
    if len(items)>0:
       return render_template("list.html", **locals())
    else:
        return "没有数据"

@app.route('/edit/<key>')
def kg_edit(key):
    """

    过滤
    
    
    """

    # data=[]
    kg.tdb.load("kg_mark")
    data=kg.tdb.get(key)
    data=kg.tdb.str_dict(data)
    #检查是否是合理的知识
    tkg="[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
    p=tclass.pre(tkg)
    softmax=tclass.softmax()
    print("分类","|",'概率')
    pre=[]
    for ck,rank in zip([1,2],softmax):
        print(ck,"|",rank)
        pre.append([ck,rank])
    data['pre']=pre
    data['ai']=p+1
    data['key']=key

    return render_template("edit.html", **locals())

@app.route("/edit_submit/<key>/<int:label>",methods=[ 'GET'])
def edit_submit(key,label):
    """
    构建训练数据
    """
    kg.tdb.load("kg_mark")
    data=kg.tdb.get(key)
    data=kg.tdb.str_dict(data)
    data['state']='2'
    data["label"]=label
    kg.mark_sentence(key,data)

    #检查是否是合理的知识
    tkg="[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
    p=tclass.pre(tkg)
    softmax=tclass.softmax()
    print("分类","|",'概率')
    pre=[]
    for ck,rank in zip([1,2],softmax):
        print(ck,"|",rank)
        pre.append([ck,rank])
    data['pre']=pre
    data['ai']=p
    data['key']=key
    return render_template("edit.html", **locals())
@app.route("/add",methods=[ 'GET'])
def add():
    """
    构建训练数据
    """
    sentence=request.args.get('s')
    kg1=request.args.get('kg1')
    kg2=request.args.get('kg2')
    kg3=request.args.get('kg3')
    if sentence==None:
        sentence=''
    if kg1==None:
        kg1=''
    if kg2==None:
        kg2=''
    if kg3==None:
        kg3=''
    return render_template("add.html", **locals())
@app.route("/add_submit",methods=[ 'GET'])
def add_submit():
    """
    构建训练数据
    """
    tt=tkitText.Text()
    kg.tdb.load("kg_mark")
    # data=kg.tdb.get(key)
    # data=kg.tdb.str_dict(data)
    sentence=request.args.get('sentence')
    kg1=request.args.get('kg1')
    kg2=request.args.get('kg2')
    kg3=request.args.get('kg3')
    data={}
    data['state']='2'
    data["label"]=2
    data['sentence']=sentence
    data['kg']=[kg1,kg2,kg3]
    key=tt.md5(data["sentence"]+'，'.join(data['kg']))
    
    
    kg.mark_sentence(key,data)

    # #检查是否是合理的知识
    # tkg="[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
    # p=tclass.pre(tkg)
    # softmax=tclass.softmax()
    # print("分类","|",'概率')
    # pre=[]
    # for ck,rank in zip([1,2],softmax):
    #     print(ck,"|",rank)
    #     pre.append([ck,rank])
    # data['pre']=pre
    # data['ai']=p
    # data['key']=key
    # return '已经保存'
    return redirect("/edit_submit/"+key+"/2", code=302)

@app.route("/json/edit_submit",methods=[ 'GET'])
def json_edit_submit():
    """
    构建训练数据
   
    """
    print("开始修改")
    key=request.args.get('key')
    label=request.args.get('label')
    print(label)

    kg.tdb.load("kg_mark")
    data=kg.tdb.get(key)
    data=kg.tdb.str_dict(data)
    data['state']='2'
    data["label"]=label
    kg.mark_sentence(key,data)

    # #检查是否是合理的知识
    # tkg="[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
    # p=tclass.pre(tkg)
    # softmax=tclass.softmax()
    # print("分类","|",'概率')
    # pre=[]
    # for ck,rank in zip([1,2],softmax):
    #     print(ck,"|",rank)
    #     pre.append([ck,rank])
    # data['pre']=pre
    # data['ai']=p
    data['key']=key
    print(data)
    return jsonify(data)
    # return render_template("edit.html", **locals())










if __name__ == "__main__":
    app.run(
        host = '0.0.0.0',
        port = 7777,  
        debug = False 
    )

