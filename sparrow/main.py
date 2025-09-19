import config
import os, asyncio, websockets, ssl
from flask import Flask, request, render_template, redirect
import multiprocessing
from sparrow.flow.flow_session import *
from sparrow.agent.researcher import Researcher
import sparrow.toolkit.route.scheduler as sc
import sparrow.toolkit.route.slots as sl

from datetime import date, datetime

app = Flask(__name__)

flow_host = os.getenv("FLOW_HOST")
flow_port = os.getenv("FLOW_PORT")
page_port = os.getenv("PAGE_PORT")

# print( flow_host, flow_port, page_port )    

scheduler = sc.Scheduler()

@app.route('/')
def index_page():
    return redirect('/handler')

@app.route('/handler')
def handler_page():
    return render_template('t-handler.html', flow_host=flow_host, flow_port=flow_port, flow='handler')

@app.route('/researcher')
def researcher_page():
    return render_template('t-researcher.html', flow_host=flow_host, flow_port=flow_port, flow='researcher')




@app.route('/scheduler')
def scheduler_page():
    API_KEY = os.environ['GOOGLE_ROUTER_API_KEY']
    return render_template('t-scheduler.html', API_KEY=API_KEY)

@app.route('/scheduler-slots')
def scheduler_slots():
    
    date_st = request.args.get('date')
    print("scheduler-slots.date_st:", date_st)
    duration = int(request.args.get('duration'))
    name_st = request.args.get('name')
    address_st = request.args.get('address')

    parsed_date = datetime.strptime(date_st, "%Y-%m-%d").date()
    slots = scheduler.available_slots(parsed_date, duration, name_st, address_st)

    return { "slots": [ slot.to_json() for slot in slots ]}

@app.route('/scheduler-save-slot')
def scheduler_save_slot():
    
    start_time_st = request.args.get('start_time')
    duration = int(request.args.get('duration'))
    name_st = request.args.get('name')
    address_st = request.args.get('address')

    parsed_start_time = datetime.strptime(start_time_st, "%Y-%m-%d %H:%M:%S")
    slot = sl.Slot(parsed_start_time, duration, name_st, address_st)

    scheduler.month.add_slot( slot )
    scheduler.month.save( sc.router.folder + "month.json" )

    return scheduler.get_directions( parsed_start_time.date() )

@app.route('/scheduler-directions')
def scheduler_directions():

    date_st = request.args.get('date')
    print("scheduler-day.date_st:", date_st)

    return scheduler.get_directions( datetime.strptime(date_st, "%Y-%m-%d").date() )











@app.route('/invoke', methods=['GET'])
def invoke():
    # model = request.args.get('model')
    task = request.args.get('task')

    agent = Researcher()

    print("Invoking Researcher Agent")

    res = agent.invoke(task)
    #print(res)
    return res

def start_page_server():

    print(0,'start_page_server', flow_host, flow_port, page_port)
    extra_files = [ os.path.join('templates', 't-base.html', 't-sparrow.html', 't-scientist.html'), os.path.join('static/css', 'style.css')]
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(extra_files=extra_files, host="0.0.0.0", port=page_port, threaded=True)

def start_socket_server():

    print(0,'start_socket_server')

    cert_file = os.getenv("CERT_FILE")
    key_file = os.getenv("KEY_FILE")

    # if flow_host == "localhost":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain( certfile=cert_file, keyfile=key_file )

    start_server = websockets.serve( flow_session, "0.0.0.0", flow_port, ssl=ssl_context )
    loop = get_or_create_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
    
    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()

    # loop = asyncio.new_event_loop()
    # return serve_websocket()




async def serve_websocket():
    return await websockets.serve(flow_session, "0.0.0.0", flow_port)

def get_or_create_event_loop():

    try:
        print("trout 20")
        return asyncio.get_event_loop()
    except Exception as ex:
        print("trout 30")
        print(ex.message)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return asyncio.get_event_loop()

if __name__ == '__main__':
    
    process1 = multiprocessing.Process(target=start_page_server)
    # process2 = multiprocessing.Process(target=start_socket_server)
    process1.start()
    # process2.start()
    # process1.join()
    # process2.join()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(serve_websocket())
    # print(10,loop)
    loop.run_forever()
    

    # start_socket_server()
    # start_page_server()

    # loop = asyncio.get_event_loop()
    # async def create_tasks_func():
    #     tasks = list()
    #     tasks.append(asyncio.create_task( start_socket_server() ))
    #     await asyncio.wait(tasks)
    # loop.run_until_complete(create_tasks_func())
    # loop.run_forever()

    # asyncio.run(start_socket_server())

    # # asyncio.get_event_loop().run_until_complete(start_server)
    # # asyncio.get_event_loop().run_forever()
    # asyncio.run(start_server)
    # print("salmon")
    # asyncio.get_event_loop().run_forever()

    # import threading 
    # # process1 = threading.Thread(target=start_socket_server)
    # process2 = threading.Thread(target=start_page_server)
    # # process1.start()
    # process2.start()
    # # process1.join()
    # process2.join()
