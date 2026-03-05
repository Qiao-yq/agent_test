import streamlit as st
import time
from rag import RagService 
import config_data as config 

st.title("智能客服")
st.divider() # 添加分割线

if "message" not in st.session_state: # 检查session_state中是否已经存在"messages"这个键，如果不存在则创建一个新的空列表并存储在session_state中
    st.session_state["message"] = [{"role": "assistant", "content": "您好！我是您的智能客服，请问有什么可以帮助您的？"}] # 创建一个新的消息列表，并将其存储在session_state中，以便在不同的脚本运行之间共享

if "rag" not in st.session_state: # 检查session_state中是否已经存在"rag"这个键，如果不存在则创建一个新的RagService对象并存储在session_state中
    st.session_state["rag"] = RagService() # 创建一个RagService对象，并将其存储在session_state中，以便在不同的脚本运行之间共享

for msg in st.session_state["message"]: # 遍历消息列表中的每条消息，根据消息的角色显示不同的消息样式
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"]) # 显示用户输入的消息
    else:
        st.chat_message("assistant").write(msg["content"]) # 显示客服回复的消息



prompt = st.chat_input("请输入您的问题：")

if prompt:
    st.chat_message("user").write(prompt) # 显示用户输入的消息
    st.session_state["message"].append({"role": "user", "content": prompt}) # 将用户输入的消息添加到消息列表中
    
    ai_res_list = []
    with st.spinner("正在查询相关资料..."):  # 显示一个加载动画，提示用户正在处理输入
        res = st.session_state["rag"].chain.stream({"input": prompt}, config=config.session_config) # 调用RagService对象的chain组件，传入用户输入的消息和配置参数，获取客服回复的消息

    def capture(generator, cache_list): # 定义一个函数，用于捕获生成器的输出并将其存储在缓存列表中
        for item in generator:
            cache_list.append(item) # 将生成器的输出添加到缓存列表中
            yield item # 将生成器的输出返回给调用者

    st.chat_message("assistant").write_stream(capture(res, ai_res_list)) # 显示客服回复的消息
    st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)}) # 将客服回复的消息添加到消息列表中
