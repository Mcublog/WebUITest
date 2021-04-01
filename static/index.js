window.onload = function(){
    console.log('hello console!');
    StatusUpdate();
}

function table_fill(json) {
    const NAME_ROW = 0;
    const V_ROW = 2;
    var table = document.getElementById('status');
    tbody = table.children[table.children.length - 1];
    for (let row of tbody.children)
    {
        for (let cell of row.children)
        {
            if (cell.cellIndex != NAME_ROW)
            {
                if (cell.cellIndex == V_ROW)
                {
                    cell.innerHTML = String(Math.random());
                }
                else
                {
                    cell.innerHTML = json.t[row.rowIndex-1];
                }
            }
        }
    }
}

function StatusUpdate() {
    let xhr = new (XMLHttpRequest);
    xhr.open("GET", "update", true);
    xhr.responseType = "application/json";
    xhr.send(null);

    fetch('/update')
        .then(response => response.json())
        .then(json => table_fill(json));

    var x = Math.random();
    document.getElementById("data").innerHTML = "Vbat: &nbsp;" + String(x);
    setTimeout(StatusUpdate, 2000);
    //-------------------------------------------------------------
}
