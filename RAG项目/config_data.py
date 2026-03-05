md5_path = "./md5.txt" # 存储MD5值的文件路径

# Chroma
collection_name = "rag" # ChromaDB数据库表名
persist_directory = "./chroma_db" # ChromaDB数据库持久化目录


chunk_size = 1000 # 文本块大小
chunk_overlap = 100 # 文本块重叠部分大小
separators = ["\n\n", "\n", " ", "", "!", "?", ".", "。", "，"] # 文本分割符列表

max_split_char_number = 1000 # 文本分割时，单个文本块的最大字符数

#
top_k = 2 # 向量检索时返回最相似的结果数量

embedding_model_name = "text-embedding-v4" # 用于生成文本向量的模型名称
chat_model_name = "qwen-max" # 用于生成回答的聊天模型名称


session_config = {
        "configurable": {
            "session_id": "test_session_1"
        }
    }