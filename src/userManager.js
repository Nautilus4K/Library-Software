function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/;SameSite=Strict";
}

function deleteAllCookies() {
    document.cookie.split(';').forEach(cookie => {
        const eqPos = cookie.indexOf('=');
        const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT';
    });
}

var username1 = getCookie("username")
    if (!username1) {
        username1 = null
    }
    fetch("/journal", {
        method: "GET",
        headers: {
            "Username": username1,
            "Action": "Truy cap trang: " + window.location.href
        }
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json);
    })

const username = getCookie("username")
const userElement = document.getElementById("user")

if (username == "") {
    // Do some stuffs to make sure user needs to be authorized (via accounts) to even access the infrastructure in the first place
    // Some stuffs about, idk, security?
    userElement.textContent = "Đăng nhập"
    // window.location.href = "/login.html"
    userElement.href = "/login.html"
    document.getElementById("dropdown_search").innerHTML = ""
    const newElement = document.createElement("a")
    newElement.textContent = "Bạn phải đăng nhập để sử dụng chức năng này!"
    document.getElementById("dropdown_search").appendChild(newElement)
    document.getElementById("searchbarlink").href = "#"
}
else {
    // Fetch information from the API calls. It should be working as intended
    fetch("/get", {
        method: "GET",
        headers: {
            "Username": username
        }
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json)
        if (json["name"] == null) {
            // Performing a hard reset on cookies. Because they're probably corrupted.
            deleteAllCookies()
            userElement.href = "/login.html"
        }
        else {
            userElement.textContent = json["name"]

            // By renewing user's logging in state, it would allow for us
            // to make sure that users that are not visiting the site
            // for more than 7 days are gonna be logged out (for safety)
            setCookie("username", username, 7) // Renew user login state
        }
    })
}
