## Chinese Open Entity Relation Extraction

The content of this work is to extract entity relations based on dependency syntax for open domain.

本工作内容为基于依存句法分析，面向开放域的实体和关系抽取。

Welcome to watch, star or fork.

### Extraction Example

> "中国国家主席习近平访问韩国，并在首尔大学发表演讲"

We can extract knowledge triples from the sentence as follows:

- (中国, 国家主席, 习近平)
- (习近平, 访问, 韩国)
- (习近平, 发表演讲, 首尔大学)

### Project Structure

```
knowledge_extraction/
|-- code/  # code directory
|   |-- bean/
|   |-- core/
|   |-- demo/  # procedure entry
|   |-- tool/
|-- data/ # data directory
|   |-- input_text.txt  # input text file
|   |-- knowledge_triple.json  # output knowledge triples file
|-- model/  # ltp models, can be downloaded from http://ltp.ai/download.html, select ltp_data_v3.4.0.zip
|-- resource  # dictionaries dirctory
|-- requirements.txt  # dependent python libraries
|-- README.md  # project description
```

### Requirements

This repo was tested on Python 3.5+. The requirements are:

- pynlpir>=0.5.2
- pyltp>=0.2.1

### Install Dependent libraries

```
pip install -r requirements.txt
```

### Entry procedure

```shell
cd ./code/demo/
python extract_demo.py
```

### Main Implementation Content

![DSNF](./img/DSNF.png)

### References

If you use the code, please kindly cite the following paper:

Jia S, Li M, Xiang Y. Chinese Open Relation Extraction and Knowledge Base Establishment[J]. ACM Transactions on Asian and Low-Resource Language Information Processing (TALLIP), 2018, 17(3): 15.
