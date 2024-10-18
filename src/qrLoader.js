console.log("Initializing QR Loader from <script> call...")

const videoElement = document.getElementById('camera');
const canvasElement = document.getElementById('canvas');
const canvasContext = canvasElement.getContext('2d', { willReadFrequently: true });
const resultElement = document.getElementById('result');
canvasContext.willReadFrequently = true;


// Function to start the video stream
function startVideoStream() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
            .then(function (stream) {
                videoElement.srcObject = stream; // Display the stream in the video element
                requestAnimationFrame(tick); // Start processing frames in real-time
            })
            .catch(function (err) {
                console.log("Error: " + err);
            });
    } else {
        console.log("getUserMedia not supported on this browser.");
    }
}

// Function to process video frames and scan for QR codes
function tick() {
    if (videoElement.readyState === videoElement.HAVE_ENOUGH_DATA) {
        // Draw the video frame to the canvas
        canvasElement.width = videoElement.videoWidth;
        canvasElement.height = videoElement.videoHeight;
        canvasContext.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
        
        // Extract image data from the canvas
        const imageData = canvasContext.getImageData(0, 0, canvasElement.width, canvasElement.height);
        
        // Scan the image data for a QR code
        const qrCode = jsQR(imageData.data, imageData.width, imageData.height);
        
        if (qrCode) {
            // Display the QR code's decoded data
            resultElement.textContent = "Đã tìm thấy mã QR: " + qrCode.data;
            window.location.href = "/idinfo.html?code="+qrCode.data;
        } else {
            resultElement.textContent = "Hãy chiếu chiếu toàn bộ mã QR vào camera của bạn";
        }
    }

    // Call tick again for the next frame
    requestAnimationFrame(tick);
}

// Start the video stream when the page loads
startVideoStream();