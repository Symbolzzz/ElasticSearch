import requests
import re

# 获取南开新闻网综合新闻的URL
html = requests.get('http://news.nankai.edu.cn/ywsd/index.shtml')
html_bytes = html.content
# 获取网页源代码
htmlcode = html_bytes.decode("utf-8")

# 使用正则表达式获取新闻标题和相应的链接
titlere = re.compile('<a href="(.*?)" target="_blank">(.*?)</a></div></td>')
# 在源代码中找出所有匹配的项
titles = titlere.findall(htmlcode)

# 网页首页与其他页网址不同，需要单独获取
filehandle = open('./南开新闻/南开要闻533.txt', mode = 'w', encoding='utf-8')
for title in titles:
    text = "link:" + str(title[0]) + ", title:" + str(title[1])
    filehandle.write(text + '\n')
filehandle.close()

count = 0
for i in range(532, 0, -1):
    # 网页的页数有规律
    i = str(i).zfill(3)
    html = requests.get('http://news.nankai.edu.cn/ywsd/system/count//0003000/000000000000/000/000/c0003000000000000000_000000' + i + '.shtml')
    html_bytes = html.content
    htmlcode = html_bytes.decode("utf-8")

    titlere = re.compile('<a href="(.*?)" target="_blank">(.*?)</a></div></td>')
    titles = titlere.findall(htmlcode)
    filehandle = open('./南开新闻/南开要闻' + i + '.txt', mode='w', encoding='utf-8')
    for title in titles:
        text = "link:" + str(title[0]) + ", title:" + str(title[1])
        filehandle.write(text + '\n')
        count += 1
    filehandle.close()
print("finish!")
