// handle left bar for switch of tabs
document.addEventListener('DOMContentLoaded', async function () {
    const { _type, _username } = await check_session();

    if ( _type == 'expired' )
    {
        disconnect();
    }
    else if ( _type == "student" )
        $("#content").load("home.html");
    else if ( _type == "admin" )
        $("#content").load("stats.html");

    document.getElementById("real").innerText = _username;
    
    var clickableDivs = document.querySelectorAll('#section-zone div');

    clickableDivs.forEach(function (div) {
        div.addEventListener('click', async function () {
            let text = div.textContent.trim();

            document.getElementById("content").innerHTML = "";

            const { _type, _username } = await check_session();

            if ( _type == 'expired' )
            {
                disconnect();
            }

            if (text == "Home")
            {
                if ( _type == "student" )
                    $("#content").load("home.html");
                else if ( _type == "admin" )
                    $("#content").load("stats.html");
            }
            else if ( text == "Search")
            {
                $("#content").load("search.html");
            }
            else if ( text == "Files")
            {
                loadDocuments();
            }

            document.getElementById("header").innerHTML = `<h1>${text}</h1><i class="fa fa-sign-out" aria-hidden="true" onclick="disconnect();"></i>`;
            
        });
    });
});

