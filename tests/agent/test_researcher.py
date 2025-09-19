from sparrow.agent.model import *
import asyncio, pytest 

from sparrow.agent.researcher import Researcher

model = pop_model()

async def test_cohere():

    task = "Create a plot of the number of full time employees at the 3 tech companies with the highest market cap in 2024."
    #task = "How many employees did Google have in 2023?"

    agent = Researcher()

    print("Running " + type(agent).__name__)
    res = agent.invoke(task)
    print(res)

    assert len(res.search_results) > 0



if __name__ == '__main__':

    asyncio.run(test_cohere())

    class Solution:
        def mergeTwoLists(self, l1, l2):
            if l1 is None:
                return l2
            elif l2 is None:
                return l1
            elif l1.val < l2.val:
                l1.next = self.mergeTwoLists(l1.next, l2)
                return l1
            else:
                l2.next = self.mergeTwoLists(l1, l2.next)
                return l2