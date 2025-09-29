import jackdaw.scheduler.slots as sl
from datetime import date, datetime, time
import jackdaw.scheduler.router as rt


router = rt.Router(sl.origin_address)

def test_add_slots():

    month = sl.Month()    
    # wednesday = sl.Day(start=datetime(2025,9,10,8,0), end=datetime(2025,9,10,18,0) )
    month.add_slot( sl.Slot( datetime(2025,9,10,9,0), 60, "Joe Taylor", "274 Campbell Ave, Toronto, ON" ) )
    month.add_slot( sl.Slot( datetime(2025,9,10,11,0), 45, "Fred Butcher", "23 Glenlake Ave, Toronto, ON" ) )
    month.add_slot( sl.Slot( datetime(2025,9,10,15,0), 30, "John Smith", "575 Indian Rd, Toronto, ON" ) )
    # month.add_day( wednesday )
    month.print()

def test_save_slots():

    month = sl.Month()  
    today = date.today()  
    month.add_slot( sl.Slot( datetime.combine(today, time(8,0,0)), 60, "Sandra Brown", "575 St Clarens Ave, Toronto, ON" ) )
    # month.add_slot( sl.Slot( datetime.combine(today, time(10,0,0)), 45, "Jennifer Mason", "451 Pacific Ave, Toronto, ON" ) )
    # month.add_slot( sl.Slot( datetime.combine(today, time(16,0,0)), 30, "Wendy Carson", "9 Armadale Ave, Toronto, ON" ) )
    month.save( router.folder + "month.json" )
    month.print()

def test_load_slots():

    month = sl.Month()    
    month.load( router.folder + "month.json" )
    month.print()


if __name__ == '__main__':

    # test_save_slots()
    test_load_slots()

    # month = sl.Month()    
    # month.load( router.folder + "month.json" )
    # month.print()

    # app = sl.Slot( datetime(2025,9,10,8,30), 60, "Sandra Mason", "575 St Clarens Ave, Toronto, ON" )
    # point = router.address_to_point(app.address)

    # distance1, travel_time_origin = router.distance_and_time( router.origin_point, point )

    # # Is it on the map?
    # if travel_time_origin > router.max_journey_time: 
    #     on_map = False 
    # else: 
    #     on_map = True
        
    # if on_map == False:
    #     print(f"Time from origin > {router.max_journey_time} mins") 
    # else:
    #     print(f"Appointment added")
    #     wednesday.add_slot( app1 )

    # # address1 = "23 Glenlake Ave, Toronto, ON"
    # # point1 = router.address_to_point(address1)
    # # distance, travel_time = router.distance_and_time( router.origin_point, point1 )
    # # print(f"Travel time: {travel_time:.3f} min", f"Distance: {distance:.3f} km")

    # # address2 = "1246 Yonge St, Toronto, ON"
    # # point2 = router.address_to_point(address2)
    # # distance, travel_time = router.distance_and_time( point1, point2 )
    # # print(f"Travel time: {travel_time:.3f} min", f"Distance: {distance:.3f} km")

    # print(wednesday)
    # for slot in wednesday.slots:
    #     print(slot)

    # month = sl.Month()    
    # month.add_day( wednesday )
    # month.save( router.folder + "month.json" )
    # data = month.load( router.folder + "month.json" )
    # print(data)

