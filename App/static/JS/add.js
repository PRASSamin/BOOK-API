submit = document.getElementById("bookForm");
bTitle = document.getElementById("bookName");
bAuthor = document.getElementById("bookAuthor");
bPublisher = document.getElementById("bookPublisher");
bGenre = document.getElementById("bookGenre");
bLang = document.getElementById("bookLang");
bPublished = document.getElementById("bookPublished");
bPage = document.getElementById("bookPage");
bISBN = document.getElementById("ISBN");
addStatusSuccess = document.getElementById("StatusSuccess");
addStatusFailure = document.getElementById("StatusFailure");

document
  .getElementById("bookForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    if (
      bTitle.value == "" ||
      bAuthor.value == "" ||
      bPublisher.value == "" ||
      bGenre.value == "" ||
      bLang.value == "" ||
      bPublished.value == "" ||
      bPage.value == "" ||
      bISBN.value == ""
    ) {
      bTitle.style.border = "2px solid red";
      bAuthor.style.border = "2px solid red";
      bPublisher.style.border = "2px solid red";
      bGenre.style.border = "2px solid red";
      bLang.style.border = "2px solid red";
      bPublished.style.border = "2px solid red";
      bPage.style.border = "2px solid red";
      bISBN.style.border = "2px solid red";
      addStatusFailure.style.display = "block";
      document.getElementById("MessageFailure").innerHTML =
        "Please fill all the fields";
      setTimeout(() => {
        addStatusFailure.style.display = "none";
      }, 1000);
      return;
    }

    if (bPage.value == Text) {
      addStatusFailure.style.display = "block";
      document.getElementById("MessageFailure").innerHTML =
        "No of page should be a number";
      setTimeout(() => {
        addStatusFailure.style.display = "none";
      }, 1000);
    }

    var formData = new FormData(this);

    try {
      fetch("/api/pras/book/db/add", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            addStatusSuccess.style.display = "block";
            document.querySelector(".alert").innerHTML = data.message;
            setTimeout(() => {
              addStatusSuccess.style.display = "none";
            }, 1000);
            document.getElementById("bookForm").reset();
            bAuthor.style.border = "";
            bTitle.style.border = "";
            bPublisher.style.border = "";
            bGenre.style.border = "";
            bLang.style.border = "";
            bPublished.style.border = "";
            bPage.style.border = "";
            bISBN.style.border = "";
          } else {
            addStatusFailure.style.display = "block";
            document.querySelector(".alert").innerHTML = data.error;
            setTimeout(() => {
              addStatusFailure.style.display = "none";
            }, 1000);
          }
        });
    } catch (error) {
      console.log(error);
    }
  });

async function pasteButton(element) {
  const inputField = element.nextElementSibling;
  const text = await navigator.clipboard.readText();
  inputField.focus();
  try {
    console.log(text);
    inputField.value += text;
  } catch (error) {
    console.log("error:" + error);
  }
}

function showInfo() {
  const info = document.getElementById("infoDia");

  info.style.display = "flex";

  setTimeout(() => {
    info.style.display = "none";
  }, 2000);
}
