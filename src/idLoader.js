
const url = new URL(window.location.href)

const code = url.searchParams.get("code")

console.log(code)

const codeDisplay = document.getElementById("codeDisplay")

codeDisplay.textContent = "Mã sách: " + code

function convertTimestamp(timestamp) {
  // Array of weekday names
  const weekdays = ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"];

  // Create a new Date object with the Unix timestamp (in milliseconds)
  const date = new Date(timestamp * 1000); // Convert seconds to milliseconds

  // Get the day of the week, day, month, and year
  const dayOfWeek = weekdays[date.getUTCDay()]; // Use getUTCDay() to avoid timezone issues
  const day = String(date.getUTCDate()).padStart(2, '0'); // Ensure day is two digits
  const month = String(date.getUTCMonth() + 1).padStart(2, '0'); // Months are zero-based
  const year = date.getUTCFullYear();

  // Format the date as "Weekday, dd-mm-yyyy"
  return `${dayOfWeek}, ${day}-${month}-${year}`;
}

fetch("/get", {
    method: "GET",
    headers: {
        "Request": code
    }
})
  .then((response) => response.json())
  .then((json) => {
    console.log(json)
    if (json["id"] == "null" && json["type"]  == "null") window.location.href="/"
    console.log("Checking step 1...")

    // Create elements variables for easy later use
    var borrowerEl = document.getElementById("borrowerpar")
    var borrowdayEl = document.getElementById("borrowdaypar")
    var borrowexpireEl = document.getElementById("borrowexpirepar")
    // If there is no borrower
    if (json["borrower"] == "0" && borrowerEl) {
      console.log("Yes")

      // Remove all elements related to
      borrowerEl.remove()
      borrowdayEl.remove()
      borrowexpireEl.remove()
    }
    else {
      borrowerEl = document.getElementById("borrower")
      borrowdayEl = document.getElementById("borrowday")
      borrowexpireEl = document.getElementById("borrowexpire")

      borrowerEl.textContent = json["borrower"]

      const curTime = Math.floor(Date.now() / 1000);
      if (curTime > json["borrow_expire"]) {
        borrowdayEl.textContent = convertTimestamp(json["borrow_date"])
        borrowdayEl.style = "color: red;"
        borrowexpireEl.textContent = convertTimestamp(json["borrow_expire"]) + " [Quá Hạn!]"
        borrowexpireEl.style = "color: red;"
      }
      else {
        borrowdayEl.textContent = convertTimestamp(json["borrow_date"])
        borrowexpireEl.textContent = convertTimestamp(json["borrow_expire"])
      }
    }

    const nameEl = document.getElementById("name")
    const authorEl = document.getElementById("author")
    const useEl = document.getElementById("use")
    const yearEl = document.getElementById("year")
    const descEl = document.getElementById("desc")

    nameEl.textContent = json["title"];
    nameEl.href = "/search.html?query=" + json["title"].replace(/\s+/g, "+");

    authorEl.textContent = json["author"]
    useEl.textContent = json["use"]
    yearEl.textContent = json["year_published"]
    descEl.textContent = json["description"]
  });
