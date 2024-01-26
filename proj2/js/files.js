async function downloadDocument(fileId) 
{
    fetch(`http://localhost:8000/get_document/?id=${fileId}`)
    .then(response => response.json())
    .then(data => {
        const base64String = data.data;

        // we decode base64 we receive from api
        const byteCharacters = atob(base64String);

        // make an array of same length of the decoded string
        const byteNumbers = new Array(byteCharacters.length);

        // we take each character from the decoded string and generate the ascii code for it
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }

        // we need to turn each int to 8 bytes in order to transform the whole array into a blob
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'application/octet-stream' });

        // launch the download
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = data.filename;
        link.click();
        });
}

// Function to load table for search
function loadDocuments()
{    
    const fetchOptions = {
        method: 'GET', // You can change the HTTP method as needed
        headers: {
          'Authorization': `Bearer ${getCookie('token')}`
        }
      };

    fetch(`http://localhost:8000/get_documents/`, fetchOptions)
    .then(response => response.json())
    .then(data => {

        if (data) {

            var existingTable = document.getElementById("mytable");

            // If the table exists, remove it so they do not overlap
            if (existingTable) {
              existingTable.remove();
            }

            var tableHtml = '<table class="table" id="mytable">';
                    
            tableHtml += '<thead><tr>';
            tableHtml += '<th>Document ID</th>';
            tableHtml += '<th>Document Name</th>';
            tableHtml += '<th>Student</th>';
            tableHtml += '<th></th>';
            tableHtml += '</tr></thead>';

            tableHtml += '<tbody>';

            data = data.documents;

            Object.keys(data).forEach(function(key) {
                var entry = data[key];
                var id;

                tableHtml += '<tr>';

                Object.values(entry).forEach(function(value, index) {
                    if ( index == 0 )
                    {
                        id = value;
                    }

                    tableHtml += '<td>' + value + '</td>';
                });

                tableHtml += `<td><i class="fa fa-download" aria-hidden="true" onclick="downloadDocument('${id}');" style="cursor: pointer;"></i></td>`;

                tableHtml += '</tr>';

              });

            tableHtml += '</tbody>';

            tableHtml += '</table>';


            document.getElementById('content').innerHTML += tableHtml;
        } else {
            console.error('Invalid response format');
        }

    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}