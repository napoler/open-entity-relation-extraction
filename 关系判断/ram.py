#常用的：
import psutil
import os
import sys
import objgraph
info = psutil.virtual_memory()
print (u'内存使用：',psutil.Process(os.getpid()).memory_info().rss)
print (u'总内存：',info.total)
print (u'内存占比：',info.percent)
print (u'cpu个数：',psutil.cpu_count())

print('virtual_memory',info)


# print(sys.getsizeof(object[, default]))
print (dir())

print()
for x in dir():
    print(x,sys.getsizeof(x)/1024/1024,'mb')

print(sys.getsizeof(sys.getsizeof))
x = []
y = [x, [x], dict(x=x)]
# objgraph.show_refs([y], filename='sample-graph.png')
# objgraph.show_most_common_types() 
# import sys, pprint
# sys.displayhook = pprint.pprint
# print(locals())
# print(globals)

# from memory_profiler import profile
@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a
my_func()