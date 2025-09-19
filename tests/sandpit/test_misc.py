# import asyncio, pytest 

# 

class Solution:
    def mergeTwoLists(self, l1, l2):
        print(type(l1))
        if l1 is None:
            return l2
        elif l2 is None:
            return l1
        elif l1[0] < l2[0]:
            return self.mergeTwoLists(l1[1:], l2)
        else:
            return self.mergeTwoLists(l1, l2[1:])
        

if __name__ == '__main__':

    sol = Solution()
    l1 = [1,2,4]
    l2 = [1,3,4]

    res = sol.mergeTwoLists(l1, l2)
    print(res)    