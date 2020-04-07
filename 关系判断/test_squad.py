import tkitFile


# ner_reljson=tkitFile.Json("../tdata/onlyner/dev.json")
# i=0
# all=0
# # ner_list=ner_plus(text)
# for item in ner_reljson.auto_load():


# The checkpoint albert-base-v2 is not fine-tuned for question answering. Please see the
# examples/run_squad.py example to see how to fine-tune a model to a question answering task.

from transformers import AlbertTokenizer, AlbertForQuestionAnswering,BertTokenizer,AlbertConfig
import torch

# tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
tokenizer = BertTokenizer.from_pretrained('tkitfiles/qa/model/')
# config=AlbertConfig.from_pretrained('tkitfiles/qa/model/config.json')
model = AlbertForQuestionAnswering.from_pretrained('tkitfiles/qa/model/')

data=tkitFile.Json("../tdata/SQuAD/dev.json")
i=0
all=0
f=0
for item in data.auto_load():
    for one in item['data']:
        all=all+1
        # print(one['paragraphs'][0])
        # print(one['paragraphs'][0]['context'])
        question, text = one['paragraphs'][0]['qas'][0]['question'],one['paragraphs'][0]['context']

        # question, text = "利比里亚共和国", "利比里亚共和国（英语：'） 通称赖比瑞亚，是位于西非，北接几内亚，西北界塞拉利昂，东邻象牙海岸，西南濒大西洋的总统制共和国家"
        input_dict = tokenizer.encode_plus(question, text, return_tensors='pt')
        start_scores, end_scores = model(**input_dict)
        # print(start_scores, end_scores)
        # print( torch.argmax(start_scores).item())
        # print( torch.argmax(end_scores).item())

        s = torch.softmax(end_scores,dim=1)  #指定求1范数  
        # print(s.data.numpy().tolist())
        
        # print(start_scores, end_scores)
        for s,e in zip(start_scores, end_scores):
            start=torch.argmax(s).item()
            end=torch.argmax(e).item()
            if start>end:
                # print(text[end:start+1])
                if text[end:start+1]==one['paragraphs'][0]['qas'][0]['answers'][0]['text']:
                    i=i+1
                    f=f+1
                pass
            else:
                print("+++++++++++++++++++")
                print(question, text )
                print("+++++++++++++++++++")
                print("问题",question)
                print("标注答案",one['paragraphs'][0]['qas'][0]['answers'][0]['text'])
                print("预测",text[start:end+1])
                if text[start:end+1]==one['paragraphs'][0]['qas'][0]['answers'][0]['text']:
  
                    i=i+1
                print("成功",i,f,all)
print("成功",i,f,all)



        # s = torch.softmax(end_scores,dim=1)  #指定求1范数  
        # print(s.data.numpy().tolist())