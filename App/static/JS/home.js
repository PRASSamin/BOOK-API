function displayMessage() {
  const currentTime = new Date().getTime();
  const lastDisplayTime = localStorage.getItem("lastDisplayTime");

  if (
    !lastDisplayTime ||
    currentTime - parseInt(lastDisplayTime) > 60 * 60 * 1000
  ) {
    document.getElementById("Note").style.animation = "show 0.4s forwards";
    document.getElementById("Note").classList.remove("hidden");
    document.querySelector("body").classList.add("overflow-hidden");
    document.querySelector("body").classList.add("select-none");
    localStorage.setItem("lastDisplayTime", currentTime);
  }
}

displayMessage();

setInterval(displayMessage, 30 * 60 * 1000);

document
  .getElementById("closeNote")
  .addEventListener("click", function (event) {
    document.getElementById("Note").style.animation = "hide 0.4s forwards";
    document.querySelector("body").classList.remove("overflow-hidden");
    document.querySelector("body").classList.remove("select-none");
    setTimeout(() => {
      document.getElementById("Note").classList.add("hidden");
    }, 400)
  });

function toggleDropdown(element) {
  const dropdown = element.nextElementSibling;
  dropdown.classList.toggle("show");
  dropdown.classList.toggle("hidden");
}

const loader = document.getElementById("loader");

document
  .getElementById("mailForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    loader.style.display = "grid";

    var formData = new FormData(this);
    const toastMsg = document.getElementById("toastMsg");
    const toastCont = document.getElementById("toastCont");
    const msg = document.getElementById("msg");
    try {
      fetch("/api/documentations", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          loader.style.display = "none";
          if (data.success) {
            toastCont.style.display = "block";
            msg.style.backgroundColor = "#d4edda";
            msg.style.border = "1px solid #155724";
            toastMsg.style.color = "#155724";
            toastMsg.innerHTML = data.message;

            setTimeout(() => {
              toastCont.style.display = "none";
            }, 2000);
          } else {
            toastCont.style.display = "block";
            toastMsg.innerHTML = data.error;
            setTimeout(() => {
              toastCont.style.display = "none";
            }, 2000);
          }
        });
    } catch (error) {
      console.log("Error:" + error);
    }
  });

document
  .getElementById("toggleSidebarMobile")
  .addEventListener("click", (event) => {
    const navDrawer = document.getElementById("navDrawer");
    const overlay = document.getElementById("overlay");

    navDrawer.style.animation = "expanded 0.5s forwards";

    overlay.classList.remove("hidden");

    document.querySelector("body").classList.add("overflow-hidden");
  });

document.getElementById("navClose").addEventListener("click", (event) => {
  const navDrawer = document.getElementById("navDrawer");
  const overlay = document.getElementById("overlay");

  navDrawer.style.animation = "collapsed 0.5s forwards";

  overlay.classList.add("hidden");

  document.querySelector("body").classList.remove("overflow-hidden");
});

function copyCode(button) {
  const codeElement =
    button.parentElement.parentElement.parentElement.nextElementSibling.querySelector(
      "code"
    );

  const textArea = document.createElement("textarea");

  textArea.value = codeElement.innerText;
  document.body.appendChild(textArea);
  textArea.select();
  textArea.setSelectionRange(0, 99999);

  document.execCommand("copy");

  document.body.removeChild(textArea);
}
