const loader = document.getElementById("loader");

document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    loader.style.display = "grid";

    var formData = new FormData(this);

    try {
      fetch("/api/login", {
        method: "POST",
        body: formData,
      })
        .then((Response) => Response.json())
        .then((data) => {
          loader.style.display = "none";
          if (data.error) {
            document.getElementById("StatusSuccess").style.display = "block";
            document.getElementById("MessageSuccess").innerHTML = data.error;
            setTimeout(function () {
              document.getElementById("StatusSuccess").style.display = "none";
            }, 1000);
          } else {
            document.getElementById("StatusSuccess").style.display = "block";
            document.getElementById("MessageSuccess").innerHTML =
              "Login Successful. Redirecting...";
            setTimeout(function () {
              document.getElementById("StatusSuccess").style.display = "none";
              window.location.replace("/api/pras/book/db/add");
            }, 1000);
          }
        });
    } catch (error) {
      console.log(error);
    }
  });

const eyeBtn = document.getElementById("eyeBtn");
const eye = document.getElementById("eye");

eye.addEventListener("click", function (e) {
  e.preventDefault();
  var input = document.getElementById("code");

  if (input.type === "password") {
    input.type = "text";
    eye.src = "/static/hidden.png";
  } else {
    input.type = "password";
    eye.src = "/static/view.png";
  }
});
