function normalizeUnicode(text) {
    // Normalize to NFKD form and remove diacritics/accents by filtering combining characters
    return text.normalize('NFKD').replace(/[\u0300-\u036f]/g, "");
}

function search() {
    var oldElements = document.getElementById("result")
    while (oldElements != null) {
        oldElements.remove()
        oldElements = document.getElementById("result")
    }

    const searchContent = document.getElementById("searchbar").value.trim()
    console.log("Search Name: "+searchContent)
    if (searchContent == "") {
        alert("Xin hãy cho ít nhất một từ khóa để tìm kiếm")
        document.getElementById("searchbar").value = ""
        return null;
    }

    fetch("/get", {
        method: "GET",
        headers: {
            "Search": normalizeUnicode(searchContent)
        }
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json)
        const resultfield = document.getElementById("resultfield")
        const valid_ids = json["valid_ids"]
        const bktypes = json["bktypes"]
        const ranks = json["ranks"]
        const titles = json["titles"]
        const episodes = json["episodes"]

        for (let i in valid_ids) {
            // console.log("A"+i)

            const newElement = document.createElement("a")
            // newElement.innerText = "(" + ranks[i] + "%)" + "["+valid_ids[i]+"] " + titles[i] + "\n"
            if (episodes[i] != 0)
                newElement.innerText =titles[i] + " (Tập " + episodes[i] + ")" + "\n"
            else newElement.innerText =titles[i] + "\n"
            newElement.id = "result"
            newElement.href = "/idinfo.html?code="+valid_ids[i]
            newElement.style = "font-size: 20px; text-decoration: none; color: black; padding: 20px; text-align: center;"
            newElement.style.textAlign = "center";
            newElement.classList.add("searchres")
            newElement.style.display = "block";
            newElement.style.margin = "0 auto";
            newElement.style.fontWeight = "bold";
            newElement.style.color = "#0048a6"

            // Add the element
            resultfield.appendChild(newElement)
        }
    })
}

const url = new URL(window.location.href)

const query = url.searchParams.get("query")

if (query != null) {
    document.getElementById("searchbar").value = query
    search()
}

const username2 = getCookie("username")
if (!username2) {
    alert("Bạn cần đăng nhập để sử dụng tính năng này!")
    window.location.href = "/"
}

document.addEventListener("keydown", key => {
    if (key.code == "Enter" && document.activeElement.id == "searchbar") {
        search()
        // console.log(document.activeElement.id)
    }
})