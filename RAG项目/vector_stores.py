from langchain_chroma import Chroma
import config_data as config

class VectorStoreService(object):
    """
    向量存储服务类
    embedding: 嵌入模型传入，用于将文本转换为向量表示
    """
    def __init__(self, embedding):
        self.embedding = embedding  # 存储嵌入模型
        self.vector_store = Chroma(
            collection_name=config.collection_name,   #数据库表名
            embedding_function=self.embedding, #文本向量化函数
            persist_directory=config.persist_directory #数据库持久化目录
        )  # 初始化向量存储对象

    def get_retriever(self):
        # 获取向量存储的检索器对象,方便加入chain
        return self.vector_store.as_retriever(search_kwargs={"k": config.top_k})  # 返回向量存储的检索器对象, search_kwargs={"k": 2}表示检索时返回最相似的2条结果
    
    
if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    embedding = DashScopeEmbeddings(model="text-embedding-v4") # 创建一个DashScopeEmbeddings对象，指定使用"text-embedding-v4"模型进行文本向量化
    service = VectorStoreService(embedding) # 创建一个VectorStoreService对象，并将嵌入模型传入进行初始化
    retriever = service.get_retriever() # 获取向量存储的检索器对象
    res = retriever.invoke("测试文本") # 调用检索器对象的invoke方法，传入一个测试文本进行检索，返回最相似的结果列表并打印输出
    print(res)