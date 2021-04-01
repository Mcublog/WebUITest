from flask import Flask, render_template, render_template_string, jsonify, make_response
from flask_table import Table, Col

# Declare your table
class ItemTable(Table):
    name = Col('Cell')
    temp = Col('t C')
    volt = Col('V mV')

    # def __init__(self, items, classes, thead_classes, sort_by, sort_reverse, no_items, table_id, border, html_attrs):
    #     super().__init__(items, classes=classes, thead_classes=thead_classes, sort_by=sort_by, sort_reverse=sort_reverse, no_items=no_items, table_id=table_id, border=border, html_attrs=html_attrs)
    #     self.th_contents


# Get some objects
class Item(object):
    def __init__(self, name, temp, volt):
        self.name = name
        self.temp = temp
        self.volt = volt



BATTARY_NUM = 16
def create_table() -> Table:
    items = []
    for i in range(BATTARY_NUM):
        items.append(Item('#%d' % i, 0, 0))
    table = ItemTable(items, table_id='status')
    return table


def render_js(fname, **kwargs):
    with open(fname) as fin:
        script = fin.read()
        rendered_script = render_template_string(script, **kwargs)
        return rendered_script


app = Flask(__name__)
table = create_table()


@app.route('/')
def hello():
    for item in table.items:
        item.temp += 1
    js = render_js('static/index.js', a="wow")
    return render_template('index.html', js=js, table=table, cal=table)


@app.route('/update', methods=['GET'])
def update():
    for item in table.items:
        item.temp += 1

    tempList = list(map(lambda item: item.temp, table.items))
    return jsonify({"result": "OK", "response": True, "t": tempList})


if __name__ == "__main__":
    app.run(debug=True)
