import os
import re
import numpy as np
import requests
import networkx as nx

hit = []
with open('./南开新闻/南开要闻491.txt', mode='r', encoding='utf-8') as f:
    line = f.readlines()
    Re = re.compile('link:(.*?), title:')
    # 找到该行的链接
    link = Re.findall(line[0])[0]
    # 获取该网页源代码
    html = requests.get(link)
    html_bytes = html.content
    htmlcode = html_bytes.decode('utf-8')
    # 找到该网页指向的网页
    Re = re.compile('<a href="(.*?)" target="_blank">(.*?)</a><br/>')
    hit = Re.findall(htmlcode)
    with open('./南开新闻/热点新闻.txt', mode='w', encoding='utf-8') as w:
        for i in range(10):
            text = "link:" + hit[i][0] + ", title:" + hit[i][1] + '\n'
            w.write(text)
        w.close()
    f.close()

G = nx.Graph()

for filepath, dirnames, filenames in os.walk('./南开新闻'):
    for filename in filenames:
        ab_filepathos = os.path.join(filepath, filename)
        with open(ab_filepathos, 'r', encoding='utf-8') as f:
            # 将文件读取到lines中，按行读取
            lines = f.readlines()
        for line in lines:
            Re = re.compile('link:(.*?), title:')
            # 找到该行的链接
            link = Re.findall(line)[0]
            for i in range(10):
                G.add_edge(link, hit[i][0])
        f.close()

pr = nx.pagerank(G)
for node, value in pr.items():
    print(node, value)
for i in range(10):
    print(hit[i][0], pr[hit[i][0]])