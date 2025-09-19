from sparrow.agent.model import *
from sparrow.tool.tools import *
from sparrow.agent.handler import Handler, Consultant
from sparrow.flow.flow_util import *


async def meeting(websocket, name: str, agenda: list[str], handler: Handler, attendees: list[Consultant]):

    # Start meeting
    para = name

    # List attendees
    para += " Attendees: " + handler.name
    for attendee in attendees:
        para += ", " + attendee.name

    await send(websocket, handler.name,para)
    minutes = para

    # Handle agenda
    item_num = 0
    for item in agenda:

        # Discuss item
        item_num += 1
        para = "Item "+ str(item_num) + ": " + item
        await send(websocket, handler.name, para)
        minutes += para

        # Consult attendees
        discussion = await handler.consult_attendees(item, attendees)
        for input in discussion:
            para = "Input (" + input.name + "): " + input.content
            await send(websocket, input.name, para)
            minutes += para

        # Summarize discussion
        summary = await handler.summarize_discussion(item, discussion)
        await send(websocket, handler.name, summary.content)
        minutes += summary.content

        # Make proposal
        proposal = await handler.make_proposal(summary)
        para = "Proposal: " + proposal.content
        await send(websocket, handler.name, para)
        minutes += para

        # Vote on proposal
        votes = await handler.gather_votes(proposal, attendees, minutes)
        for vote in votes:
            para = "Vote (" + vote.name + "): " + vote.content + "<br>"
            await send(websocket, vote.name, para)
            minutes += para

        # Count votes
        passed = await handler.proposal_passed(votes, attendees)
        if passed == False:
            para = "Proposal failed"
        else:
            # Delegate actions
            para = "Proposal passed"
            await send(websocket, handler.name, para)
            minutes += para
            
            delegation = await handler.delegate_actions(proposal, attendees)
            para = "Delegation: " + delegation.content
            actors = []
            for attendee in attendees:
                if attendee.name in delegation.content:
                    actors.append(attendee.name)
            para += "<br>Actions Delegated to (" + ", ".join(actors) + ")"

        await send(websocket, handler.name, para)
        minutes += para

    return minutes
    









async def hold_meeting(name: str, agenda, handler: Handler, attendees):
    
    # Start meeting
    minutes = name + "\n"
    minutes += "Minutes\n"
    minutes += "\nAttendees: " + handler.name

    # List attendees
    for attendee in attendees:
        minutes += ", " + attendee.name

    # Handle agenda
    item_num = 0
    for item in agenda:

        # Discuss item
        item_num += 1
        minutes += "\nItem "+ str(item_num) + ": " + item

        # Consult attendees
        discussion = await handler.consult_attendees(item, attendees)
        for input in discussion:
            minutes += "\nInput (" + input.name + "): " + input.content

        # Summarize discussion
        summary = handler.summarize_discussion(item, discussion)
        minutes += "\nSummary: " + summary.content

        # Make proposal
        proposal = handler.make_proposal(summary)
        minutes += "\nProposal: " + proposal.content

        # Vote on proposal
        votes = await handler.gather_votes(proposal, attendees, minutes)
        for vote in votes:
            minutes += "\nVote (" + vote.name + "): " + vote.content

        # Count votes
        passed = handler.proposal_passed(votes, attendees)

        # Delegate actions
        if passed == False:
            minutes += "\nProposal failed"
        else:
            minutes += "\nProposal passed"
            delegation = await handler.delegate_actions(proposal, attendees)
            minutes += "\nDelegation:\n" + delegation.content
            actors = []
            for attendee in attendees:
                if attendee.name in delegation.content:
                    actors.append(attendee.name)
            minutes += "\nProposed Actions Delegated to (" + ", ".join(actors) + ")"
            # handler.route_proposal(delegate, proposal)

    return minutes

