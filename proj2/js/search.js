function submitForm(event)
{
    event.preventDefault();

    var keyword = document.getElementById('searchBar').value;
    var year = document.getElementById('yearRange').value;
    var theme = document.getElementById('themeCompany').value;
    var company = document.getElementById('companyName').value;

    loadSearch(keyword,
            theme,
            company,
            year);
}

function toggleAdvancedFilters() {
  var advancedFilters = document.getElementById('advancedFilters');
  var toggleCheckbox = document.getElementById('toggleFilters');

  // Toggle the visibility of advanced filters based on the checkbox state
  advancedFilters.style.display = toggleCheckbox.checked ? 'flex' : 'none';
}

fill_year_range("yearRange");

// load options for company
var company_options = document.getElementById("companyName");

fetch('http://localhost:8000/get_companies')
.then(response => response.json())
.then(data => {
    data.forEach(company => {
    var option = document.createElement("option");
    option.value = company;
    option.text = company;
    company_options.add(option);
    });
})
.catch(error => console.error('Error fetching data:', error));

// load options for theme
var theme_options = document.getElementById("themeCompany");

fetch('http://localhost:8000/get_themes')
.then(response => response.json())
.then(data => {
    data.forEach(company => {
    var option = document.createElement("option");
    option.value = company;
    option.text = company;
    theme_options.add(option);
    });
})
.catch(error => console.error('Error fetching data:', error));

// Function to load table for search
function loadSearch(keyword="", theme="", company="", year="")
{    
    const fetchOptions = {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${getCookie('token')}`
        }
      };

    fetch(`http://localhost:8000/search?keywords=${keyword}&company=${company}&theme=${theme}&year=${year}`, fetchOptions)
    .then(response => response.json())
    .then(data => {

        if (data) {

            var existingTable = document.getElementById("mytable");

            if (existingTable) {
              existingTable.remove();
            }

            var tableHtml = '<table class="table" id="mytable" style="margin-top:2%;">';
                    
            tableHtml += '<thead><tr>';
            tableHtml += '<th>Student</th>';
            tableHtml += '<th>Company</th>';
            tableHtml += '<th>Start</th>';
            tableHtml += '<th>End</th>';
            tableHtml += '<th>Supervisor</th>';
            tableHtml += '<th>Theme</th>';
            tableHtml += '<th>Download</th>';
            tableHtml += '</tr></thead>';

            tableHtml += '<tbody>';

            Object.keys(data).forEach(function(key) {
                var entry = data[key];

                tableHtml += '<tr>';

                tableHtml += `
                    <td>${entry['studentName']}</td>
                    <td>${entry['company_name']}</td>
                    <td>${entry['start_date']}</td>
                    <td>${entry['end_date']}</td>
                    <td>${entry['supervisor_name']}</td>
                    <td>${entry['theme']}</td>
                    <td><i class="fa fa-download" aria-hidden="true" onclick="downloadDocument('${entry['reportId']}');" style="cursor: pointer;"></i></td>
                    `

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