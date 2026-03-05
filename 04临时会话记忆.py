from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatTongyi(model = "qwen-max", temperature=0.8)

prompt = PromptTemplate.from_template(
    "你需要根据会话历史来回答问题。会话历史如下：{history} 问题是：{question}，请回答"
)

str_parser = StrOutputParser()

base_chain = prompt | model | str_parser

store = {}  # 用于存储会话历史的字典, key为session_id, value为InMemoryChatMessageHistory对象

# 实现通过会话id获取InMemoryChatMessageHistory对象的函数
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()  # 如果没有历史记录，创建一个新的InMemoryChatMessageHistory对象
    return store[session_id]

# 创建一个新的链， 对原有链增强，自动附加历史消息
conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,  #通过会话id获取InMemoryChatMessageHistory对象的函数
    input_messages_key="question",  # 将输入问题作为获取历史消息的参数
    history_messages_key="history",       # 将获取到的历史消息放入输入中，
)
  
if __name__ == "__main__":
    #
    session_config = {
        "configurable": {
            "session_id": "test_session_1"
        }
    }
    res = conversation_chain.invoke({"question": "小明有2只猫"}, config=session_config)
    print(res)

    res = conversation_chain.invoke({"question": "小明有3只狗"}, config=session_config)
    print(res)

    res = conversation_chain.invoke({"question": "小明有几只宠物"}, config=session_config)
    print(res)