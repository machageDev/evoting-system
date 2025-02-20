document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    
    form.addEventListener("submit", function (event) {
        let valid = true;
        const inputs = form.querySelectorAll("input, select, textarea");
        
        inputs.forEach(input => {
            if (input.hasAttribute("required") && input.value.trim() === "") {
                input.classList.add("is-invalid");
                valid = false;
            } else {
                input.classList.remove("is-invalid");
            }
        });

        if (!valid) {
            event.preventDefault(); // Prevent submission if validation fails
            alert("Please fill out all required fields.");
        }
    });
});
