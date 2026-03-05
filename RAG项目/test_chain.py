from rag import RagService
import config_data as config

session_config = {"configurable": {"session_id": "test_session_1"}}
rs = RagService()
res = rs.chain.invoke({"input": "test question"}, config=session_config)
print('result type', type(res))
print(res)
