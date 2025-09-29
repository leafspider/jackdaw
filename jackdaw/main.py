import config
import os, asyncio, ssl
from flask import Flask, request, render_template, redirect
import multiprocessing
import jackdaw.appointments.scheduler as sc
import jackdaw.appointments.router as rt
import jackdaw.appointments.slots as sl
from datetime import date, datetime


app = Flask(__name__)

flow_host = os.getenv("FLOW_HOST")
flow_port = os.getenv("FLOW_PORT")
page_port = os.getenv("PAGE_PORT")

scheduler = sc.Scheduler()
router = rt.Router(sl.origin_address)

# --------------------------

@app.route('/')
def index_page():
    return redirect('/scheduler')

@app.route('/scheduler')
def scheduler_page():
    API_KEY = os.environ['GOOGLE_ROUTER_API_KEY']
    return render_template('t-scheduler.html', API_KEY=API_KEY)

@app.route('/scheduler-available-slots')
def scheduler_available_slots():
    
    date_st = request.args.get('date')
    # print("scheduler-available-slots.date_st:", date_st)
    duration = int(request.args.get('duration'))
    name_st = request.args.get('name')
    address_st = request.args.get('address')

    parsed_date = datetime.strptime(date_st, "%Y-%m-%d").date()
    slots, status = scheduler.available_slots(parsed_date, duration, name_st, address_st)
    print("available slots:", slots, status )
    return { 
        "slots": [ slot.to_json() for slot in slots ],
         "status": status
    }

@app.route('/scheduler-booked-slots')
def scheduler_booked_slots():
    
    date_st = request.args.get('date')
    name = request.args.get('name')
    print("scheduler-booked-slots: ", name, date_st)

    parsed_date = datetime.strptime(date_st, "%Y-%m-%d").date()
    slots = scheduler.booked_slots(parsed_date, name)

    return { "slots": [ slot.to_json() for slot in slots ]}

@app.route('/scheduler-all-booked-slots')
def scheduler_all_booked_slots():
    
    slots = scheduler.all_booked_slots()

    return { "slots": [ slot.to_json() for slot in slots ]}

@app.route('/scheduler-save-slot')
def scheduler_save_slot():
    
    start_time_st = request.args.get('start_time')
    duration = int(request.args.get('duration'))
    name_st = request.args.get('name')
    address_st = request.args.get('address')

    parsed_start_time = datetime.strptime(start_time_st, "%Y-%m-%d %H:%M:%S")

    slot, status = scheduler.save_slot( parsed_start_time, duration, name_st, address_st )

    return { "status": status, "slot": slot.to_json() }

@app.route('/scheduler-delete-slot')
def scheduler_delete_slot():
    
    start_time_st = request.args.get('start_time')
    name_st = request.args.get('name')

    parsed_start_time = datetime.strptime(start_time_st, "%Y-%m-%d %H:%M:%S")

    status = scheduler.delete_slot( parsed_start_time, name_st )

    return { "status": status }

# --------------------------

@app.route('/scheduler-admin')
def scheduler_admin_page():
    API_KEY = os.environ['GOOGLE_ROUTER_API_KEY']
    return render_template('t-scheduler-admin.html', API_KEY=API_KEY)

@app.route('/scheduler-directions')
def scheduler_directions():

    date_st = request.args.get('date')
    # print("scheduler-directions.date_st:", date_st)

    return scheduler.get_directions( datetime.strptime(date_st, "%Y-%m-%d").date() )

# --------------------------

def start_page_server():

    print(0,'start_page_server', flow_host, flow_port, page_port)
    extra_files = [ os.path.join('templates', 't-base.html', 't-sparrow.html', 't-scientist.html'), os.path.join('static/css', 'style.css')]
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(extra_files=extra_files, host="0.0.0.0", port=page_port, threaded=True)


if __name__ == '__main__':
    
    process1 = multiprocessing.Process(target=start_page_server)
    # process2 = multiprocessing.Process(target=start_socket_server)

    process1.start()
    # process2.start()

    # process1.join()
    # process2.join()

