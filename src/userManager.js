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
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

const username = getCookie("username")
const userElement = document.getElementById("user")

if (username == "") {
    userElement.textContent = "Đăng nhập"
}
else {
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
            for (let i = 0; i < allCookies.length; i++)
                document.cookie = allCookies[i] + "=;expires="
                    + new Date(0).toUTCString()
            window.location.href = window.location.href
        }
        userElement.textContent = json["name"]
    })
}
