async function check_session() {
    const token = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*=\s*([^;]*).*$)|^.*$/, "$1");
    let _type = '';
    let _username = '';

    if (token) {
        const url = 'http://localhost:8000/check_validity/';

        const requestBody = JSON.stringify({ token: token });

        const headers = new Headers({
            'Content-Type': 'application/json'
        });

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: headers,
                body: requestBody
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            _type = data.type;
            _username = data.username;

            return { _type, _username }; // Return _type value

        } catch (error) {
            console.error('Error during fetch operation:', error);
            throw error; // Rethrow the error

        }
    } else {
        _type = 'expired';
        return { _type, _username };
    }
}

function deleteAllCookies() 
{
    const cookies = document.cookie.split(";");

    // adds up expiration of cookie so browser deletes it
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
}

// Function to get the value of a cookie by name
function getCookie(name) 
{
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) 
    {
        const cookie = cookies[i].trim();
        // example token= -> matches -> return token value
        if (cookie.startsWith(name + '=')) 
        {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}


// handle disconnect
function disconnect()
{
    deleteAllCookies();
    window.location.pathname='/html/login.html';
}
  