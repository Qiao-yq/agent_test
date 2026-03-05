"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
from langchain_chroma import Chroma



def check_md5(md5_str: str):
    """检查传入的文本是否已经存在于知识库中"""
    if not os.path.exists(config.md5_path): # 如果MD5文件不存在，说明知识库中没有任何文本，直接返回None
        open(config.md5_path, "w", encoding="utf-8").close() # 创建一个空的MD5文件
        return False
    else:
        for line in open(config.md5_path, "r", encoding="utf-8").readlines(): # 逐行读取MD5文件
            if line.strip() == md5_str: # 如果找到匹配的MD5值，说明文本已经存在于知识库中，返回True
                return True
        return False # 如果没有找到匹配的MD5值，说明文本不存在于知识库中，返回False

    

def save_md5(md5_str: str):
    """将新的文本和对应的MD5值保存到知识库中"""
    with open(config.md5_path, "a", encoding="utf-8") as f: # 以追加模式打开MD5文件
        f.write(md5_str + "\n") # 将新的MD5值写入文件，每个MD5值占一行

def get_string_md5(input_str: str, encoding="utf-8"):
    """计算传入文本的MD5值"""
    # 将输入字符串编码为字节流对象，并计算MD5值，返回16进制字符串形式的MD5值
    md5 = hashlib.md5() # 创建一个MD5对象
    md5.update(input_str.encode(encoding))
    return md5.hexdigest()

class KnowledgeBaseService(object):

    """知识库服务类，提供检查文本是否存在、保存文本和计算MD5值的功能"""
    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True) # 创建ChromaDB数据库持久化目录，如果目录已经存在则忽略

        self.chroma = Chroma(
            collection_name=config.collection_name,   #数据库表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"), #文本向量化函数
            persist_directory=config.persist_directory #数据库持久化目录
        ) # 初始化ChromaDB数据库连接对象


        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size, # 文本块大小
            chunk_overlap=config.chunk_overlap, # 文本块重叠部分大小
            separators=config.separators, # 文本分割符列表
            length_function=len # 计算文本长度的函数

        ) # 初始化文本分割器对象

    def update_by_str(self, data, filename):
        """将传入字符串进行向量化，存入向量数据库中"""
        md5_str = get_string_md5(data) # 计算传入文本的MD5值
        if check_md5(md5_str): # 检查文本是否已经存在于
            return "文本已经存在于知识库中 "
            
        if len(data) > config.max_split_char_number: # 如果文本长度超过最大字符数限制，进行文本分割
            text_chunks: list[str] = self.spliter.split_text(data) # 将文本分割成多个文本块
        else:       
            text_chunks = [data] # 如果文本长度没有超过最大字符数限制，直接将文本作为一个文本块

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "qyq"
        } # 创建文本块的元数据，包含文件名信息,创建时间和操作人信息

        self.chroma.add_texts(texts=text_chunks, metadatas=[metadata for _ in text_chunks]) # 将文本块和对应的元数据添加到ChromaDB数据库中

        save_md5(md5_str) # 将新的MD5值保存到MD5文件

        return "文本已成功添加到知识库中"

if __name__ == "__main__":
    service = KnowledgeBaseService() # 创建知识库服务对象
    test_str = "如果文本长度没有超过最大字符数限制，直接将文本作为一个文本块"
    result = service.update_by_str(test_str, "test.txt") # 将测试文本添加到知识库中
    print(result)

    