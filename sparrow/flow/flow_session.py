# import asyncio
import websockets
from sparrow.agent.model import *
from sparrow.tool.tools import *
from sparrow.agent.handler import Handler
from sparrow.agent.consultant import Consultant
from sparrow.flow.meeting import meeting
from sparrow.flow.flow_util import *
import json


# tools = [magic_function, sparrow_websearch, sparrow_finsearch, sparrow_vectorsearch, sparrow_rag]
tools = []

handler = Handler("Handler", pop_model(), tools, sys_prompt="You are the CEO of a telecoms company. You run meetings efficiently, by facilitating discussion of agenda items and making concise proposals when they are required.")
fin = Consultant("Financial", pop_model(), [fin_costs], sys_prompt="You are a financial manager. You provide very succinct fact-based answers and recommendations, using tools where appropriate.")
ops = Consultant("Operational", pop_model(), [ops_costs], sys_prompt="You are an operations manager. You provide very succinct fact-based answers and recommendations, using tools where appropriate.")
pro = Consultant("Promotional", pop_model(), [pro_costs], sys_prompt="You are a marketing manager. You provide very succinct fact-based answers and recommendations, using tools where appropriate.")

consultants = [ops, pro, fin]


async def flow_session(websocket):
    try:
        # from urllib.parse import urlparse, parse_qs
        # print("path:", path)
        # parsed_path = urlparse(path)
        # query_params = parse_qs(parsed_path.query)
        # print(query_params)

        message = await websocket.recv()
        print(message)

        data = json.loads(message)
        flow = data['flow']
        agents = data['agents']
        agenda = [data['task']]

        attendees = []
        for agent in agents:
            for consultant in consultants:
                if agent == consultant.name:
                    attendees.append(consultant)

        try:
            if flow == "meeting":
                await meeting(websocket, "Meeting", agenda, handler, attendees)
            else:
                await send(websocket, handler.name, "Flow not recognised: " + flow)    
        except Exception as e:
            await send(websocket, handler.name, "" + repr(e))
        
        await websocket.close()        

    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed")


# start_server = websockets.serve(flow_session, "0.0.0.0", 8765)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
