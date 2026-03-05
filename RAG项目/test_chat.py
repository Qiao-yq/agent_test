from langchain_community.chat_models.tongyi import ChatTongyi
import config_data as config
chat=ChatTongyi(model=config.chat_model_name)
res=chat.invoke('hello')
print(type(res), res)
