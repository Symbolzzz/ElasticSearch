# hw4

## Web搜索引擎 - 南开资源站

### 网页抓取

实验中我抓取了南开新闻网中的南开要闻(http://news.nankai.edu.cn/ywsd/index.shtml)板块，爬取其中的共533页网站，每页网站爬取的新闻条数都是30条。

主要使用了Python的requests包来爬取网站。

```python
# 获取南开新闻网综合新闻的URL
html = requests.get('http://news.nankai.edu.cn/ywsd/index.shtml')
html_bytes = html.content
# 获取网页源代码
htmlcode = html_bytes.decode("utf-8")
```

并将爬取下来的网站写到记事本中，截取部分网站如下：

![image-20211214205228904](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214205228904.png)

![image-20211214205257588](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214205257588.png)

爬取的过程中，可以发现南开要闻网址的规律，网址是呈线性增加的，因此可以通过循环，比较容易的爬取到数据，同时将数据写入文本中。

```python
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
```

我使用了Python的re包，即正则表达式来提取网页，在网页中打开网页源代码，找到需要爬取的网页的位置，如下图：

![image-20211214211958718](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214211958718.png)

然后将需要爬取的网址和标题用(.*?)代替，即可匹配需要爬取的网站，然后再写入文本中即可。

```python
    titlere = re.compile('<a href="(.*?)" target="_blank">(.*?)</a></div></td>')
    titles = titlere.findall(htmlcode)
```

### 文本索引

文本索引与上次的思路大致相当，在爬取数据的过程中，考虑索引的构建，因此在爬取的时候在网址前加关键字`link`，在标题前加关键字`title`，那么建索引可以依据这两个关键字来建立。

```python
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
```

以上代码建立完索引后，往其中插入数据，遍历爬取数据的文件夹，同样使用正则表达式匹配之后，提取出每一行的链接和标题，存入一个列表之后，使用`bulk`函数将数据插入。

```python
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
```

### PageRank链接分析

可以发现在南开要闻网上，每一个新闻都会指向10个热点新闻：

![image-20211214214529391](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214214529391.png)

我对这十个新闻提取出来，写入到一个文本中便于访问

![image-20211214214617720](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214214617720.png)

PageRank算法的含义是，为网页构建一个有向图，当一个网页指向另外一个网页，则该边加入有向图中。遍历爬取的资源，每一个网页都指向上述所说的十个网页，因此将指向这十个热点新闻的网页的边加入到有向图中：

```python
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
```

使用Python的networkx包中的Pagerank函数，即可方便地计算出网页的PageRank值。

```python
pr = nx.pagerank(G)
for node, value in pr.items():
    print(node, value)
for i in range(10):
    print(hit[i][0], pr[hit[i][0]])
```

在终端中打印一部分信息如下：

根据上面的分析可知，只有这十个热点新闻的PageRank值较高，其余的值都一样，如下：

![image-20211214215704604](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214215704604.png)

最后十行便是热点最高的十个新闻。

### 查询服务

#### 站内查询

站内查询是指定一个查询网址，在该网址中进行查询，查询体如下：

```python
query_json = {
        'query':{
            'bool':{
                'must':[
                    {'match':{'title':key}},
                    {'match_phrase':{'link':web}}
                ]
            }
        },
        'size': 10
    }
```

其中`match_phrase`为模糊匹配，可以满足站内查询的条件，因为该网址内的资源，都会匹配包含它的网站。运行如下：

![image-20211214231059293](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214231059293.png)

以上查询目的是查询出来2021年12月6日发布的并且匹配关键字“南开大学”的新闻，可以看到结果符合预期。

#### 文档查询

该查询需要查询出来elasticsearch中的一个文档，由于每个文档的都有如下相同的结构：

```python
ACTIONS = {
        '_id': i
    }
```

可以根据‘_id'的值来查询文档，用它作为查询体的一部分。

```python
query_json = {
        'query':{
            'bool':{
                'must': [
                    {'match':ACTIONS}
                ]
            }
        },
        'size': 10
    }
```

若想查询到如下的文档：

![image-20211214231821613](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214231821613.png)

运行如下：

![image-20211214231852881](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214231852881.png)

输入该id的值，即可查询到准确的文档。

#### 短语查询

该部分在elasticsearch中已经实现，只需要编写查询体，使用`match_phrase`匹配关键词即可。

```python
query_json = {
        'query':{
            'bool':{
                'must': [
                    {'match_phrase':{'title':key}}
                ]
            }
        },
        'size': 10
    }
```

运行如下：

![image-20211214232809549](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214232809549.png)

#### 通配符查询

通配符类似于正则表达式，python中有两个主要的通配符

* `?`: which matches any single character
* `*`: which can match zero or more characters, including an empty one

`?`匹配任意单个字符，`*`匹配任意字符。

同时在查询体中，使用`wildcard`字段，可以使用通配符进行查询：

```python
query_json = {
        'query':{
            'wildcard':{
                'title':{
                    'value':key
                }
            }       
        },
        'size': 10
    }
```

运行结果如下：

![image-20211214233910625](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214233910625.png)

#### 查询日志

在上述查询函数中将查询条件、查询时间、查询类型写入文档中(以短语查询为例)

```python
with open('./查询日志.txt', mode='a', encoding='utf-8') as f:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write('phraseSearch' + '\n')
        f.write(time_str + '\n')
        f.write('key:' + key + '\n')
        f.close()
```

![image-20211214234125043](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211214234125043.png)

### 个性化查询&Web界面

实验中将这两个部分合成了一个部分，使用了python中的streamlit包来搭建web界面。

搭建的界面如下图：

![image-20211215144509802](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211215144509802.png)

![image-20211215144524129](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211215144524129.png)

在这部分中，定义了一个选择框：

```python
# 设置左侧导航栏
sidebar = st.sidebar.radio(
    "南开要闻",
    ("首页", "站内查询", "文档查询", "短语查询", "通配查询", "查询日志")
)

```

当点击不同的选择框出现不同的查询结果，以站内查询为例子：

```python
if sidebar == '站内查询':
    st.title('站内查询')
    # 创建一个表单
    with st.form('站内查询'):
        webtext = st.text_input('在网址中查询')
        keytext = st.text_input('关键词')
        confirm = st.form_submit_button('确认')
        # 点击按钮
    if confirm:
        res = search.inWebSearch(name, webtext, keytext)
        st.success('查询到了' + str(res['hits']['total']['value']) + '条结果')
        for hit in res['hits']['hits']:
            st.write(hit['_source'])
```

在子界面中，调用了站内查询函数，然后进行相应的输出即可：

![image-20211215144752538](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211215144752538.png)

同时点击查询日志，可以看到查询的记录：

![image-20211215145003330](C:\Users\86183\AppData\Roaming\Typora\typora-user-images\image-20211215145003330.png)

以此来个性化查询。
