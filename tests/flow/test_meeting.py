from sparrow.agent.model import *
from sparrow.tool.tools import *
from sparrow.agent.handler import Handler
from sparrow.agent.consultant import Consultant
from sparrow.flow.meeting import *
import pytest, asyncio

model = pop_model()

async def test_meeting():

    # tools = [magic_function, sparrow_websearch, sparrow_finsearch, sparrow_vectorsearch, sparrow_rag]
    tools = []
    
    handler = Handler("Chair", model, tools, sys_prompt="You are the chair of the corporate board for a telecoms company. You run board meetings efficiently, by facilitating discussion of agenda items and making proposals when they are required.")
    fin = Consultant("Financial", model, tools, sys_prompt="You are a financial expert. You provide very succinct answers and recommendations, using tools where appropriate.")
    ops = Consultant("Operational", model, [ops_costs], sys_prompt="You are a operations expert. You provide very succinct answers and recommendations, using tools where appropriate.")
    pro = Consultant("Promotional", model, [pro_costs], sys_prompt="You are a marketing expert. You provide very succinct answers and recommendations, using tools where appropriate.")

    # agenda = ["Sales have dropped by 5%"]
    agenda = ["Our production costs have increased by 5% per unit over the last month"]
    consultants = [fin, ops, pro]

    minutes = await hold_meeting("Board Meeting", agenda, handler, consultants)
    print(minutes)

    # proposal = "Increase the advertising budget by 5%." 
    # delegate = handler.delegate_actions(proposal, attendees)
    # print(delegate.content)


if __name__ == '__main__':
    
    asyncio.run(test_meeting())