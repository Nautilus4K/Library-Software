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

function changepasswd() {
    const password = document.getElementById("password").value
    const newpass = document.getElementById("newpass").value
    const confirmpass = document.getElementById("confirmpass").value

    if (password == "") {
        document.getElementById("alerto1").style.display = "none"
        document.getElementById("newpass").style.border = "0"

        document.getElementById("alerto").style.display = "block"
        document.getElementById("alerto").textContent = "Điền mật khẩu"
        document.getElementById("password").style.border = "2px solid red"
    }

    fetch("/logincheck", {
        method: "GET",
        headers: {
            "Username": getCookie("username"),
            "Password": password
        }
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json);

        // In case the check has concluded that the credentials provided are invalid
        // we push out zhe alerto
        if (json["correct"]) {
            console.log("oh yea")
            document.getElementById("alerto").style.display = "none"
            document.getElementById("password").style.border = "0"

            if (newpass == "") {
                // Revert back all boxes that aren't really relevant
                document.getElementById("alerto2").style.display = "none"
                document.getElementById("confirmpass").style.border = "0"
        
                document.getElementById("alerto1").style.display = "block"
                document.getElementById("alerto1").textContent = "Điền mật khẩu mới"
                document.getElementById("newpass").style.border = "2px solid red"
            }
            else if (confirmpass != newpass) {
                document.getElementById("alerto1").style.display = "none"
                document.getElementById("newpass").style.border = "0"

                document.getElementById("alerto2").style.display = "block"
                document.getElementById("alerto2").textContent = "Mật khẩu không trùng khớp!"
                document.getElementById("confirmpass").style.border = "2px solid red"
            }
            else {
                document.getElementById("alerto1").style.display = "none"
                document.getElementById("newpass").style.border = "0"
                document.getElementById("alerto2").style.display = "none"
                document.getElementById("confirmpass").style.border = "0"

                fetch("/modifyaccounts", {
                    method: "GET",
                    headers: {
                        "Username": getCookie("username"),
                        "Password": password,
                        "Newpass": newpass
                    }
                })
                .then((response) => response.json())
                .then((json) => {
                    console.log(json)
                    if (json["error"]) {
                        document.getElementById("alerto3").style.display = "block"
                        document.getElementById("alerto3").style.color = "red"
                        document.getElementById("alerto3").textContent = "Đã có lỗi xảy ra. Vui lòng thử lại sau"
                    }
                    else {
                        document.getElementById("alerto3").style.display = "block"
                        document.getElementById("alerto3").style.color = "green"
                        document.getElementById("alerto3").textContent = "Đổi mật khẩu thành công!"
                    }
                })
                .catch((error2) => {
                    console.error("Error:", error2)
                    document.getElementById("alerto3").style.display = "block"
                    document.getElementById("alerto").textContent = "Đã có lỗi xảy ra. Vui lòng thử lại sau"
                })
            }
        }
        else {
            document.getElementById("alerto").style.display = "block"
            document.getElementById("alerto").textContent = "Mật khẩu sai!"
            document.getElementById("password").style.border = "2px solid red"
        }  
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}

function deleteAllCookies() {
    document.cookie.split(';').forEach(cookie => {
        const eqPos = cookie.indexOf('=');
        const name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT';
    });
}
function signout() {
    deleteAllCookies()
    window.location.href=window.location.href
}