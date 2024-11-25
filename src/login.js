function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function submit() {
    console.log("Checking supplied credentials");

    const username = document.getElementById("first").value.trim();
    const password = document.getElementById("password").value.trim();

    // Validate input fields
    if (username === "") {
        alert("Điền tên đăng nhập của bạn");
        document.getElementById("first").focus(); // Focus on the username field
        return; // Stop further execution
    } else if (password === "") {
        alert("Điền mật khẩu của bạn");
        document.getElementById("password").focus(); // Focus on the password field
        return; // Stop further execution
    }

    // If validation passes, proceed to fetch
    fetch("/logincheck", {
        method: "GET",
        headers: {
            "Username": username,
            "Password": password
        }
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json);

        // In case the check has concluded that the credentials provided are invalid
        // we push out zhe alerto
        if (json["correct"]) {
            setCookie("username", username, 7) // Let the user be logged in for 7 days
            window.location.href = "/"
        }
        else {
            document.getElementById("alerto").style.display = "block"
            document.getElementById("first").style.border = "2px solid red"
            document.getElementById("password").style.border = "2px solid red"
        }  
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}
