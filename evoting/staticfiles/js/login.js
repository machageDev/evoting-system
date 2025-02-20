document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent actual form submission

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            if (username === "" || password === "") {
                alert("Please fill in all fields.");
                return;
            }

            // Simulate login (Replace this with actual authentication logic)
            if (username === "admin" && password === "password") {
                localStorage.setItem("user", username);
                window.location.href = "dashboard.html";
            } else {
                alert("Invalid credentials!");
            }
        });
    }
});
