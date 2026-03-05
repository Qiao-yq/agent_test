from langchain.agents import create_agent, AgentState
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, wrap_tool_call
from langgraph.runtime import Runtime
    
@tool (description="获取天气信息的工具")
def get_weather(location: str) -> str:
    # 模拟获取天气信息的函数
    return f"{location}今天晴，温度25度"

"""

"""
@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[before agent] {len(state['messages'])}")

@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[after agent] {len(state['messages'])}")

@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[before model] {len(state['messages'])}")

@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[after model] {len(state['messages'])}")

@wrap_model_call
def model_call_hook(request, handler):
    print("模型调用了")
    return handler(request)

@wrap_tool_call
def monitor_tool(request, handler):
    print(f"工具执行：{request.tool_call['name']}")
    print(f"传入参数：{request.tool_call['args']}")
    return handler(request)


agent = create_agent(
    model=ChatTongyi(model="qwen-max"),
    tools=[get_weather],
    middleware=[log_before_agent, log_after_agent, log_before_model, log_after_model, model_call_hook, monitor_tool],
    #system_prompt="你是我的人工智能助手，请简洁、准确地回答我的问题",
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

