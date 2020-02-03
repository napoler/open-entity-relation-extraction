# encoding=utf-8
from flask import Flask, render_template, request, json, Response, jsonify, escape, redirect
import psutil

import os
import sys
# encoding=utf-8
from kg_lvdb import KgDatabase
from albert_pytorch import classify
import jiagu
import tkitFile
import tkitText
import tkitNlp
import tkitSearch

from cocoNLP.extractor import extractor
from tkitMarker import *
# # import tkitFile
# P=Pre()
# P.args['conf']="tkitfiles/v0.1/config.json"
# P.args['load_path']="tkitfiles/v0.1/pytorch_model.bin"
# P.args['vocab']="tkitfiles/v0.1/vocab.txt"
# P.args['label_file']="tkitfiles/v0.1/tag.txt"
# P.args['max_length']=50
# P.setconfig()

# #初始化提取关系词
# TNer=Pre()
# TNer.args['conf']="tkitfiles/ner_rel/config.json"
# TNer.args['load_path']="tkitfiles/ner_rel/pytorch_model.bin"
# TNer.args['vocab']="tkitfiles/ner_rel/vocab.txt"
# TNer.args['label_file']="tkitfiles/ner_rel/tag.txt"
# TNer.args['albert_path']="tkitfiles/ner_rel"
# TNer.args['albert_embedding']=312
# TNer.args['rnn_hidden']=400

# TNer.model_version='ner_rel'
# TNer.args['max_length']=50
# TNer.setconfig()


# # 初始化提取实体

# Ner=Pre()
# Ner.args['conf']="tkitfiles/ner/config.json"
# Ner.args['load_path']="tkitfiles/ner/pytorch_model.bin"
# Ner.args['vocab']="tkitfiles/ner/vocab.txt"
# Ner.args['label_file']="tkitfiles/ner/tag.txt"
# Ner.args['albert_path']="tkitfiles/ner"
# Ner.args['albert_embedding']=312
# Ner.args['rnn_hidden']=400

# Ner.model_version='ner'
# Ner.args['max_length']=50
# Ner.setconfig()


# ex = extractor()
from harvesttext import HarvestText

import pkuseg

from pprint import pprint
import gc


import os
# LTP_DATA_DIR = '/mnt/data/dev/model/ltp/ltp_data_v3.4.0'  # ltp模型目录的路径
# ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
# cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
# pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
# srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl.model')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
# par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`

from pyltp import Parser
from pyltp import SementicRoleLabeller
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

# 查看内存占用
from memory_profiler import profile


# kg=KgDatabase()
# ht0 = HarvestText()
# tfile=tkitFile.File()
# tt=tkitText.Text()
# # tt=tkitText.Text()
# # tt.load_ht(ht_model="tkitfiles/ht.model")

# tt.load_ht()
# # tt.typed_words(ht_model="tkitfiles/ht.model")
# i=0
# Tclass=classify(model_name_or_path='tkitfiles/checkkg')
# #检查是不是知识
# Check_kg=classify(model_name_or_path='../tdata/albert_Check_kg')
# # check_pet=classify(model_name_or_path='../tdata/albert-chinese-pytorch-pet')


from mark import *
from TEntityRel import *
from config import *


def pre(data):
    """
    获取预测结果
    """
    tkg = "[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
    p = Tclass.pre(tkg)
    softmax = Tclass.softmax()
    Tclass.release
    print("分类", "|", '概率')
    pre = []
    for ck, rank in zip([1, 2], softmax):
        print(ck, "|", rank)
        pre.append([ck, rank])
    # del Tclass
    gc.collect()
    return p+1, pre


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
    i = 0
    items = {}
    # kg.tdb.load("kg_mark")

    # ss=tkitSearch.Search()
    # keyword=request.args.get('keyword')
    # start=request.args.get('start')
    label = request.args.get('label')
    state = request.args.get('state')

    if label == None or len(label) == 0:
        label = "all"
    # for k, v in kg.tdb.get_all():
    for item in DB.kg_mark.find():
        k=item['_id']
        if item.get('kg') != None and item.get('state') == state:
            if len(item.get('kg')) == 3:
                if label == "all":
                    # items.append(item['kg'][1])
                    if items.get(item['kg'][1]) == None:
                        items[item['kg'][1]] = 1
                    else:
                        items[item['kg'][1]] = items[item['kg'][1]]+1
                    i = i+1
                elif item.get('label') == label or item.get('label') == int(label):
                    if items.get(item['kg'][1]) == None:
                        items[item['kg'][1]] = 1
                    else:
                        # print("1111",item['kg'][1])
                        items[item['kg'][1]] = items[item['kg'][1]]+1
                    i = i+1
    new = []
    print(items)
    for word in items.keys():
        new.append((word, items[word]))
    new.sort(key=takeSecond, reverse=True)
    items = new
    # if item.get('kg')==None or len(item.get('kg'))==0:
    # items=list(set(items))
    if len(items) > 0:
        return render_template("list_rel.html", **locals())
    else:
        return "没有数据"


@app.route('/list')
def kg_list():
    """
    label all 0,1,2
    过滤


    """
    tt = tkitText.Text()
    # label all 0,1,2
    # print(label)
    i = 0
    items = []
    
    

    ss = tkitSearch.Search()
    keyword = request.args.get('keyword')
    start = request.args.get('start')
    label = request.args.get('label')
    tp = request.args.get('type')
    state = request.args.get('state')
    check = request.args.get('check')
    limit=request.args.get('limit')
    if limit==None:
        limit=100
    if start == None:
        kg.tdb.load("var")
        try:
            start=kg.tdb.get("list_start")
        except:
            pass
    print("start",start)

    kg.tdb.load("kg_mark")
    print(state)
    if state == None:
        state = "2"
    # states=[]
    if label == None or len(label) == 0:
        label = 2
    if keyword == None or len(keyword) == 0:
        print("no kw")
        jump=["目","是",'市镇']
        # for k, v in kg.tdb.get_all(start=start):
        q={'check': None,"state":state,'label':int(label)}
        print('q',q)
        for item in DB.kg_mark.find(q).limit(int(limit)):
            k=item['_id']
            print(item)
            # try:
            #     item = kg.tdb.str_dict(v)
            # except:
            #     pass
            # if i >= 100:
            #     kg.tdb.load("var")
            #     # kg.tdb.get("list_start")
            #     kg.tdb.put_data([('list_start',list_start)])
            #     print('list_start',list_start)
            #     break
            # 索引数据
            # index_one(k, item)
            # if item.get('kg') != None and item.get('state') == state and item.get('check') == check:
            # if item.get('kg') != None:
            # index_one(k, item)
            #自动跳过
            # if item.get('kg')[1] in jump:
            #     continue
            print('选择', item)
            p, pr = pre(item)
            item['pre'] = pr
            item['ai'] = p
            # 自动保存进程
            item['check'] = True
            # key=tt.md5(item["sentence"]+'，'.join(item['kg']))
            kg.mark_sentence(k, item)

            s = item['sentence']
            for w in item['kg']:
                s = s.replace(w, "<<█"+w+"█>>")
            item['sentence_mark'] = s

            if label == "all":
                items.append((k, item))
                i = i+1
                list_start=k
            elif item.get('label') == int(label):
                items.append((k, item))
                i = i+1
                list_start=k

    else:
        q={'check': None,"kg":keyword,"state":state,'label':int(label)}
        print('q',q)
        for item in DB.kg_mark.find(q).limit(int(limit)):
            k=item['_id']
            print(item)
        # print("kkk")
        # if tp == 'title':
        #     result = ss.find_title(keyword)
        # else:
        #     result = ss.find(keyword)
        # # print(result)
        # for one in result:
            # v = kg.tdb.get(one['path'])
            # k = one['path']
            # try:
            #     item = kg.tdb.str_dict(v)
            # except:
            #     continue
            #     pass
            # if item.get('kg')!=None and item.get('state')=='2':
            if item.get('kg') != None and item.get('state') == state and item.get('check') == check:
                # 预测内容的概率
                p, pr = pre(item)
                item['pre'] = pr
                item['ai'] = p
                # 自动保存进程
                item['check'] = True
                # key=tt.md5(item["sentence"]+'，'.join(item['kg']))
                kg.mark_sentence(k, item)

                s = item['sentence']
                for w in item['kg']:
                    s = s.replace(w, "<<█"+w+"█>>")
                item['sentence_mark'] = s

                if label == "all":
                    items.append((k, item))
                    i = i+1
                elif item.get('label') == label or item.get('label') == int(label):
                    items.append((k, item))
                    # print("3333")
                    i = i+1

    # for x in dir():
    #     print(x,sys.getsizeof(x)/1024/1024,'mb')
    del ss
    gc.collect()

    # if item.get('kg')==None or len(item.get('kg'))==0:
    if len(items) > 0:
        q={'check': True}
        checked=DB.kg_mark.find(q).count()
        q={'check': None,"state":state}
        uncheck=DB.kg_mark.find(q).count()
        return render_template("list.html", **locals())
    else:
        return "没有数据"


@app.route('/edit/<key>')
def kg_edit(key):
    """

    过滤


    """
    # Tclass=classify(model_name_or_path='tkitfiles/checkkg')
    # data=[]
    # kg.tdb.load("kg_mark")
    # data = kg.tdb.get(key)

    # data = kg.tdb.str_dict(data)
    data= DB.kg_mark.find_one({'_id':key})
    print("获取data",data)
    # 检查是否是合理的知识
    tkg = "[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
    p = Tclass.pre(tkg)
    softmax = Tclass.softmax()
    Tclass.release()
    print("分类", "|", '概率')
    pre = []
    for ck, rank in zip([1, 2], softmax):
        print(ck, "|", rank)
        pre.append([ck, rank])
    data['pre'] = pre
    data['ai'] = p+1
    data['key'] = key

    return render_template("edit.html", **locals())









@app.route('/page')
def page_list():
    """
    label all 0,1,2
    过滤


    """
    tt = tkitText.Text()
    start = request.args.get('start')
    kg.tdb.load("kg_mark")
    items=[]
    i=0
    for k, v in kg.tdb.get_all(start=start):
        # print(k)
        try:
            item = kg.tdb.str_dict(v)
        except:
            pass
        if i >= 100:
        
            break
        # 索引数据
        # index_one(k, item)
        if item.get('kg') != None:
            # index_one(k, item)
            # print('选择', item)
            items.append((k, item))
            i = i+1
    # gc.collect()
    if len(items) > 0:
        return render_template("page_list.html", **locals())
    else:
        return "没有数据"

    # return jsonify(items)





@app.route("/page/<key>/")
def page(key):
    """
    构建训练数据
    """
    # Tclass=classify(model_name_or_path='tkitfiles/checkkg')
    kg.tdb.load("kg_mark")
    data = kg.tdb.get(key)
    data = kg.tdb.str_dict(data)
    # 检查是否是合理的知识
    tkg = "[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
    p = Tclass.pre(tkg)
    softmax = Tclass.softmax()
    Tclass.release()
    print("分类", "|", '概率')
    pre = []
    for ck, rank in zip([1, 2], softmax):
        print(ck, "|", rank)
        pre.append([ck, rank])
    data['pre'] = pre
    data['ai'] = p
    data['key'] = key
    print('原始md5',key)
    # kg.tdb.delete(key)
    key=get_key(data)
    print('新的md5',key)
    return render_template("page.html", **locals())








@app.route("/edit_submit/<key>/<int:label>", methods=['GET'])
def edit_submit(key, label):
    """
    构建训练数据
    """
    # Tclass=classify(model_name_or_path='tkitfiles/checkkg')
    # kg.tdb.load("kg_mark")
    # data = kg.tdb.get(key)
    # data = kg.tdb.str_dict(data)
    data= DB.kg_mark.find_one({'_id':key})
    if data==None:
        return "没有key"+key
   
    else:
        pass

    data['state'] = '2'
    data["label"] = label
    kg.mark_sentence(key, data)

    # 检查是否是合理的知识
    tkg = "[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
    p = Tclass.pre(tkg)
    softmax = Tclass.softmax()
    Tclass.release()
    print("分类", "|", '概率')
    pre = []
    for ck, rank in zip([1, 2], softmax):
        print(ck, "|", rank)
        pre.append([ck, rank])
    data['pre'] = pre
    data['ai'] = p
    data['key'] = key
    print('原始md5',key)
    # kg.tdb.delete(key)
    key=get_key(data)
    print('新的md5',key)
    return render_template("edit.html", **locals())


@app.route('/add/text')
def add_text():
    """
    添加文章

    """
    return render_template("add_text.html", **locals())


@app.route('/add/article', methods=['POST', 'GET'])
def add_article():
    """
    添加文章

    """
    items = []
    print(request.form)
    article = request.form.get('article')
    if article == None:
        return render_template("add_article.html", **locals())
    else:
        tt = tkitText.Text()
        sents = tt.sentence_segmentation_v1(article)
        # print(items)
        for item in sents:
            if len(item) > 10:
                ner_list = ner_plus(item)
                onlykgs = []
                if len(ner_list) > 0:
                    onlykgs = pre_kg(item)
                items.append((item, onlykgs, ner_list))

        return render_template("add_article.html", **locals())
# @app.route('/add_submit/text',methods=[ 'GET'])
# def add_submit_text():
#     """
#     添加文章
#     """
#     tt=tkitText.Text()
#     sentence=request.args.get('sentence')
#     onlykgs=pre_kg(sentence)
#     for kg_one in onlykgs:
#         # data['kg']=kg
#         key=tt.md5(sentence+'，'.join(kg_one))
#         print(key)
#         # kg_status=kg.check_marked(key)

#         #检查是否是合理的知识
#         tkg="[kg] "+",".join(kg_one)+" [/kg] "+sentence
#         p=Tclass.pre(tkg)
#         softmax=Tclass.softmax()
#         # print("分类","|",'概率')
#         # for ck,rank in zip([1,2],softmax):
#         #     print(ck,"|",rank)

#         if softmax[1]>0.1:
#             if kg.check_marked(key)==True:
#                 kgs.append((kg_one,key,'True',softmax[1], "rank_"+str(int(round(softmax[1], 1)*10))))
#             else:
#                 print("kg检查失败")
#                 kgs.append((kg_one,key,'False',softmax[1],  "rank_"+str(int(round(softmax[1], 1)*10))))


#     return render_template("add_submit_text.html", **locals())

@app.route("/add", methods=['GET'])
#@profile
def add():
    """
    构建训练数据
    """
    info = psutil.virtual_memory()

    print(u'内存占比：', info.percent)

    if info.percent > 10:
        # os.kill()
        # sys.exit()
        # quit()
        print('get_threshold', gc.get_threshold())
        gc.set_threshold(1, 1, 1)
        gc.collect()
        pass
    elif info.percent > 90:
        sys.exit()

    tt = tkitText.Text()
    # Tclass=classify(model_name_or_path='tkitfiles/checkkg')
    sentence = request.args.get('s')
    kg1 = request.args.get('kg1')
    kg2 = request.args.get('kg2')
    kg3 = request.args.get('kg3')
    if sentence == None:
        sentence = ''
    if kg1 == None:
        kg1 = ''
    if kg2 == None:
        kg2 = ''
    if kg3 == None:
        kg3 = ''
    onlykgs = pre_kg(sentence)
    data = {'sentence': sentence, 'kg': [kg1, kg2, kg3]
            }
    # pre(data)
    p, pr = pre(data)
    data['pre'] = pr
    data['ai'] = p
    kgs = []
    for kg_one in onlykgs:
        # data['kg']=kg
        key = tt.md5(data["sentence"]+'，'.join(kg_one))  
        print(key)
        # kg_status=kg.check_marked(key)

        # 检查是否是合理的知识
        tkg = "[kg] "+",".join(kg_one)+" [/kg] "+data['sentence']
        p = Tclass.pre(tkg)
        softmax = Tclass.softmax()
        Tclass.release()
        # print("分类","|",'概率')
        # for ck,rank in zip([1,2],softmax):
        #     print(ck,"|",rank)

        if softmax[1] > 0.1:
            if kg.check_marked(key) == True:
                kgs.append(
                    (kg_one, key, 'True', softmax[1], "rank_"+str(int(round(softmax[1], 1)*10))))
            else:
                print("kg检查失败")
                kgs.append(
                    (kg_one, key, 'False', softmax[1],  "rank_"+str(int(round(softmax[1], 1)*10))))
        del p
        del softmax
        del tkg
        gc.collect()

    # del p
    del onlykgs
    del pr

    gc.collect()
    return render_template("add.html", **locals())


@app.route("/add_submit", methods=['GET'])
#@profile
def add_submit():
    """
    构建训练数据

    """
    tt = tkitText.Text()
    info = psutil.virtual_memory()
    print(u'内存占比：', info.percent)
    if info.percent > 90:
        os.kill()
        pass
    # kg.tdb.load("kg_mark")
    # data=kg.tdb.get(key)
    # data=kg.tdb.str_dict(data)
    sentence = request.args.get('sentence')
    kg1 = request.args.get('kg1')
    kg2 = request.args.get('kg2')
    kg2_rel = request.args.get('kg2_rel')
    kg3 = request.args.get('kg3')
    data = {}
    data['state'] = '2'
    data["label"] = 2
    data['sentence'] = sentence
    data['kg'] = [kg1, kg2, kg3]
    data['check'] = True
    key = get_key(data)
    

    kg.mark_sentence(key, data)
    # 开始添加关系词
    # terry_er=TEntityRel()
    print("添加关系词", kg2_rel, kg2)
    if kg2_rel != None:
        # print("添加关系词",kg2_rel,kg2)
        Terry_er.add_entities_one(kg2_rel, kg2, '关系')
    else:
        Terry_er.add_entities_one(kg2, kg2, '关系')

    # if kg2_rel !=None and kg2 !=None:
    #     terry_er.add_entities_one(kg2_rel,kg2,'关系')
    # return "保存"
    return redirect("/edit_submit/"+key+"/2", code=302)


@app.route("/json/edit_submit", methods=['GET'])
def json_edit_submit():
    """
    构建训练数据

    """
    print("开始修改")
    key = request.args.get('key')
    label = request.args.get('label')
    print(label)

    # kg.tdb.load("kg_mark")
    # data = kg.tdb.get(key)
    # data = kg.tdb.str_dict(data)
    data= DB.kg_mark.find_one({'_id':key})
    data['state'] = '2'
    data["label"] = label
    data['check'] = True
    kg.mark_sentence(key, data)

    # #检查是否是合理的知识
    # tkg="[kg] "+",".join(data['kg'])+" [/kg] "+data['sentence']
    # p=Tclass.pre(tkg)
    # softmax=Tclass.softmax()
    # print("分类","|",'概率')
    # pre=[]
    # for ck,rank in zip([1,2],softmax):
    #     print(ck,"|",rank)
    #     pre.append([ck,rank])
    # data['pre']=pre
    # data['ai']=p
    data['key'] = key
    print(data)
    return jsonify(data)
    # return render_template("edit.html", **locals())


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=7777,
        debug=False
    )
