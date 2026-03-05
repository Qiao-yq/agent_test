from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
import config_data as config

class RagService(object):
    def __init__(self): 

        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "以我提供的资料为主，简洁、准确地回答我的问题，如果资料中没有提到相关信息，请直接说不知道，不要编造答案。参考资料：{context}"),
                ("system", "我提供用户的历史会话记录，作为回答问题的参考，历史会话记录如下："),
                MessagesPlaceholder("history"),
                ("human", "请回答用户提问：{input}"),
            ]
        )

        self.chat_model = ChatTongyi(model=config.chat_model_name)

        self.chain = self.__get_chain()

    def __get_chain(self): #获取最终的执行链
        retriever = self.vector_service.get_retriever() #获取向量数据库的检索器

        def format_document(docs : list[Document]): #格式化检索到的资料
            if not docs:
                return "没有相关资料"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return formatted_str

        def format_for_retriever(value: dict) -> str: #格式化输入，供向量数据库检索使用
            return value["input"]
        
        def format_for_prompt_template(value: dict) -> str: #格式化输入，供提示模板使用
            new_value = {}
            new_value["input"] = value["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
            {
                "input": RunnablePassthrough(),                   #输入不变，直接传递给下一个组件
                "context": RunnableLambda(format_for_retriever) | retriever | format_document           #从向量数据库中检索相关资料
            }  |  RunnableLambda(format_for_prompt_template) | self.prompt_template   | self.chat_model |   StrOutputParser()         #将检索到的资料和用户输入格式化成提示
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )  

        return conversation_chain
    
if __name__ == "__main__":

    # session_id = "test_session"
    session_config = {
        "configurable": {
            "session_id": "test_session_1"
        }
    }
    rag_service = RagService()
    question = "请问什么是RAG？"
    result = rag_service.chain.invoke({"input": question}, config=session_config)
    print(result)