const url = new URL(window.location.href)

const code = url.searchParams.get("code")

console.log(code)

const codeDisplay = document.getElementById("codeDisplay")

codeDisplay.textContent = "Mã sách: " + code

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
  });
