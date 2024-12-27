function scrollToSection(id) {
    const target = document.getElementById(id);
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

console.log("Initializing QR Loader from <script> call...");

const videoElement = document.getElementById('camera');
const canvasElement = document.getElementById('canvas');
const canvasContext = canvasElement.getContext('2d', { willReadFrequently: true });
const resultElement = document.getElementById('result');
canvasContext.willReadFrequently = true;

// Function to start the video stream
async function startVideoStream() {
    try {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: "environment" }
            });
            videoElement.srcObject = stream; // Display the stream in the video element
            videoElement.onloadedmetadata = () => {
                videoElement.play();
                requestAnimationFrame(tick); // Start processing frames in real-time
            };
        } else {
            throw new Error("getUserMedia is not supported on this browser.");
        }
    } catch (err) {
        console.error("Error accessing the camera:", err);
        resultElement.textContent = "Không thể truy cập camera. Vui lòng kiểm tra quyền.";
    }
}

var scanned = false

// Function to process video frames and scan for QR codes
function tick() {
    if (videoElement.readyState === videoElement.HAVE_ENOUGH_DATA) {
        canvasElement.width = videoElement.videoWidth;
        canvasElement.height = videoElement.videoHeight;
        canvasContext.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

        const imageData = canvasContext.getImageData(0, 0, canvasElement.width, canvasElement.height);
        const qrCode = jsQR(imageData.data, imageData.width, imageData.height);

        if (qrCode && !scanned) {
            var username = getCookie("username")
            if (!username) {
                username = null
            }
            fetch("/journal", {
                method: "GET",
                headers: {
                    "Username": username,
                    "Action": "Quet ma QR: " + qrCode.data
                }
            })
            .then((response) => response.json())
            .then((json) => {
                console.log(json);
            })
            resultElement.textContent = "Đã tìm thấy mã QR: " + qrCode.data;
            window.location.href = "/idinfo.html?code=" + qrCode.data;
            scanned = true
        } else {
            resultElement.textContent = "Hãy chiếu chiếu toàn bộ mã QR vào camera của bạn";
        }
    }

    requestAnimationFrame(tick);
}

scrollToSection("camera")
// Start the video stream when the page loads
startVideoStream();
