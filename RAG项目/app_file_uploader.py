"""
基于Streamlit的web组件，允许用户上传文件并将其保存到服务器指定目录。

Streamlit:当web页面发生变化，Streamlit会自动重新运行整个脚本，从而更新页面内容。
每次用户上传文件时，Streamlit会重新运行脚本，检查是否有新的文件上传，并根据上传的文件更新页面显示的信息。
"""
import streamlit as st
from knowledge_base import KnowledgeBaseService
import time

# 添加网页标题
st.title("知识库更新服务")

#file_uploader组件允许用户上传文件，accept_multiple_files=True表示允许上传多个文件
update_file = st.file_uploader(
    "上传文件",
    type=['txt'],
    accept_multiple_files=False, # 只允许上传一个文件
)

# st.session_state 是Streamlit提供的一个特殊对象，用于在不同的脚本运行之间存储和共享数据。
if "service" not in st.session_state: # 检查session_state中是否已经存在"service"这个键，如果不存在则创建一个新的KnowledgeBaseService对象并存储在session_state中
    st.session_state["service"] = KnowledgeBaseService() # 创建一个KnowledgeBaseService对象，并将其存储在session_state中，以便在不同的脚本运行之间共享

if update_file is not None:
    # 提取文件的信息
    file_name = update_file.name
    file_type = update_file.type
    file_size = update_file.size / 1024

    st.subheader(f"文件名: {file_name}")
    st.write(f"格式： {file_type}")
    st.write(f"大小： {file_size:.2f} KB")

    # get_value()方法获取文件内容，返回一个字节流对象
    file_content = update_file.getvalue().decode("utf-8")

    with st.spinner("载入知识库中..."):  # 显示一个加载动画，提示用户正在处理文件
        time.sleep(1)  # 模拟处理文件的时间，实际应用中可以替换为真正的处理逻辑
        # 调用KnowledgeBaseService对象的update_by_str方法，将文件内容传入进行处理
        result = st.session_state["service"].update_by_str(file_content, file_name)
        st.write(result)