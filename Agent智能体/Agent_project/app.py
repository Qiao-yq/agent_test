from agent.react_agent import ReactAgent
import streamlit as st
import time

# 标题
st.title("扫地机器人智能客服")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:     # 每次页面变化，streamlit都会重新执行流程，为了之前代码都能显示，循环写
    st.chat_message(message["role"]).write(message["content"])
# 用户输入提示词
prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    with st.spinner("智能客服思考中……"):
        res = st.session_state["agent"].execute_stream(prompt)

        res_messages = []

        def capture(generator, cache_list):  # 传进来迭代器，返回迭代器，中间把迭代器内容放进缓存列表
            for chunk in generator:          # 迭代器只能使用一次，直接输出的话，就不能保存进历史消息
                cache_list.append(chunk)

                for char in chunk:
                    time.sleep(0.01)
                    yield char
        
        st.chat_message("assistant").write_stream(capture(res, res_messages))  # 这样就能既在页面显示，又往res_messages记录AI返回内容
        st.session_state["message"].append({"role": "assistant", "content": res_messages[-1]})  # 只记录最后一条就可以
        st.rerun()

