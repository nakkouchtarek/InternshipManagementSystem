document.addEventListener("DOMContentLoaded", function(event){
    fill_year_range("graduation-year");
});

function register()
{
    var username = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var year = document.getElementById("graduation-year").value;

    if ( username !== "" && password !== "" )
    {
        fetch("http://localhost:8000/register/", {
                method: "POST",
                body: JSON.stringify({
                    username: username,
                    password: password,
                    year: year
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
                })
        .then(response => {

            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Request failed');
            }
        })
        .then(data => {
            if (data.state === 'created') 
            {
              alert('User created!');
              goLogin();
            } 
            else 
            {
              alert('User already exists!');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

    }
    else
    {
        alert("Incomplete inputs!")
    }
}


function goLogin()
{
    window.location.pathname='/html/login.html';
}