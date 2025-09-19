from sparrow.agent.model import *
from sparrow.tool.tools import *
from sparrow.agent.agent import Agent
from langchain_core.messages import HumanMessage
from typing import List
import asyncio
import sparrow.toolkit.kgraph.chunker as chunker


class Ontologist(Agent):

    def __init__(s, name, model, tools, sys_prompt):
        super().__init__(name, model, tools, sys_prompt)
    
    async def export_kgraph(s, text: str):

        chunks: List[str] = chunker.chunk(text)    
        messages = []
        for chunk in chunks:
            task_prompt = f"Export the following text to knowledge graph in OWL format: {chunk}"
            messages.append( [HumanMessage(content=task_prompt)] )
        tasks = [s.invoke(message) for message in messages]        
        res = await asyncio.gather(*tasks)
        return res


if __name__ == '__main__':

    tools = []
    text = "Create a plot of the number of full time employees at the 3 tech companies with the highest market cap in 2024."

    agent = Ontologist("Ontologist", pop_model(), tools, sys_prompt="You are an ontologist. You create ontologies.")

    print("Running " + type(agent).__name__)
    print( asyncio.run( agent.export_kgraph(text) )[0].content )