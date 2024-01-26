function login()
{
    var username = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    if ( username !== "" && password !== "" )
    {
        fetch("http://localhost:8000/login/", {
                method: "POST",
                body: JSON.stringify({
                    username: username,
                    password: password,
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
            if (data.token === '') 
            {
              alert('Invalid credentials!');
            } 
            else 
            {
              var token = data.token;
              document.cookie = `token=${token}; SameSite=None; Secure`;
              window.location.pathname='/html/index.html';
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


function goRegister()
{
    window.location.pathname='/html/register.html';
}
