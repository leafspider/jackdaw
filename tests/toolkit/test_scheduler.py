import sparrow.toolkit.route.scheduler as sc
import sparrow.toolkit.route.slots as sl
import sparrow.toolkit.route.router as rt
from datetime import datetime, timedelta

origin_address = sl.origin_address
router = rt.Router(origin_address)

def test_add_slots():

    scheduler = sc.Scheduler()

    scheduler.month.add_slot( sl.Slot( datetime(2025,9,10,8,0), 30, "Sandra Mason", "575 St Clarens Ave, Toronto, ON" ) )
    scheduler.month.add_slot( sl.Slot( datetime(2025,9,10,8,0), 30, "Jennifer Mason", "451 Pacific Ave, Toronto, ON" ) )
    scheduler.month.add_slot( sl.Slot( datetime(2025,9,10,10,0), 60, "Wendy Carson", "9 Armadale Ave, Toronto, ON" ) )
    scheduler.month.add_slot( sl.Slot( datetime(2025,9,10,16,15), 30, "Bridget Jones", "18 Ostend Ave, Toronto, ON" ) )


if __name__ == '__main__':

    test_add_slots()


