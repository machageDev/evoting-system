document.addEventListener("DOMContentLoaded", function () {
    // ✅ FORM VALIDATION FOR CREATE & EDIT USER FORMS
    const userForm = document.querySelector("form");
    if (userForm) {
        userForm.addEventListener("submit", function (event) {
            const username = document.getElementById("username").value.trim();
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password");

            if (username === "" || email === "") {
                alert("Username and Email are required.");
                event.preventDefault();
                return;
            }

            if (password && password.value.length > 0 && password.value.length < 6) {
                alert("Password must be at least 6 characters long.");
                event.preventDefault();
                return;
            }
        });
    }

    // ✅ PASSWORD STRENGTH CHECKER (FOR CREATE & EDIT USER FORMS)
    const passwordInput = document.getElementById("password");
    if (passwordInput) {
        passwordInput.addEventListener("input", function () {
            const strengthMessage = document.getElementById("password-strength");
            const password = passwordInput.value;

            let strength = "Weak";
            if (password.length >= 6 && /[A-Z]/.test(password) && /[0-9]/.test(password)) {
                strength = "Medium";
            }
            if (password.length >= 8 && /[A-Z]/.test(password) && /[0-9]/.test(password) && /[^a-zA-Z0-9]/.test(password)) {
                strength = "Strong";
            }

            strengthMessage.textContent = `Password Strength: ${strength}`;
            strengthMessage.style.color = strength === "Strong" ? "green" : strength === "Medium" ? "orange" : "red";
        });
    }

    // ✅ CONFIRM DELETE USER
    const deleteButtons = document.querySelectorAll(".btn-delete-user");
    deleteButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            const confirmDelete = confirm("Are you sure you want to delete this user?");
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    });

    // ✅ ADDING SMOOTH FADE-IN EFFECT TO TABLE ROWS
    const tableRows = document.querySelectorAll("tbody tr");
    tableRows.forEach((row, index) => {
        setTimeout(() => {
            row.style.opacity = 1;
            row.style.transform = "translateY(0)";
        }, index * 100);
    });
});
