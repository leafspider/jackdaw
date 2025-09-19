import asyncio
from sparrow.monitor.base_monitor import BaseMonitor
from tests.agent.test_consultant import Consultant


class Monitor(BaseMonitor):

    def __init__(s, name="Monitor", data_source="DataSource"):
        s.name = name
        s.data_source = data_source
        pass

    async def observe(s, agents):
        # look for signals in data
        print( "\n:Monitoring:", s.data_source )        
        observation = "The ratings of comedy shows are falling sharply."
        print( ":Alert:", observation )
        tasks = [s.alert(observation, agent) for agent in agents]
        return await asyncio.gather(*tasks)    


if __name__ == '__main__':

    base_prompt = "You are a cosmetics company director. You answer succinctly when asked about the impact of observations on your department, giving specific recommendations."

    fin_agent = Consultant("Financial", sys_prompt=base_prompt + " Your expertise is Financial.")
    ops_agent = Consultant("Operational", sys_prompt=base_prompt + " Your expertise is Operational.")
    pro_agent = Consultant("Promotional", sys_prompt=base_prompt + " Your expertise is Promotional.")

    # fin_agent.agents = [ops_agent, pro_agent]
    # ops_agent.agents = [fin_agent, pro_agent]
    # pro_agent.agents = [ops_agent, fin_agent]

    agents = [fin_agent, ops_agent, pro_agent]

    ratings_monitor = Monitor(name="Ratings Monitor", data_source="Ratings Database")

    report = asyncio.run( ratings_monitor.observe(agents) )
    for msg in report:
        print(":" + msg.name, "Agent:", msg.content)
    # print(report)


# Agent
# 	query: get data or text
# 	decorate: decorate alert with local context
# 	report: send alert to handler
# 	consult: send alert to agent
	
# Handler
# 	report: display alert with global perspective
# 	research: support further inquiry
