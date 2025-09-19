from sparrow.agent.model import *
import pytest, asyncio, os, config
from sparrow.tool.tools import *
from sparrow.agent.consultant import Consultant

model = pop_model()

# tools = [sparrow_websearch, sparrow_finsearch, sparrow_vectorsearch, sparrow_rag]
tools = []
fin_tools = []
ops_tools = [ops_costs]
pro_tools = [pro_costs]

async def test_invoke():
    
    ops = Consultant("Operational", model, ops_tools, sys_prompt="You are a operations expert. You provide very succinct answers and recommendations, using tools where necessary.")
    ops.contacts = []
    item = "What explanations are there for the fact that production costs have increased by 5%?"
    output = await ops.invoke([item])
    print(output)

async def test_consult():
    
    ops = Consultant("Operational", model, ops_tools, sys_prompt="You are a operations expert. You provide very succinct answers and recommendations, using tools where necessary.")
    ops.contacts = []

    item = "What explanations are there for the fact that production costs have increased by 5%?"
    output = await ops.consult(item)
    print(output)


async def test_report():
    
    fin = Consultant("Financial", model, tools, sys_prompt="You are a financial expert. You provide very succinct answers and recommendations, using tools where appropriate.")
    ops = Consultant("Operational", model, ops_tools, sys_prompt="You are a operations expert. You provide very succinct answers and recommendations, using tools where appropriate.")
    pro = Consultant("Promotional", model, pro_tools, sys_prompt="You are a marketing expert. You provide very succinct answers and recommendations, using tools where appropriate.")

    # fin.contacts = [ops, pro]
    # ops.contacts = [fin, pro]
    pro.contacts = [ops, fin]

    # item = "What impact do increased transportation costs have on your department?"
    item = "What explanations are there for the fact that monthly sales revenue has dropped by 5%?"

    report = await pro.report(item)
    print(report)

if __name__ == '__main__':
    
    # asyncio.run(test_invoke())
    # asyncio.run(test_consult())
    asyncio.run(test_report())
