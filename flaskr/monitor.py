from copy import deepcopy
from flask_table import Table, Col
import threading, time
from flask import render_template_string
from pathlib import Path

from flaskr.CanBmsPy.cubbie import Cubbie


BATTARY_NUM = 16
cubbieCan = Cubbie(console_mode=True, enumerate=False, wdt=False, autodetect=False)
statusTable = None
statusDict = None


class ItemTable(Table):
    name = Col('Cell')
    temp = Col('t C')
    volt = Col('V mV')


class Item(object):
    def __init__(self, name, temp, volt):
        self.name = name
        self.temp = temp
        self.volt = volt

def create_table() -> Table:
    items = []
    for i in range(BATTARY_NUM):
        items.append(Item('#%d' % (i+1), 0, 0))
    table = ItemTable(items, table_id='status')
    return table


def render_js(fname):
    with open(fname) as fin:
        script = fin.read()
        rendered_script = render_template_string(script)
        return rendered_script


def update_status():
    global statusDict
    global cubbieCan
    while True:
        status_temp = cubbieCan.get_last_update(1)
        if status_temp:
            statusDict = deepcopy(status_temp)
        time.sleep(1)

def get_status_table() -> Table:
    global statusTable
    return statusTable


def get_js_render():
    path = Path(__file__).parent.parent.joinpath('static/index.js')
    return render_js(str(path))

def get_status_value():
    global statusDict
    return statusDict


def monitor_init():
    global statusTable
    global statusDict
    statusTable = create_table()
    cubbieCan.enumerate()
    threading.Thread(name="status_upadater", target=update_status, args=()).start()
