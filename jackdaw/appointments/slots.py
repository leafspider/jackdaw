from datetime import date, datetime, time, timedelta
import json, os
import jackdaw.appointments.router as rt

origin_address = "64 Mavety St, Toronto, ON"
max_journey_time = 20  # minutes
default_start_hour = 8
default_end_hour = 18

router = rt.Router(origin_address)
month_file = router.folder + "month.json"

class Slot():

    def __init__(self, start_time, duration_mins, name, address, point=None):
        self.start_time = start_time
        self.end_time = start_time + timedelta(minutes=duration_mins)
        self.name = name
        self.address = address
        self.point = point if (point != None) else router.address_to_point(address)

    def __str__(self):
        start = self.start_time.strftime("%H:%M")
        end = self.end_time.strftime("%H:%M")
        return f"{start}-{end}: {self.name}, {self.address} ({self.point})"

    def to_json(self):
        return {
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "name": self.name,
            "address": self.address,
            "point": self.point
        }
    
class Day():

    def __init__(self, start, end):
        
        global origin_address, max_journey_time
        self.origin_address = origin_address
        self.max_journey_time = max_journey_time  # minutes
        self.date = start.date()
        self.name = self.date.strftime("%A")
        self.start = start
        self.end = end
        self.slots = []

        # self.slots.append( Slot(start-timedelta(minutes=self.max_journey_time), 5, "Start", address=self.origin_address) )
        # self.slots.append( Slot(end+timedelta(minutes=self.max_journey_time), 5, "End", address=self.origin_address) )
    
    def __str__(self):
        return f"{self.name} {self.date}"

    def to_json(self):

        day_json = { "name": self.name, 
            "date": str(self.date),
            "start": str(self.start),
            "end": str(self.end),
            "slots": [
                slot.to_json() for slot in self.slots
            ]
        }
        return day_json                    

    def add_slot(self, slot):
        if slot in self.slots:
            return None, f"Slot already exists: {slot}"
        else:
            self.slots.append( slot )
            self.slots.sort(key=lambda slot: slot.start_time)
            return slot, "ok"

class Month():

    def __init__(self):
        
        print("Month.init()")
        
        self.days = []
        
        if os.path.exists(month_file):
            self.load()
            print("Month loaded: days in month:", len(self.days))
        
        today = date.today()
        last_bookable_date = today + timedelta(days=30)

        current = today

        print("Month init dates:")

        while current < last_bookable_date:
            if current.weekday() < 5:           # 0=Monday, 4=Friday

                day_start = datetime.combine(current, time(default_start_hour,0,0))
                day_end = datetime.combine(current, time(default_end_hour,0,0))

                if any(loaded_day.date == day_start.date() for loaded_day in self.days):
                    print(f"Day exists: {current}")                    
                    break
                else:
                    print(f"Day doesn't exist: {current}")
                    day = Day(day_start, day_end)
                    day.slots.append( Slot(day_start-timedelta(minutes=max_journey_time), 5, "Start", address=origin_address, point=router.origin_point) )
                    day.slots.append( Slot(day_end+timedelta(minutes=max_journey_time), 5, "End", address=origin_address, point=router.origin_point) )
                    self.days.append(day)
                    print(f"Appended {day.date}")
            current += timedelta(days=1)

    def add_slot(self, slot):
        for day in self.days:
            if day.date == slot.start_time.date():
                return day.add_slot( slot )

    def to_json(self):
        month_json = { 
            "days": [
                day.to_json() for day in self.days
            ]
        }
        return month_json                

    def save(self, filename=month_file):
        data = self.to_json()
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load(self, filename=month_file):

        with open(filename, 'r') as f:
            data = json.load(f)

        if self.days == None:
            self.days = []

        for day_data in data["days"]:
            day = Day(datetime.strptime(day_data["start"], "%Y-%m-%d %H:%M:%S"), datetime.strptime(day_data["end"], "%Y-%m-%d %H:%M:%S"))
            day.name = day_data["name"]
            
            day.slots = []
            for slot_data in day_data["slots"]:
                slot = Slot(datetime.strptime(slot_data["start_time"], "%Y-%m-%d %H:%M:%S"), 
                            (datetime.strptime(slot_data["end_time"], "%Y-%m-%d %H:%M:%S") - datetime.strptime(slot_data["start_time"], "%Y-%m-%d %H:%M:%S")).seconds // 60,
                            slot_data["name"],
                            slot_data["address"],
                            slot_data.get("point", None))
                day.slots.append( slot )
            self.days.append( day )

        self.days.sort(key=lambda day: day.start)
        
        # print("--- loading slots ---")
        # self.print()

    def print(self):
        
        for day in self.days:
            print(day)
            for slot in day.slots:
                print(slot)


if __name__ == '__main__':

    import calendar
    cal = calendar.Calendar()
    year = 2025
    month = 9
    for day in cal.itermonthdates(year, month):
        print(day)
    cal_text = calendar.month(year, month)
    print(cal_text)

        