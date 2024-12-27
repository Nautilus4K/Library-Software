const username2 = getCookie("username")
if (username2 != "admin") {
    // If user isn't admin
    alert("Bạn không có thẩm quyền để vào trang này.")
    window.location.href = "/"
}

// Chart loai sach
const ctx = document.getElementById('chart1').getContext('2d');

var thamkhao = 0, truyen = 0, baitap = 0, giaokhoa = 0

fetch("/getstats", {
    method: "GET",
})
.then((response) => response.json())
.then((json) => {
    console.log(json)
    thamkhao = json["thamkhao"]
    baitap = json["baitap"]
    truyen = json["truyen"]
    giaokhoa = json["giaokhoa"]

    const chart1 = new Chart(ctx, {
        type: 'doughnut', // Chart type: 'bar', 'line', 'pie', 'doughnut', etc.
        data: {
            labels: ['Sách Giáo Khoa', 'Sách Tham Khảo', 'Sách Bài Tập', 'Sách Truyện'], // X-axis labels
            datasets: [{
                label: 'Số sách', // Legend label
                data: [giaokhoa, thamkhao, baitap, truyen], // Data for the chart
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                ],
                borderWidth: 1 // Border width of the bars
            }]
        },
        options: {
            responsive: true, // Make it responsive
            scales: {
                y: {
                    beginAtZero: true // Start the Y-axis at 0
                }
            }
        }
    })
})

function add_book() {
    const fileInput = document.getElementById("book-thumbnail");
    const file = fileInput.files[0];

    // Ensure a file is selected
    if (!file) {
        alert("Vui lòng chọn một tệp ảnh .jpg!");
        return;
    }

    // Read the file as Base64
    const reader = new FileReader();
    reader.onload = function (event) {
        const base64Image = event.target.result.split(",")[1]; // Extract Base64 part

        // Send a POST request with headers and Base64 image in the body
        fetch('/addbook', {
            method: "POST",
            headers: {
                'ID': document.getElementById("book-id").value,
                'Title': document.getElementById("book-title").value,
                'Author': document.getElementById("book-publisher").value,
                'Year': document.getElementById("book-year").value,
                'Description': document.getElementById("book-description").value,
                'Episode': document.getElementById("book-ep").value,
                'Use': document.getElementById("book-type").value,
                'Content-Type': 'text/plain', // Indicate plain text for body
            },
            body: base64Image, // Include the image as a plain string
        })
        .then((response) => response.json())
        .then((json) => {
            console.log(json);
            alert("Sách đã được thêm thành công!");
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Có lỗi xảy ra!");
        });
    };

    // Read the file
    reader.readAsDataURL(file);
}

function add_id() {
    const fileInput = document.getElementById("book-thumbnail2");
    const file = fileInput.files[0];
    const reader = new FileReader();

    // Ensure a file is selected
    if (!file) {
        // Send a POST request with headers and Base64 image in the body
        fetch('/addbook', {
            method: "POST",
            headers: {
                'ID': document.getElementById("book-id").value,
                'Episode': document.getElementById("book-ep").value,
            },
        })
        .then((response) => response.json())
        .then((json) => {
            console.log(json);
            if (json["success"]) alert("Sách đã được thêm thành công!");
            else alert(json["error"])
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Có lỗi xảy ra: " + error);
        });
    }
    else {
        // Read the file as Base64
        const reader = new FileReader();
        reader.onload = function (event) {
            const base64Image = event.target.result.split(",")[1]; // Extract Base64 part
            console.log("Image detected")
            // Send a POST request with headers and Base64 image in the body
            fetch('/addbook', {
                method: "POST",
                headers: {
                    'ID': document.getElementById("book-id2").value,
                    'Episode': document.getElementById("book-ep2").value,
                    'Content-Type': 'text/plain', // Indicate plain text for body
                    'Content-Length': base64Image.length.toString()
                },
                body: base64Image, // Include the image as a plain string
            })
            .then((response) => response.json())
            .then((json) => {
                console.log(json);
                if (json["success"]) alert("Sách đã được thêm thành công!");
                else alert(json["error"])
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Có lỗi xảy ra: " + error);
            });
        };
        // Read the file
        reader.readAsDataURL(file);
    }
}

function del_borrow() {
    fetch("/delborrow", {
        method: "GET",
        headers: {
            "Id": document.getElementById("book-code").value
        }
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json)
        if (json["success"]) alert("Sách đã được trả lại!");
        else alert(json["error"])
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("Có lỗi xảy ra: " + error);
    })
}
