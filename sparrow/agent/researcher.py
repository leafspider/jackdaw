from sparrow.agent.model import *
from sparrow.tool.tools import *
from langchain.agents import AgentExecutor
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_core.prompts import ChatPromptTemplate

class Researcher:

    key_picker = 0

    def __init__(s):
        
        # s.tools = [sparrow_websearch, sparrow_finsearch, sparrow_vectorsearch, sparrow_embed, ops_costs, pro_costs]
        s.tools = [sparrow_websearch, sparrow_finsearch]
        s.sys_prompt = (
            "You are a data scientist providing answers and data visualisations to corporate executives. "
            "Use thoughts, actions and observations until you are satisfied you have a full answer. "
            "You may need to search the web for information like the ticker for a company. Remember that company financial data is usually absent at the weekend. "
            "Data series output should be provided as a {{\"chart\"}} json object valid for highcharts.js for example {{\"chart\": {{}},\"title\": {{}},\"xAxis\": {{}},\"yAxis\": {{}},\"series\": []}}"
            #"If you must provide results in a table, they should be in HTML table format. "
        )
        s.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", s.sys_prompt),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
                #MessagesPlaceholder("{agent_scratchpad}"),
            ]
        )
        
        if Researcher.key_picker % 2 == 0:
            cohere_api_key = os.environ['COHERE_API_KEY1']
        else:
            cohere_api_key = os.environ['COHERE_API_KEY2']
        Researcher.key_picker += 1

        print("key", cohere_api_key)

        model = ChatCohere(model="command-r-plus", temperature=0, cohere_api_key=cohere_api_key)

        agent = create_cohere_react_agent(llm=model, tools=s.tools, prompt=s.prompt)
        s.agent_executor = AgentExecutor(agent=agent, tools=s.tools, verbose=True)

    def invoke(s, task_prompt):
        res = s.agent_executor.invoke({"input": task_prompt})
        output = res['output'].replace("`", "").replace("json", "").replace(" ", " ")       # replace("\n", "")
        # print(output)
        return output

if __name__ == '__main__':

    task = "Create a plot of the number of full time employees at the 3 tech companies with the highest market cap in 2024."
    #task = "How many employees did Google have in 2023?"

    agent = Researcher()

    print("Running " + type(agent).__name__)
    print(agent.invoke(task))
