document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const username = document.getElementById("username").value;
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const confirmPassword = document.getElementById("confirm-password").value;

            if (username === "" || email === "" || password === "" || confirmPassword === "") {
                alert("All fields are required.");
                return;
            }

            if (password !== confirmPassword) {
                alert("Passwords do not match.");
                return;
            }

            // Simulate storing user data
            localStorage.setItem("registeredUser", JSON.stringify({ username, email, password }));
            alert("Registration successful! Please log in.");
            window.location.href = "login.html";
        });
    }
});
