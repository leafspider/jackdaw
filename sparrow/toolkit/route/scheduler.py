import sparrow.toolkit.route.slots as sl
import sparrow.toolkit.route.router as rt
import sparrow.toolkit.route.directions as di
from datetime import date, datetime, timedelta
import os

router = rt.Router(sl.origin_address)

class Scheduler():

    def __init__(self):
        
        month = sl.Month()  
        file = router.folder + "month.json"
        if os.path.exists(file):
            month.load( router.folder + "month.json" )
            print("--------------")
            month.print()
            print("--------------")
        self.month = month

    def available_slots(self, date, duration_mins, name, address):

        print(f"Looking for a {duration_mins} min appointment on {date} with {name} at {address}")

        point = router.address_to_point(address)

        available_slots = []

        # Check it's on the map
        travel_time_origin = router.travel_time( router.origin_point, point )
        if travel_time_origin > sl.max_journey_time: 
            print(f"No slots available, time from origin > {sl.max_journey_time} mins")
            return available_slots

        for day in self.month.days:
            # print( f"{day.name} {day.date}" )
            
            if day.date == date:
                
                for this_slot in day.slots:
                    if( this_slot.name == "End" ):
                        break
                    next_slot = day.slots[ day.slots.index(this_slot)+1 ]
                    range = self.check_gap(this_slot, next_slot, duration_mins, point)                                                                        

                    if range != None:
                        candidate_slots = []    # Only need 1st and last slots in the gap
                        range_start, range_end = range
                        print("Range:", range_start.strftime("%H:%M"), range_end.strftime("%H:%M"))

                        start_time = self.round_up_to_nearest_15(range_start)
                        while start_time + timedelta(minutes=duration_mins) <= range_end:                  
                            candidate_slots.append( sl.Slot( start_time, duration_mins, name, address ) )
                            start_time += timedelta(minutes=15)

                        if len(candidate_slots) > 0:
                            available_slots.append( candidate_slots[0] )
                        if len(candidate_slots) > 1:
                            available_slots.append( candidate_slots[-1] )

        print(f"Found {len(available_slots)} available slots" )

        return available_slots

    def check_gap(self, slot, next_slot, duration_mins, new_point):
        
        # print( f"Gap: {slot.name}, {next_slot.name}" )

        point1 = router.address_to_point(slot.address)                    
        travel_time1 = router.travel_time( point1, new_point )

        point2 = router.address_to_point(next_slot.address)                    
        travel_time2 = router.travel_time( new_point, point2 )

        print(f"Travel times {travel_time1:.0f} min and {travel_time2:.0f} min")
        
        range_start = slot.end_time + timedelta(minutes=travel_time1)
        range_end = next_slot.start_time - timedelta(minutes=travel_time2)

        if range_end - range_start < timedelta(minutes=duration_mins):
            print(f"No time between {slot.name} and {next_slot.name}")
            return None
        else:
            print(f"Gap between {slot.name} and {next_slot.name}")            
            return (range_start, range_end)

    def round_up_to_nearest_15(self, dt):
        # Calculate minutes to add
        minutes_to_add = (-(dt.minute % 15) + 15) % 15
        if minutes_to_add:
            dt += timedelta(minutes=minutes_to_add)
        # Zero out seconds and microseconds
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
        return nads

    def example1(self):

        slots = self.available_slots( date(2025,9,10), 45, "Sandra Mason", "575 St Clarens Ave, Toronto, ON" )

        print("--------------")
        print(f"Found {len(slots)} available slots")
        for slot in slots:
            print(slot)   
        self.month.add_slot( slots[0] )
        print("--------------")

        slots = self.available_slots( date(2025,9,10), 60, "Jennifer Saunders", "101 Armstrong Ave, Toronto, ON" )
        print("--------------")
        print(f"Found {len(slots)} available slots")
        for slot in slots:
            print(slot)
        self.month.add_slot( slots[0] )
        print("--------------")

        self.scheduler.month.save( router.folder + "month.json" )

        route_latlongs = self.day_slots_latlong( date(2025,9,10) )            # TODO Use slot points to keep # of waypoints to 25 max !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        return route_latlongs

    def example2(self):

        slots = self.available_slots( date(2025,9,10), 45, "Sandra Mason", "575 St Clarens Ave, Toronto, ON" )

        print("--------------")
        print(f"Found {len(slots)} available slots")
        for slot in slots:
            print(slot)   
        self.month.add_slot( slots[0] )
        print("--------------")

        slots = self.available_slots( date(2025,9,10), 60, "Jennifer Saunders", "101 Armstrong Ave, Toronto, ON" )
        print("--------------")
        print(f"Found {len(slots)} available slots")
        for slot in slots:
            print(slot)
        self.month.add_slot( slots[0] )
        print("--------------")

        # selfscheduler.month.save( router.folder + "month.json" )

        route_latlongs = self.day_route_latlong( date(2025,9,10) )
        
        return route_latlongs
    
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
        