from langchain.agents import create_agent
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
    
@tool (description="获取天气信息的工具")
def get_weather(location: str) -> str:
    # 模拟获取天气信息的函数
    return f"{location}今天晴，温度25度"

agent = create_agent(
    model=ChatTongyi(model="qwen-max"),
    tools=[get_weather],
    system_prompt="你是我的人工智能助手，请简洁、准确地回答我的问题",
)

res = agent.invoke(
    {
    "messages": [
        {"role": "user", "content": "今天大连天气如何"}
    ]
    }
)

for message in res["messages"]:
    print(type(message).__name__, message.content)