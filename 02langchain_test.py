from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi

model = ChatTongyi(model = "qwen-max", temperature=0.8)

# example_template = PromptTemplate.from_template("What is the capital of {country}? {capital}") #创建一个简单的提示模板，使用占位符{country}和{capital}来表示需要替换的变量
# FewShotPromptTemplate(
#     example_prompt=example_template, #示例数据的模板
#     examples=None,                                          #示例数据
#     prefix="Answer the following questions:",               #前缀，示例前的提示词
#     suffix="What is the capital of Germany?",              #后缀，示例后的提示词
#     input_variables=["question"],                            #声明在前缀和后缀中使用的变量，这些变量将在调用时被替换为实际的值
# )

prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname}, 刚生了{gender}, 请起名"
)

chain = prompt | model | StrOutputParser()
 
res = chain.invoke({"lastname": "张", "gender": "男"})

print(res)
