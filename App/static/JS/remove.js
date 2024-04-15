uid = document.getElementById("uid");
removeStatusSuccess = document.getElementById("StatusSuccess");
removeStatusFailure = document.getElementById("StatusFailure");
document
  .getElementById("bookremForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    var formData = new FormData(this);

    if (uid.value == "") {
      uid.style.border = "2px solid red";
      removeStatusFailure.style.display = "block";
      document.getElementById("MessageFailure").innerHTML =
        "Please enter a valid UID";
      setTimeout(() => {
        removeStatusFailure.style.display = "none";
      }, 1000);
      return;
    }

    fetch("/api/pras/book/db/remove", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          removeStatusSuccess.style.display = "block";
          document.getElementById("MessageSuccess").innerHTML = data.message;
          setTimeout(() => {
            removeStatusSuccess.style.display = "none";
          }, 1000);
          document.getElementById("bookremForm").reset();
        } else {
          removeStatusFailure.style.display = "block";
          document.getElementById("MessageFailure").innerHTML = data.error;
          document.getElementById("bookremForm").reset();
          setTimeout(() => {
            removeStatusFailure.style.display = "none";
          }, 1000);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
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
