import  tkitNlp
from memory_profiler import profile
import gc

@profile
def t():
    ie=tkitNlp.TripleIE(model_path="/mnt/data/dev/model/ltp/ltp_data_v3.4.0")
    text="Python 内存管理及删除or释放- 汪洋大海– 蜗居"
    a=ie.get(text)
    ie.release()
    # del ie
    gc.collect()
    print('1111')
    print(a)
    ie=None
@profile
def t2():
    ie=tkitNlp.TripleExtractor()
    for i in range(100):
        text="Python 内存管理及删除or释放- 汪洋大海– 蜗居"
        a=ie.triples_main(text)
        print('1111')
    ie.release()
    del ie
    gc.collect()
    print('1111')
    print(a)
    del a
    gc.collect()
    print('2222')
    ie=None


# for i in range(10):
    # t()
t2()
t2()
    # t()