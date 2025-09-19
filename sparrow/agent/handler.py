from sparrow.agent.model import *
from sparrow.tool.tools import *
from sparrow.agent.agent import Agent
from sparrow.agent.consultant import Consultant
from langchain_core.messages import HumanMessage
import asyncio
# from sparrow.flow.meeting import meeting  # TODO: Fix this


class Handler(Agent):

    def __init__(s, name, model, tools, sys_prompt):
        super().__init__(name, model, tools, sys_prompt)
    
    async def invoke_attendees(s, item, attendees):
        tasks = [attendee.invoke([item]) for attendee in attendees]        
        return await asyncio.gather(*tasks) 
	
    async def consult_attendees(s, item, attendees):
        tasks = [attendee.consult(item) for attendee in attendees]        
        return await asyncio.gather(*tasks)

    async def summarize_discussion(s, item, messages):  #
        task_prompt = f"Summarize the preceding discussion of agenda item: {item}."
        messages = messages + [HumanMessage(content=task_prompt)]
        return await s.invoke(messages)
    
    async def make_proposal(s, summary):                #
        # return "Increase the advertising budget by 5%."
        task_prompt = f"Propose a course of action which arises from this discussion: {summary}."
        messages = [HumanMessage(content=task_prompt)]
        return await s.invoke(messages)
	
    async def gather_votes(s, proposal, voters, minutes):        
        tasks = [voter.vote(proposal.content, minutes) for voter in voters]        
        return await asyncio.gather(*tasks)

    async def proposal_passed(s, votes, attendees):     #
        num_votes = 1   # Handler votes Yes
        num_abstentions = 0
        for vote in votes:
            if "Yes" in vote.content:
                num_votes += 1
            elif "Abstain" in vote.content:
                num_abstentions += 1          
        passed = num_votes >= (len(attendees) - num_abstentions)/2
        return passed

    async def delegate_actions(s, proposal, attendees):    #
        task_prompt = "Attendees: "
        for attendee in attendees:
            task_prompt += "\nName: " + attendee.name + ", Role: "+ attendee.sys_prompt
        task_prompt += f"\nDecide which one of the above attendees is the best to lead in carrying out the following actions based on their role: {proposal}"
        messages = [HumanMessage(content=task_prompt)]
        return await s.invoke(messages)
    
    # async def hold_meeting(s, agenda, attendees):

    #     return await meeting(None, name="Board meeting", agenda=agenda, handler=s, attendees=attendees)

# from langchain_core.tools import tool
# @tool
# def query_change_in_labour_costs():
#     """Returns the lastest change in labour costs."""
#     return "Factory labour costs have increased by 10% over the past month."


if __name__ == '__main__':

    # tools = [magic_function, sparrow_websearch, sparrow_finsearch, sparrow_vectorsearch, sparrow_rag]
    tools = []
    
    fin = Consultant("Financial", pop_model(), tools, sys_prompt="You are a financial expert. You provide very succinct answers and recommendations, using tools where necessary.")
    ops = Consultant("Operational", pop_model(), [ops_costs], sys_prompt="You are a operations expert. You provide very succinct answers and recommendations, using tools where necessary.")
    pro = Consultant("Promotional", pop_model(), tools, sys_prompt="You are a marketing expert. You provide very succinct answers and recommendations, using tools where necessary.")
    handler = Handler("Handler(Chair)", pop_model(), tools, sys_prompt="You are the chair of a corporate board. You run board meetings efficiently, by facilitating discussion of agenda items and making proposals when they are required.")

    agenda = ["Production costs have increased by 5%"]
    # agenda = ["Sales have dropped by 5%"]
    attendees = [fin, ops, pro]
    # attendees = [pro]

    # minutes = asyncio.run(handler.hold_meeting(agenda, attendees))
    # print(minutes)

    # proposal = "Increase the advertising budget by 5%." 
    # delegate = handler.find_delegate(proposal, attendees)
    # print(delegate.content)

    discussion = asyncio.run(handler.consult_attendees("Production costs have increased by 5%", attendees))
    for input in discussion:
        print("Input (" + input.name + "): " + input.content)