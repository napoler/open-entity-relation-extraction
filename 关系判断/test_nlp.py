import tkitNlp
import macropodus


extractor=tkitNlp.TripleExtractor()



content2 = """
乔治·克林顿（George Clinton，1739年7月26日－1812年4月20日），美国军人、政治家，民主共和党党员，曾任纽约州州长（1777年-1795年、1801年-1804年）和美国副总统（1805年-1812年）。

下列县名是以他的姓氏命名作为纪念。

"""

# extractor = TripleExtractor()
svos = extractor.triples_main(content2)
# print('svos', svos)

for it in svos:
    
    # print(it)
    for one in it[1]:
        print("++++"*10)
        if one[3]=="主谓宾":
            print(one)