import os
import re
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch()

# 建立索引的函数
def create_index():
    mappings = {
        "mappings":{
            "properties":{
                "link":{
                    "type":"text",
                    "index":"true"
                },
                "title":{
                    "type":"text",
                    "index":"true"
                }
            }
        }
    }

    if es.indices.exists("nkindex") is not True:
        es.indices.create(index = 'nkindex', body = mappings)
    else:
        es.indices.delete(index = 'nkindex')
        es.indices.create(index = 'nkindex', body = mappings)
# 将抓取下来的南开新闻添加到索引中

def loadnews():
    tempList = []
    for filepath, dirnames, filenames in os.walk('./南开新闻'):
        for filename in filenames:
            # 合成绝对路径
            ab_filepathos = os.path.join(filepath, filename)
            # 以r格式打开，即只读格式
            with open(ab_filepathos, 'r', encoding='utf-8') as f:
                # 将文件读取到lines中，按行读取
                lines = f.readlines()
            for line in lines:
                # 提取每一行中的链接和标题
                Re = re.compile('link:(.*?), title:')
                link = Re.findall(line)[0]
                title = line[line.index('title:') + 6:]
                body = {
                    'link':link,
                    'title':title,
                }
                # 使用json格式传输字典
                tempList.append(json.dumps(body))

    ACTIONS = [
        {
            '_index':'nkindex',
            '_type':'_doc',
            '_source': s
        }
        for s in tempList
    ]

    bulk(es, ACTIONS)

create_index()
loadnews()
