let csvSocket = null;

function connectWebSocket() {
    let url = `ws://${window.location.host}:80/ws/socket-server/`;
    const csvSocket = new WebSocket(url);

    csvSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);

        if (data.type === "connection_established") {
            let rowInput = document.getElementById("row-input");
            let newRowInput = document.createElement("input");
            newRowInput.setAttribute("type", "number");
            newRowInput.setAttribute("name", "rows");
            newRowInput.setAttribute("required", "true");
            rowInput.parentNode.replaceChild(newRowInput, rowInput);

            let connectionInfo = document.getElementById("connection-info");
            let newConnectionInfo = document.createElement("p");
            newConnectionInfo.innerHTML = `Ready to generate csv file!`;
            connectionInfo.parentNode.replaceChild(newConnectionInfo, connectionInfo);
        }

        if (data.type === "csv_generator_processing") {
            let csvFilesTable = document.getElementById("csv-files");

            csvFilesTable.insertAdjacentHTML(
                'afterbegin',
                `<tr id="csv-file-${data.csv_instance_id}">
                 <th scope="row" class="text-center">${data.csv_instance_id}</th>
                 <td class="text-center">${data.csv_instance_created}</td>
                 <td class="text-center">
                     <div class="text-light bg-secondary rounded-3">
                     Processed
                     </div>
                 </td>
                 <td class="text-center">
                 </td>
                 </tr>
                 `
            );
        }

        if (data.type === "csv_generator_ready") {
            let csvFileRow = document.getElementById(`csv-file-${data.csv_instance_id}`);
            let newRow = document.createElement("tr");
            let downloadUrl = `/schema/generate/${data.csv_instance_id}/download/`;

            newRow.innerHTML = `
            <th scope="row" class="text-center">${data.csv_instance_id}</th>
            <td class="text-center">${data.csv_instance_created}</td>
            <td class="text-center">
                <div class="text-light bg-success rounded-3">
                Ready
                </div>
            </td>
            <td class="text-center">
                <a href="${downloadUrl}">Download</a>
            </td>
            `

            csvFileRow.parentNode.replaceChild(newRow, csvFileRow);
        }
    }

    csvSocket.onclose = function (event) {
        if (event.code === 1006) {
            setTimeout(function () {
                location.reload();
            }, 100000);

            let connectionInfo = document.getElementById("connection-info");
            let newConnectionInfo = document.createElement("p");
            newConnectionInfo.innerHTML = `
              You left me before receiving your CSV file :(
              <br>You can make a new file after auto reload page in 100 seconds`;
            connectionInfo.parentNode.replaceChild(newConnectionInfo, connectionInfo);
        }

    };

    let form = document.getElementById("form")
    form.addEventListener("submit", (e)=> {
        e.preventDefault();
        let rows = e.target.rows.value;
        let data_schema_id = document.getElementById(
            "data_schema_id"
        ).getAttribute('data-pk');

        csvSocket.send(JSON.stringify({
            "rows": rows,
            "data_schema_id": data_schema_id,
        }));
        form.reset();
    })
}

connectWebSocket();
