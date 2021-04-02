from flask import Flask, render_template, render_template_string, jsonify, send_from_directory
import threading, time, os
from copy import deepcopy

from flask_table import table
from flaskr.monitor import monitor_init, get_js_render, get_status_table, get_status_value


app = Flask(__name__)


@app.before_first_request
def _init():
    monitor_init()


@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')


@app.route('/')
def update_page():
    js = get_js_render()
    return render_template('index.html', js=js, table=get_status_table())


@app.route('/update', methods=['GET'])
def update():
    status = get_status_value()
    if status != None:
        table = get_status_table()
        for (item, v, t) in zip(table.items, status['vbat'].values(), status['tbat'].values()):
            item.volt = v
            item.temp = t
        tempList = list(map(lambda item: item.temp, table.items))
        voltList = list(map(lambda item: item.volt, table.items))
        return jsonify({"result": "OK", "t": tempList, 'v': voltList, 'timestamp': status['timestamp']})
    else:
        return jsonify({"result": "FAILED"})


if __name__ == "__main__":
    app.run()
