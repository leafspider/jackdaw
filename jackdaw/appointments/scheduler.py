import jackdaw.appointments.slots as sl
import jackdaw.appointments.router as rt
from datetime import date, datetime, timedelta
import os
import jackdaw.appointments.directions as di

router = rt.Router(sl.origin_address)

class Scheduler():

    def __init__(self):
        
        self.month = sl.Month()  

    def get_point(self, address):
        for day in self.month.days:
            for slot in day.slots:
                if slot.address == address:
                    if slot.point != None:
                        return slot.point
        return router.address_to_point(address)

    def available_slots(self, date, duration_mins, name, address):

        # print(f"Looking for a {duration_mins} min appointment on {date} with {name} at {address}")

        point = self.get_point(address)

        available_slots = []

        # Check it's on the map
        travel_time_origin = router.travel_time( router.origin_point, point )
        if travel_time_origin > sl.max_journey_time: 
            status = f"No appointments available (outside catchment area)"
            return available_slots, status

        for day in self.month.days:
            
            if day.date == date:
                
                for this_slot in day.slots:

                    if( this_slot.name == "End" ):
                        break
                    
                    next_slot = day.slots[ day.slots.index(this_slot)+1 ]
                    
                    if( this_slot.name == name ):
                        available_slots.append( this_slot )
                        # continue

                    range, status = self.check_gap(this_slot, next_slot, duration_mins, point)                                                                        

                    if range != None:
                        candidate_slots = []    # Only need 1st and last slots in the gap
                        range_start, range_end = range
                        print(status, ", Available range:", range_start.strftime("%H:%M"), range_end.strftime("%H:%M"))

                        start_time = self.round_up_to_nearest_15(range_start)
                        
                        while start_time + timedelta(minutes=duration_mins) <= range_end:                  
                            # available_slots.append( sl.Slot( start_time, duration_mins, '', address, point ) )
                            candidate_slots.append( sl.Slot( start_time, duration_mins, '', address, point ) )
                            start_time += timedelta(minutes=15)

                        if len(candidate_slots) > 0:
                            available_slots.append( candidate_slots[0] )
                        if len(candidate_slots) > 1:
                            available_slots.append( candidate_slots[-1] )

                    else:
                        print(status)

        print(f"Found {len(available_slots)} available slots" )

        return available_slots, "ok"

    def available_slots_exclusive(self, date, duration_mins, name, address):

        # print(f"Looking for a {duration_mins} min appointment on {date} with {name} at {address}")

        point = router.address_to_point(address)

        available_slots = []

        # Check it's on the map
        travel_time_origin = router.travel_time( router.origin_point, point )
        if travel_time_origin > sl.max_journey_time: 
            status = f"No slots available, outside catchment area."
            return available_slots, status

        for day in self.month.days:
            
            if day.date == date:
                
                for this_slot in day.slots:

                    if( this_slot.name == "End" ):
                        break
                    # elif( this_slot.name == name ):
                    #     this_slot.name = "Your booking"
                    #     available_slots.append( this_slot )
                    #     continue

                    next_slot = day.slots[ day.slots.index(this_slot)+1 ]
                    
                    range = self.check_gap(this_slot, next_slot, duration_mins, point)                                                                        

                    if range != None:
                        candidate_slots = []    # Only need 1st and last slots in the gap
                        range_start, range_end = range
                        print("Available range:", range_start.strftime("%H:%M"), range_end.strftime("%H:%M"))

                        start_time = self.round_up_to_nearest_15(range_start)
                        
                        while start_time + timedelta(minutes=duration_mins) <= range_end:                  
                            candidate_slots.append( sl.Slot( start_time, duration_mins, name, address, point ) )
                            start_time += timedelta(minutes=15)

                        if len(candidate_slots) > 0:
                            available_slots.append( candidate_slots[0] )
                        if len(candidate_slots) > 1:
                            available_slots.append( candidate_slots[-1] )

        print(f"Found {len(available_slots)} available slots" )

        return available_slots

    def check_gap(self, slot, next_slot, duration_mins, new_point):
        
        # print( f"Gap: {slot.name}, {next_slot.name}" )

        point1 = slot.point                   
        travel_time1 = router.travel_time( point1, new_point )

        point2 = next_slot.point                   
        travel_time2 = router.travel_time( new_point, point2 )

        # print(f"Travel times {travel_time1:.0f} min and {travel_time2:.0f} min")
        
        range_start = slot.end_time + timedelta(minutes=travel_time1)
        range_end = next_slot.start_time - timedelta(minutes=travel_time2)

        if range_end - range_start < timedelta(minutes=duration_mins):
            return None, f"No gap between {slot.name} and {next_slot.name}"
        else:
            return (range_start, range_end), f"Gap between {slot.name} and {next_slot.name}"

    def round_up_to_nearest_15(self, dt):
        minutes_to_add = (-(dt.minute % 15) + 15) % 15
        if minutes_to_add:
            dt += timedelta(minutes=minutes_to_add)
        dt = dt.replace(second=0, microsecond=0)
        return dt

    def round_down_to_nearest_15(self, dt):
        minutes_to_add = ((-(dt.minute % 15) + 15) % 15) - 15
        if minutes_to_add:
            dt += timedelta(minutes=minutes_to_add)
        dt = dt.replace(second=0, microsecond=0)
        return dt

    def day_route(self, date ):
        day_nodes = []
        for day in self.month.days:
            if day.date == date:
                for slot in day.slots:
                    if slot.name not in ["End"]:
                        point = router.address_to_point(slot.address)
                        next_slot = day.slots[ day.slots.index(slot)+1 ]
                        next_point = router.address_to_point(next_slot.address)
                        print(f"Add route from {slot.name} to {next_slot.name}")
                        nodes = router.route( point, next_point )
                        
                        # fig, ax = router.map( nodes)

                        day_nodes += nodes

        # Remove duplicates
        deduped_nodes = [day_nodes[i] for i in range(len(day_nodes)) if i == 0 or day_nodes[i] != day_nodes[i-1]]

        return deduped_nodes

    def day_route_latlong(self, date ):
        day_latlong = []
        node_ids = self.day_route( date )
        for node_id in router.hood_graph.nodes:
            if node_id in node_ids:
                node = router.hood_graph.nodes[node_id]
                day_latlong.append( (node['y'], node['x']) )
        return day_latlong

    def day_slots_latlong(self, date ):
        day_latlong = []
        node_ids = self.day_route( date )
        for node_id in router.hood_graph.nodes:
            if node_id in node_ids:
                node = router.hood_graph.nodes[node_id]
                day_latlong.append( (node['y'], node['x']) )
        return day_latlong    
    
    def day_points(self, date):
        points = []
        for day in self.month.days:
            if day.date == date:
                for slot in day.slots:
                    points.append( router.address_to_point(slot.address) )
        return points

    def day_latlong(self, date):
        points = self.day_points(date)
        latlong = []
        for point in points:
            latlong.append( (point[0], point[1]) )
        return latlong

    def day_names_and_addresses(self, date):
        nads = []
        for day in self.month.days:
            if day.date == date:
                for slot in day.slots:
                    nads.append( (slot.name, slot.address) )
        # print("len(nads):", len(nads))
        
        if len(nads) < 1: 
            nads = [('Start', sl.origin_address), ('End', sl.origin_address)]
        return nads
 
    def save_slot(self, start_time, duration_mins, name, address, point=None):

        # for day in self.month.days:
        #     if day.date == start_time.date():
        #         for slot in day.slots:                   
        #             if slot.name == name:
        #                 day.slots.remove(slot)
        #                 # break

        slot = sl.Slot(start_time, duration_mins, name, address, point)

        added, status = self.month.add_slot( slot )
        # print(status)
        if added:            
            self.month.save()

        return slot, status

    def delete_slot(self, start_time, name):

        status = False
        for day in self.month.days:
            if day.date == start_time.date():
                for slot in day.slots:                   
                    if slot.name == name:
                        day.slots.remove(slot)
                        status = True
                        self.month.save()
        
        return status

    def booked_slots(self, date, name=None):

        booked_slots = []

        for day in self.month.days:
            
            if day.date == date:
                
                for this_slot in day.slots:
                    if( this_slot.name == "Start" or this_slot.name == "End" ):
                        continue
                    if name == None or this_slot.name == name:
                        booked_slots.append( this_slot )

        print(f"Found {len(booked_slots)} booked slots" )

        return booked_slots

    def all_booked_slots(self):

        booked_slots = []

        for day in self.month.days:            
            for this_slot in day.slots:
                if( this_slot.name == "Start" or this_slot.name == "End" ):
                    continue
                booked_slots.append( this_slot )

        print(f"Found all {len(booked_slots)} booked slots" )

        return booked_slots

    def get_directions(self, date):
        
        nads = self.day_names_and_addresses( date )
        return di.directions_from_addresses(nads)
    
if __name__ == '__main__':

    scheduler = Scheduler()

    latlongs = scheduler.day_latlong( date(2025,9,10) )
    print("Latlongs:", latlongs)

    exit()

    slots = scheduler.available_slots( date(2025,9,10), 45, "Sandra Mason", "575 St Clarens Ave, Toronto, ON" )

    print("--------------")
    print(f"Found {len(slots)} available slots")
    for slot in slots:
        print(slot)   
    scheduler.month.add_slot( slots[0] )
    print("--------------")

    slots = scheduler.available_slots( date(2025,9,10), 60, "Jennifer Saunders", "101 Armstrong Ave, Toronto, ON" )
    print("--------------")
    print(f"Found {len(slots)} available slots")
    for slot in slots:
        print(slot)
    scheduler.month.add_slot( slots[0] )
    print("--------------")

    # scheduler.month.save( router.folder + "month.json" )

    route_nodes = scheduler.day_route( date(2025,9,10) )
    # print(f"Route nodes: {route_nodes}")

    fig, ax = router.map( route_nodes)
    fig.savefig( router.folder + "route_map.png")

    print("--------------")
    scheduler.month.print()
        