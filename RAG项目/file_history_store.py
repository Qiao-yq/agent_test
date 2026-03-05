import os, json
from typing import List, Sequence
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

#  message_to_dict : 单个消息对象转为字典
#  messages_from_dict : 字典转为消息对象列表

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, storage_path):
        self.session_id = session_id   #会话id
        self.storage_dir = storage_path #不同会话id存储文件，所在文件夹路径
        self.file_path = os.path.join(storage_path,session_id) #完整文件路径
        #确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_message(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)

        new_messages = [message_to_dict(m) for m in all_messages]

        with open(self.file_path, 'w', encoding='utf-8') as f: #数据写入文件，覆盖原有内容
            json.dump(new_messages, f, ensure_ascii=False)
    
    @property     #装饰器，表示该方法是一个属性，可以通过对象.属性的方式访问，而不需要调用方法
    def messages(self) -> List[BaseMessage]:
        #当前文件内：list 字典 -> list 消息对象
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                messages_dict = json.load(f)
                return messages_from_dict(messages_dict)
        except FileNotFoundError:
            return []
        
    def clear(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as f: #清空文件内容
            json.dump([], f, ensure_ascii=False)




model = ChatTongyi(model = "qwen-max", temperature=0.8)

prompt = PromptTemplate.from_template(
    "你需要根据会话历史来回答问题。会话历史如下：{history} 问题是：{question}，请回答"
)

str_parser = StrOutputParser()

base_chain = prompt | model | str_parser



# 实现通过会话id获取InMemoryChatMessageHistory对象的函数
def get_history(session_id):
    return FileChatMessageHistory(session_id, storage_path="./chat_history")  # 返回FileChatMessageHistory对象，存储路径为./chat_history

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
    # res = conversation_chain.invoke({"question": "小明有2只猫"}, config=session_config)
    # print(res)

    # res = conversation_chain.invoke({"question": "小明有3只狗"}, config=session_config)
    # print(res)

    res = conversation_chain.invoke({"question": "小明有几只宠物"}, config=session_config)
    print(res)