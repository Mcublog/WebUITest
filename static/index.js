window.onload = function () {
	console.log('hello console!');
	StatusUpdate();
}

function table_fill(json) {
	if (json.result == 'OK') {
		const NAME_ROW = 0;
		const V_ROW = 2;
		var table = document.getElementById('status');
		tbody = table.children[table.children.length - 1];
		for (let row of tbody.children) {
			for (let cell of row.children) {
				if (cell.cellIndex != NAME_ROW) {
					if (cell.cellIndex == V_ROW) {
						cell.innerHTML = json.v[row.rowIndex - 1];
					}
					else {
						cell.innerHTML = json.t[row.rowIndex - 1];
					}
				}
			}
		}
		var date = new Date(json.timestamp * 1000);
		var hours = date.getHours();
		var minutes = "0" + date.getMinutes();
		var seconds = "0" + date.getSeconds();
		var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
		document.getElementById("time").innerHTML = "Time: &nbsp;" + formattedTime;
		console.log(formattedTime);
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

	setTimeout(StatusUpdate, 2000);
	//-------------------------------------------------------------
}
