function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

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
            setCookie("username", username, 7) // Let the user be logged in for 7 days before logged out
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

if (getCookie("username")) window.location.href = "/"

document.addEventListener("keydown", key => {
    if (key.code == "Enter" && (document.activeElement.id == "first" || document.activeElement.id == "password")) {
        submit()
        // console.log(document.activeElement.id)
    }
})

var facereg = false
var orgLoginbuttonDisplayStyle = document.getElementById("loginbutton").style.display
var orgLoginfieldDisplayStyle = document.getElementById("loginfield_section").style.display
var orgFaceregDisplayStyle = "block"

var sentImage = false

var token = ""

function switchmode() {
    facereg = !facereg
    if (facereg) { // If now we are changing to face recoginiton mode
        document.getElementById("loginbutton").style.display = "none"
        document.getElementById("loginfield_section").style.display = "none"
        document.getElementById("face_reg_section").style.display = orgFaceregDisplayStyle
        document.getElementById("switchmodebutton").textContent = "<"
        
        const cameraVideoStream = document.getElementById('camera')
        const canvas = document.getElementById('canvas')
        const ctx = canvas.getContext('2d')

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia({ video: true })) {
            navigator.mediaDevices
            .getUserMedia({ video: true })
            .then ((stream) => {
                cameraVideoStream.srcObject = stream
                cameraVideoStream.play()
            })
        }
        // console.log(cameraVideoStream.videoWidth + " | " + cameraVideoStream.videoHeight)

        // var token

        // Capture and send the image as JPEG
        setInterval(() => {
            if (cameraVideoStream.videoWidth === 0 || cameraVideoStream.videoHeight === 0) {
                console.log("Waiting for video dimensions...");
                return;  // Ensure video is ready before capturing
            }

            if (!sentImage) { // If haven't send image yet
                console.log("Capturing image...");
                canvas.width = cameraVideoStream.videoWidth; // Video's intrinsic width
                canvas.height = cameraVideoStream.videoHeight; // Video's intrinsic height
                ctx.drawImage(cameraVideoStream, 0, 0, canvas.width, canvas.height);

                // Capture the image from canvas as JPEG
                const imgData = canvas.toDataURL("image/jpeg").split(",")[1]
                sendImageToServer(imgData)
                sentImage = true;
            }
            else {
                fetch('/getfacialresult', {
                    method: "GET",
                    headers: {
                        'token': token
                    }
                })
                .then((response) => response.json())
                .then((json) => {
                    console.log(json)
                    const face_alert = document.getElementById("face_alerto")
                    if (json["status"] == "WAITING") {
                        // Ignore? Yea lets just wait
                        face_alert.style.display = "block"
                        face_alert.textContent = "Đang kiểm tra khuôn mặt..."
                    }
                    else if (json["status"] == "SUCCESSFUL") {
                        // Actual real stuffs
                        if (json["error"]) {
                            sentImage = false; // Redo the facial recoginition process if an error happened
                            face_alert.style.display = "block"
                            face_alert.textContent = "Đã có lỗi xảy ra. Đang kiểm tra lại khuôn mặt..."
                        }
                        else if (json["result"] == null) {
                            sentImage = false; // Redo?
                            face_alert.style.display = "block"
                            face_alert.textContent = "Hãy nhìn thẳng vào camera"
                        }
                        else {
                            // In this case, json["result"] already is a valid string.
                            // Because of that, it could only mean that there is a result.
                            // On top of that, its just how the server works behind the scenes
                            // => We make the user json["result"]!!!!

                            setCookie("username", json["result"], 7) // Let the user be logged in for 7 days before logged out
                            window.location.href = "/"
                        }
                    }
                })
            }
            

        }, 1000);  // Capture image every second
    }
    else {
        document.getElementById("loginbutton").style.display = orgLoginbuttonDisplayStyle
        document.getElementById("loginfield_section").style.display = orgLoginfieldDisplayStyle
        document.getElementById("face_reg_section").style.display = "none"
        document.getElementById("switchmodebutton").textContent = ">"
    }
}


function sendImageToServer(imgData) {
    // Send the image via POST request to the server
    fetch('/facial', {
        method: 'POST',
        body: imgData,
    })
    .then(response => {
        console.log('Response received from server:', response);
        return response.json(); // Assuming the server returns a JSON response
    })
    .then(data => {
        console.log('Server Response:', data);
        console.log(data["token"])
        token = data["token"]
        return data["token"]
    })
    .catch(error => {
        console.error('Error:', error);
    });

    console.log(token)
    return token
}
