document.addEventListener("DOMContentLoaded", function () {
    const user = localStorage.getItem("user");
    const logoutBtn = document.getElementById("logout-btn");

    if (user) {
        document.getElementById("user-greeting").textContent = `Welcome, ${user}`;
    }

    if (logoutBtn) {
        logoutBtn.addEventListener("click", function () {
            localStorage.removeItem("user");
            window.location.href = "login.html";
        });
    }
});
