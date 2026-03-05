from langchain_core.tools import tool

from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi

@tool(description="获取股票价格的工具, 输入股票名称")
def get_price(name: str) -> str:
    return f"股票{name}的价格是20元"

@tool(description="获取股票信息的工具, 输入股票名称")
def get_info(name: str) -> str:
    return f"股票{name}的基本信息是..."

agent = create_agent(
    model=ChatTongyi(model="qwen-max"),
    tools=[get_price, get_info],
    system_prompt="你是我的人工智能助手，请回答我的问题,告知我你的思考过程",
)

for chunk in agent.stream(
    {
    "messages": [
        {"role": "user", "content": "股票华为的价格,并介绍一下"}
    ]
    },
    stream_mode="values"
):
    latest_message = chunk["messages"][-1]

    if latest_message.content:
        print(type(latest_message).__name__, latest_message.content)

    try: 
        if latest_message.tool_calls:
            for tool_call in latest_message.tool_calls:
                print(f"工具调用: {tool_call.name}, 输入: {tool_call.args}, 输出: {tool_call.output}")
    except AttributeError as e:
        #print("没有工具调用")
        pass