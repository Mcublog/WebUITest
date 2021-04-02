from copy import deepcopy
from flask_table import Table, Col
import threading, time, math
from flask import render_template_string
from pathlib import Path
from typing import Tuple

from CanBmsPy.cubbie import Cubbie
from params import get_bitflags


BATTARY_NUM = 16
cubbieCan = Cubbie(console_mode=True, enumerate=False, wdt=False, autodetect=False)
statusTable = None
flagTable = None
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

class FlagTable(Table):
    bit_column0 = Col('')
    bit_column1 = Col('')
class FlagItem(object):
    def __init__(self, bit0, bit1):
        self.bit_column0 = bit0
        self.bit_column1 = bit1


def create_tables() -> Tuple[Table, Table]:
    items = []
    bf = get_bitflags(0)

    for i in range(BATTARY_NUM):
        items.append(Item('#%d' % (i+1), 0, 0))
    table = ItemTable(items, table_id='status')

    item_flags = []
    rows = math.ceil(len(bf) / 2)
    for i in range(rows):
        item_flags.append(FlagItem(bf[i], bf[i + (rows)]))
    flagtable = FlagTable(item_flags, table_id='flags')
    return table, flagtable


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


def get_js_render():
    path = Path(__file__).parent.parent.joinpath('static/index.js')
    return render_js(str(path))


def get_flag_list_for_table():
    global statusDict
    bf = get_bitflags(statusDict['status']['flag'])
    bfList = []
    rows = math.ceil(len(bf) / 2)
    for i in range(rows):
        k0, k1 = bf[i], bf[i + rows]
        bfList.append([bf[k0], bf[k1]])
    return bfList


def monitor_init():
    global statusTable, flagTable
    global statusDict
    statusTable, flagTable = create_tables()
    cubbieCan.enumerate()
    threading.Thread(name="status_upadater", target=update_status, args=()).start()


if __name__ == "__main__":
    flagInt = 18882561
    bf = get_bitflags(flagInt)
    bfList = []
    # for k, v in bf.items():
    #     bfDict[k] = v
    items = []
    bfList = []
    rows = math.ceil(len(bf) / 2)
    for i in range(rows):
        k0, k1 = bf[i], bf[i + rows]
        bfList.append([bf[k0], bf[k1]])
        items.append(FlagItem(k0, k1))
    table = FlagTable(items, table_id='flags')
    print(table.__html__())
    print()
