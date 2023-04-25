from elasticsearch import Elasticsearch
import re
import datetime
es = Elasticsearch()

def signup(name, psw):
    with open('./用户信息.txt', mode='a', encoding='utf-8') as f:
        text = 'name:' + name + ' ,password:' + psw;
        f.write(text + '\n')
    f.close()

def login(name, psw):
    with open('./用户信息.txt', mode='a', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            Re = re.compile('name:(.*?) ,password:(.*?)')
            info = Re.findall(line)
            if name == info[0] and psw == info[1]:
                f.close()
                return True
            else:
                f.close()
                return False

# 站内查询
def inWebSearch(name, web, key):
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
    res = es.search(index='nkindex', body=query_json)
    
    print("results are as follow")
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit['_source'])
    with open('./查询日志.txt', mode='a', encoding='utf-8') as f:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        f.write('inWebSearch' + '\n')
        f.write(time_str + '\n')
        f.write('web:' + web + '\n')
        f.write('key:' + key + '\n')
        f.close()
    return res


# 文档查询
def docSearch(name, i):
    ACTIONS = {
        '_id': i
    }
        
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
    res = es.search(index='nkindex', body=query_json)
    
    print("results are as follow")
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit['_source'])
    with open('./查询日志.txt', mode='a', encoding='utf-8') as f:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        f.write('docSearch' + '\n')
        f.write(time_str + '\n')
        f.write('docid:' + i + '\n')
        f.close()
    return res

# 短语查询
def phraseSearch(name, key):
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
    res = es.search(index='nkindex', body=query_json)
    
    print("results are as follow")
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit['_source'])
    with open('./查询日志.txt', mode='a', encoding='utf-8') as f:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write('phraseSearch' + '\n')
        f.write(time_str + '\n')
        f.write('key:' + key + '\n')
        f.close()
    return res

# 通配符查询
def wildcardSearch(name, key):
    # ?, which matches any single character
    # *, which can match zero or more characters, including an empty one
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
    res = es.search(index='nkindex', body=query_json)
    
    print("results are as follow")
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print(hit['_source'])
    with open('./查询日志.txt', mode='a', encoding='utf-8') as f:
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')      
        f.write('wildcardSearch' + '\n')
        f.write(time_str + '\n')
        f.write('key:' + key + '\n')
        f.close()
    return res

