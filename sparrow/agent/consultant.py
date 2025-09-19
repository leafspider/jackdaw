from sparrow.agent.model import *
from sparrow.tool.tools import *
from sparrow.agent.agent import Agent
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage
import asyncio
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.graph import CompiledGraph
from typing import List, Type


class Consultant(Agent):

    def __init__(s, name, model, tools, sys_prompt):        
        super().__init__(name, model, tools, sys_prompt)

        s.contacts: List = []
        s.config: dict = {"configurable": {"thread_id": "test-thread"}}
        s.agent_executor: Type[CompiledGraph] = create_react_agent(model, tools, state_modifier=sys_prompt, checkpointer=MemorySaver())
            
    # async def consult(s, agent, txt):
    #     messages = [HumanMessage(content=txt)]
    #     output_message = agent.invoke(messages) 
    #     output_message.name = agent.name
    #     return output_message

    async def consult(s, txt):
        messages = [SystemMessage(content=s.sys_prompt)] + [HumanMessage(content=txt)]
        # output_message = s.invoke(messages) 
        output_message = s.agent_executor.invoke( { "messages": messages }, s.config )["messages"][-1]
        output_message.name = s.name
        return output_message

    async def report(s, txt):
        # tasks = [contact.invoke(txt) for contact in s.contacts]        
        # tasks.append(s.invoke(txt))
        tasks = [contact.consult(txt) for contact in s.contacts]        
        tasks.append(s.consult(txt))
        return await asyncio.gather(*tasks)
    
    async def vote(s, proposal, minutes):
        task_prompt = f"In the context of the above discussion, vote on the following proposal. Your options are Yes, No or Abstain. Proposal: {proposal}"
        messages = [HumanMessage(content=minutes)] + [HumanMessage(content=task_prompt)]
        vote = await s.invoke(messages)
        if "Yes" in vote.content:
            vote.content = "Yes"
        elif "No" in vote.content:
            vote.content = "No"
        else:
            vote.content = "Abstain"
        return vote
        
    


if __name__ == '__main__':

    # tools = [magic_function, sparrow_websearch, sparrow_finsearch, sparrow_vectorsearch, sparrow_rag]
    tools = [sparrow_websearch]

    # name = "Bob"
    # sys_prompt = (
    #     "You are a data scientist providing answers and data visualisations to corporate executives. "
    # )
    # agent = Consultant(name, model, tools, sys_prompt)
    # print( agent.invoke("How many employees does Google have?") )
    # print( agent.invoke("What is the value of magic_function(number_of_employees)?") )

    fin = Consultant("Financial", pop_model(), tools, sys_prompt="You are a financial expert. You provide very succinct answers.")
    ops = Consultant("Operational", pop_model(), tools, sys_prompt="You are a operations expert. You provide very succinct answers.")
    pro = Consultant("Promotional", pop_model(), tools, sys_prompt="You are a marketing expert. You provide very succinct answers.")

    fin.contacts = [ops, pro]
    # ops.contacts = [fin, pro]
    # pro.contacts = [ops, fin]

    report = asyncio.run(fin.report("What impact do increased transportation costs have on your department?"))
    print("\n", report)
    