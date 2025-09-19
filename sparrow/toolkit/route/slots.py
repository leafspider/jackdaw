from datetime import date, datetime, time, timedelta
import json

origin_address = "64 Mavety St, Toronto, ON"
max_journey_time = 20  # minutes


class Slot():

    def __init__(self, start_time, duration_mins, name, address):
        self.start_time = start_time
        self.end_time = start_time + timedelta(minutes=duration_mins)
        self.name = name
        self.address = address

    def __str__(self):
        start = self.start_time.strftime("%H:%M")
        end = self.end_time.strftime("%H:%M")
        return f"{start}-{end}: {self.name}, {self.address}"

    def to_json(self):
        return {
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "name": self.name,
            "address": self.address
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
        self.slots.append( Slot(start-timedelta(minutes=self.max_journey_time), 5, "Start", address=self.origin_address) )
        self.slots.append( Slot(end+timedelta(minutes=self.max_journey_time), 5, "End", address=self.origin_address) )
    
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
        if not slot in self.slots:
            print(f"Adding slot: {slot}")
            self.slots.append( slot )
            self.slots.sort(key=lambda slot: slot.start_time)

class Month():

    def __init__(self):
        self.days = []
        
        today = date.today()

        # Calculate the same day next month
        if today.month == 12:
            next_month_first = date(today.year + 1, 1, 1)
        else:
            next_month_first = date(today.year, today.month + 1, 1)

        dates = []
        current = today

        while current < next_month_first:
            if current.weekday() < 5:  # 0=Monday, 4=Friday                
                day = Day(start=datetime.combine(current, time(8,0,0)), end=datetime.combine(current, time(18,0,0)) )
                self.days.append(day)
            current += timedelta(days=1)

        print(dates)

    # def add_day(self, day):
    #     self.days.append( day )

    def add_slot(self, slot):
        for day in self.days:
            if day.date == slot.start_time.date():
                day.add_slot( slot )

    def to_json(self):
        month_json = { 
            "days": [
                day.to_json() for day in self.days
            ]
        }
        return month_json                

    def save(self, filename):
        # data = {
        #     "days": [
        #         {
        #             "name": day.name, 
        #             "date": str(day.date),
        #             "start": str(day.start),
        #             "end": str(day.end),
        #             "slots": [
        #                 {
        #                     "start_time": str(slot.start_time),
        #                     "end_time": str(slot.end_time),
        #                     "name": slot.name,
        #                     "address": slot.address
        #                 } for slot in day.slots
        #             ]
        #         } for day in self.days
        #     ]
        # }
        data = self.to_json()
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        self.days = []
        for day_data in data["days"]:
            day = Day(datetime.strptime(day_data["start"], "%Y-%m-%d %H:%M:%S"), datetime.strptime(day_data["end"], "%Y-%m-%d %H:%M:%S"))
            day.name = day_data["name"]
            day.slots = []
            for slot_data in day_data["slots"]:
                slot = Slot(datetime.strptime(slot_data["start_time"], "%Y-%m-%d %H:%M:%S"), 
                            (datetime.strptime(slot_data["end_time"], "%Y-%m-%d %H:%M:%S") - datetime.strptime(slot_data["start_time"], "%Y-%m-%d %H:%M:%S")).seconds // 60,
                            slot_data["name"],
                            slot_data["address"])
                day.slots.append( slot )
            self.days.append( day )
        self.days.sort(key=lambda day: day.start)

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

        