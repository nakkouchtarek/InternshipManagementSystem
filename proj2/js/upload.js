document.getElementById('fileInput').addEventListener('change', handleFileSelect);

async function handleFileSelect(event) {
    const fileInput = event.target;
    const files = fileInput.files;

    if (files.length > 0) 
    {
        const file = files[0];

        const allowedExtensions = ['docx', 'pdf', 'pptx'];
        const fileNameParts = file.name.split('.');
        const fileExtension = fileNameParts[fileNameParts.length - 1].toLowerCase();
        
        if ( allowedExtensions.includes(fileExtension) )
        {
            var year = document.getElementById("yearRange").value;
            var type = document.getElementById("docType").value;

            if ( year != '' )
            {
                const additionalData = {
                    year: year,
                    file_type: type,
                };

                await uploadFile(file, additionalData);
            }
            else
            {
                alert("Please fill in year of choice!");
            }
        }
        else
        {
            alert("Allowed extensions are: pdf, docx and pptx.")
        }

    }
}

async function uploadFile(file, additionalData) 
{
    const apiUrl = 'http://localhost:8000/uploadfile/';

    const formData = new FormData();
    formData.append('file', file);

    for (const key in additionalData) {
        if (additionalData.hasOwnProperty(key)) {
            formData.append(key, additionalData[key]);
        }
    }

    fetch(apiUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'Authorization': `Bearer ${getCookie('token')}`,
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('File upload failed');
        }
        return response.json();
    })
    .then(data => {
        alert("File uploaded successfully!");
    })
    .catch(error => {
        alert("Error uploading file!");
    });
};

fill_year_range("yearRange");