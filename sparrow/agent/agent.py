from sparrow.agent.model import *
from sparrow.tool.tools import *
from langchain_core.messages import SystemMessage, HumanMessage
import asyncio
from langchain_core.language_models.chat_models import BaseChatModel
from typing import List, Type


class Agent:

    def __init__(s, name, model, tools, sys_prompt):
        s.name: str = name
        s.model: Type[BaseChatModel] = model
        s.tools: List = tools
        s.sys_prompt: str = sys_prompt
    
    async def invoke(s, messages):
        messages = [SystemMessage(content=s.sys_prompt)] + messages
        # output_message = s.agent_executor.invoke( { "messages": messages }, s.config )["messages"][-1]
        output_message = s.model.invoke(messages) 
        output_message.name = s.name
        return output_message   