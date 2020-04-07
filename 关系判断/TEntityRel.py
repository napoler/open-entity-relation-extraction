import tkitText
import tkitDb
import os
import gc
# tt=tkitText.Text()
# tt=tkitText.Text()
# tt.load_ht(ht_model="tkitfiles/ht.model")

# tt.load_ht()
# tt.typed_words(ht_model="tkitfiles/ht_rel.model")
# para="""
# 根据统计，边境牧羊犬的寿1命大概在13-14年左右，它的体型中等，身躯筋肉健壮
# """

# print(tt.ht.cut_sentences(para))


# for word, flag in tt.ht.posseg(para):
# 	print("%s:%s" % (word, flag),end = " ")
# # tt.ht.add_new_entity("寿命", mention0="寿1命", type0="关系词")  # 作为特定类型登录


# for word, flag in tt.ht.posseg(para):
# 	print("%s:%s" % (word, flag),end = " ")



# para = "上港的武磊和恒大的郜林，谁是中国最好的前锋？那当然是武磊武球王了，他是射手榜第一，原来是弱点的单刀也有了进步"

# entity_mention_dict = {'武磊':['武磊','武球王'],'郜林':['郜林','郜飞机'],'前锋':['前锋'],'上海上港':['上港'],'广州恒大':['恒大'],'单刀球':['单刀'],'寿命':["寿命",'寿1命']}
# entity_type_dict = {'武磊':'球员','郜林':'球员','前锋':'位置','上海上港':'球队','广州恒大':'球队','单刀球':'术语','寿命':'关系词'}
# entity_dict=entity_mention_dict,entity_type_dict
# pkl=tkitDb.Pkl(path="tkitfiles",task='entity_dict')
# pkl.save([entity_dict])

# def load_entity_dict():
#     """
#     加载词典
#     """
#     pkl=tkitDb.Pkl(path="tkitfiles",task='entity_dict')
#     entity_dict_list = []
#     for item in pkl.load():
#         entity_dict_list=entity_dict_list+item
#     return entity_dict_list[0]





# #保存术语词
# tt.ht.save_entity_info(save_path='./ht_entities.txt',)
# # 加载术语
# tt.ht.load_entities( load_path='./ht_entities.txt', override=True)
# #添加术语
# entity_mention_dict = {'武磊':['武磊','武球王'],'郜林':['郜林','郜飞机'],'前锋':['前锋'],'上海上港':['上港'],'广州恒大':['恒大'],'单刀球':['单刀'],'寿命':["寿命",'寿1命']}
# entity_type_dict = {'武磊':'球员','郜林':'球员','前锋':'位置','上海上港':'球队','广州恒大':'球队','单刀球':'术语','寿命':'关系词'}
# tt.ht.add_entities(entity_mention_dict,entity_type_dict)





# print(tt.ht.entity_type_dict)
# print(tt.ht.entity_mention_dict)
# print(tt.ht.entity_type_dict)



class TEntityRel:
    """
    关系词和实体操作类
    """

    def __init__(self,model=None):
        self.tt=tkitText.Text()
        if model ==None:
            self.model="tkitfiles/ht.model"
        else:
            self.model=model
        if os.path.exists(self.model):
            self.tt.load_ht(ht_model=self.model)
        else:
            self.tt.load_ht()
            self.tt.typed_words(ht_model=self.model)
            self.tt.save_ht()
    def __del__(self):
        print("__del__")
        class_name = self.__class__.__name__
        print(class_name, '销毁')

        # try:
        #     self.tt.load_ht(ht_model=self.model)
        # except:
        #     self.tt.load_ht()
        #     self.tt.typed_words(ht_model=self.model)
    def save(self):
        self.tt.save_ht()
    def release(self):
        del self.tt
        gc.collect()
        pass

    def add_entities(self,entity_mention_dict,entity_type_dict):
        """
        #添加术语
        entity_mention_dict = {'武磊':['武磊','武球王'],'郜林':['郜林','郜飞机'],'前锋':['前锋'],'上海上港':['上港'],'广州恒大':['恒大'],'单刀球':['单刀'],'寿命':["寿命",'寿1命']}
        entity_type_dict = {'武磊':'球员','郜林':'球员','前锋':'位置','上海上港':'球队','广州恒大':'球队','单刀球':'术语','寿命':'关系词'}
        """
        self.tt.ht.add_entities(entity_mention_dict,entity_type_dict)
        self.save()
    def add_entities_one(self,word,mention0,type0="实体"):
        """
        添加一个同义词或者关系词
        word, 所属的同义词 作为roo
        mention0, t关键词
        type0 类型


        
        """
        self.tt.ht.add_new_entity(word, mention0=mention0, type0=type0)  # 作为特定类型登录
        self.save()
    def get_entity_rel(self,para):
        """基于词典获取实体和关系词
        并无对应关系
        返回
         entity_words,rel
         实体和关系列表
        """

        rel=[]
        entity_words=[]
        for word, flag in self.tt.ht.posseg(para):
            # print("%s:%s" % (word, flag),end = " ")
            if flag=="关系":
                rel.append(word)
            elif flag=="实体":
                entity_words.append(word)
        # print(rel)
        # print(entity_words)
        return entity_words,rel
    def entity_linking(self,para):
        #进行消歧义实体链接
        for span, entity in self.tt.ht.entity_linking(para):
            print(span, entity)

# terry_er=TEntityRel()

# para="""
# 何引丽是中国内蒙古自治区包头市人，中华人民共和国田径运动员
# """

# # #添加实体词和冠词
# # terry_er.add_entities_one("寿命",'寿1命','关系')
# # terry_er.add_entities_one("边境牧羊犬",'边境牧羊犬','实体')
# # terry_er.entity_mention_dict,entity_type_dict)
# entity_words,rel=terry_er.get_entity_rel(para)
# print(rel)
# print(entity_words)

