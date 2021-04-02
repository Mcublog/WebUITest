from flask import Flask, render_template, jsonify, send_from_directory
import os, sys

sys.path.insert(0, 'flaskr')

import flaskr.monitor as monitor


app = Flask(__name__)


@app.before_first_request
def _init():
    monitor.monitor_init()


@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')


@app.route('/')
def update_page():
    js = monitor.get_js_render()
    return render_template('index.html', js=js, table=monitor.statusTable, flag_table=monitor.flagTable)


@app.route('/update', methods=['GET'])
def update():
    status = monitor.statusDict
    if status != None:
        table = monitor.statusTable
        flagTable = monitor.flagTable
        for (item, v, t) in zip(table.items, status['vbat'].values(), status['tbat'].values()):
            item.volt = v
            item.temp = t
        bfList = monitor.get_flag_list_for_table()
        # for (item, flags) in zip(flagTable.items, bfList):
        #     item.bit_column0 = flags[0]
        #     item.bit_column1 = flags[1]

        tempList = list(map(lambda item: item.temp, table.items))
        voltList = list(map(lambda item: item.volt, table.items))
        return jsonify({"result": "OK", "t": tempList, 'v': voltList, 'timestamp': status['timestamp'], 'flags': bfList})
    else:
        return jsonify({"result": "FAILED"})


if __name__ == "__main__":
    app.run()
