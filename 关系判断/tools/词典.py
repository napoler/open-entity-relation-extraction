# from harvesttext import HarvestText
# from harvesttext import loadHT,saveHT
# from harvesttext.resources import get_qh_typed_words,get_baidu_stopwords
# ht0 = HarvestText()
# typed_words, stopwords = get_qh_typed_words(), get_baidu_stopwords()
# ht0.add_typed_words(typed_words)
sentence = "柯基犬是个鬼精灵，非常的可爱，也很聪明。"
# print(sentence)

# print(ht0.posseg(sentence,stopwords=stopwords))

# saveHT(ht0,"ht_model1")
# ht2 = loadHT("ht_model1")
# print(ht2.named_entity_recognition(sentence))

# ht_kg=ht2.triple_extraction(sent=sentence)

# print(ht_kg)


import tkitText

tt=tkitText.Text()
tt.load_ht(ht_model="tkitfiles/ht.model")
# tt.typed_words(ht_model="tkitfiles/ht.model")
print(tt.ht.posseg(sentence))
ht_kg=tt.ht.triple_extraction(sent=sentence)
print(ht_kg)
# tt.ht.add_new_entity("柯犬", type0="实体")  # 作为特定类型登录
print(tt.ht.posseg(sentence))

print(tt.named_entity_recognition(sentence))
print(tt.ht.named_entity_recognition(sentence))
ht_kg=tt.ht.triple_extraction(sent=sentence)

print(ht_kg)
