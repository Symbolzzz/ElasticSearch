import search
from elasticsearch import Elasticsearch
import streamlit as st

# 设置网页标题
st.set_page_config(page_title='南开资源站', layout='wide')

# 隐藏右边的菜单以及页脚
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.header("欢迎来到南开资源站！")
st.subheader("查询你想要的南开资源信息")
name = st.text_input('用户名')

# 设置左侧导航栏
sidebar = st.sidebar.radio(
    "南开要闻",
    ("首页", "站内查询", "文档查询", "短语查询", "通配查询", "查询日志")
)


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

elif sidebar == '文档查询':
    st.title('文档查询')
    # 创建一个表单
    with st.form('文档查询'):
        itext = st.text_input('查询文档的ID')
        confirm = st.form_submit_button('确认')
    if confirm:
        res = search.docSearch(name, itext)
        st.write('查询到了' + str(res['hits']['total']['value']) + '条结果')
        for hit in res['hits']['hits']:
            st.write(hit['_source'])

elif sidebar == '短语查询':
    st.title('短语查询')
    # 创建一个表单
    with st.form('短语查询'):
        keytext = st.text_input('查询的短语')
        confirm = st.form_submit_button('确认')
    if confirm:
        res = search.phraseSearch(name, keytext)
        st.write('查询到了' + str(res['hits']['total']['value']) + '条结果')
        for hit in res['hits']['hits']:
            st.write(hit['_source'])

elif sidebar == '通配查询':
    st.title('通配查询')
    # 创建一个表单
    with st.form('通配查询'):
        keytext = st.text_input('通配查询关键词')
        confirm = st.form_submit_button('确认')
    if confirm:
        res = search.wildcardSearch(name, keytext)
        st.write('查询到了' + str(res['hits']['total']['value']) + '条结果')
        for hit in res['hits']['hits']:
            st.write(hit['_source'])    

elif sidebar == '查询日志':
    st.title('查询日志')
    with open('./查询日志.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        st.write(lines)
    f.close()
else:
    st.header("欢迎来到南开资源站！")
    st.subheader("查询你想要的南开资源信息")
    log_in = st.button('登录')
    sign_up = st.button('注册')
    if log_in:
        with st.form('登录'):
            name = st.text_input('用户名')
            psw = st.text_input('密码')
            confirm = st.form_submit_button('登录')
            if confirm:
                if search.login(name, psw):
                    st.balloons()
                    st.success('Login successfully!')
                else:
                    st.write('Permission denied.')
    if sign_up:
        with st.form('注册'):
            name = st.text_input('用户名')
            psw = st.text_input('密码')
            confirm = st.form_submit_button('注册')
            if confirm:
                search.signup(name, psw)
                st.balloons()
                st.success('Sign up successfullly!')