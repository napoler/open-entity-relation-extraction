from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import tkitText


tt=tkitText.Text()
a="常州现代传媒中心是一栋位于中华人民共和国江苏省常州的超高层摩天大楼，由上海建筑设计研究院有限公司设计。"
b="一栋位于中华人民共和国楼"
c=tt.find_match(a,b)
print(c)

# def find_match(a,b):
#     """
#     搜索一个相似的字段
#     从a中搜索b
#     """
#     find_b=a.find(b)
#     if find_b==-1:
#         start=a.find(b[1:2])
#         end=a.find(b[-2:-1])
#         c=a[start:end]
#         f=fuzz.partial_ratio(c,b)
#         # print(f)
#         return c,f
#     else: 
#         c=a[find_b:len(b)]
#         print(c)
#         # f=fuzz.partial_ratio(c,b)
#         # print(f)
#         # if f==100:
#         return c,100


#     # # f=fuzz.partial_ratio(a,b)
#     # start=a.find(b[1:3])
#     # end=a.find(b[-3:-1])
#     # c=a[start:end]
#     # f=fuzz.partial_ratio(c,b)
#     # # print(f)
#     # return c,f

# a="嘉朵能够帮助或带领丹恩·萧完成许多事，如逛商店；牠在完成一天的工作后便待在马厩里"
# b="帮助或带领丹恩"
# c=find_match(a,b)
# print(c)