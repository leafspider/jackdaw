from abc import abstractmethod


class BaseMonitor:

    agent = None

    def __init__(s):
        pass

    @abstractmethod
    async def observe(s, data_source, agent):
        # look for signals in data
        pass

    async def alert(s, observation, agent):
        # send an alert to an agent
        output = await agent.invoke(observation)
        output.observation = observation
        return output


# Agent
# 	query: get data or text
# 	decorate: decorate alert with local context
# 	report: send alert to handler
# 	consult: send alert to agent
	
# Handler
# 	report: display alert with global perspective
# 	research: support further inquiry
