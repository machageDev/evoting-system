'use strict';
{
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    function setTheme(mode) {
        if (mode !== "light" && mode !== "dark" && mode !== "auto") {
            console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
            mode = "auto";
        }
        document.documentElement.dataset.theme = mode;
        localStorage.setItem("theme", mode);
    }

    function cycleTheme() {
        const currentTheme = localStorage.getItem("theme") || "auto";
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

        if (prefersDark) {
            // Auto (dark) -> Light -> Dark
            if (currentTheme === "auto") {
                setTheme("light");
            } else if (currentTheme === "light") {
                setTheme("dark");
            } else {
                setTheme("auto");
            }
        } else {
            // Auto (light) -> Dark -> Light
            if (currentTheme === "auto") {
                setTheme("dark");
            } else if (currentTheme === "dark") {
                setTheme("light");
            } else {
                setTheme("auto");
            }
        }
    }

    function initTheme() {
        // set theme defined in localStorage if there is one, or fallback to auto mode
        const currentTheme = localStorage.getItem("theme");
        currentTheme ? setTheme(currentTheme) : setTheme("auto");
    }

    window.addEventListener('load', function(_) {
        const buttons = document.getElementsByClassName("theme-toggle");
        Array.from(buttons).forEach((btn) => {
            btn.addEventListener("click", cycleTheme);
        });
    });

    initTheme();
=======
=======
=======
>>>>>>> c5b4b76 (admin static files)
=======
>>>>>>> 76a1a11 (admin static files)
=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> c63776d (admin static files)
>>>>>>> f670750 (admin static files)
    window.addEventListener('load', function(e) {

        function setTheme(mode) {
            if (mode !== "light" && mode !== "dark" && mode !== "auto") {
                console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
                mode = "auto";
            }
            document.documentElement.dataset.theme = mode;
            localStorage.setItem("theme", mode);
        }

        function cycleTheme() {
            const currentTheme = localStorage.getItem("theme") || "auto";
            const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

            if (prefersDark) {
                // Auto (dark) -> Light -> Dark
                if (currentTheme === "auto") {
                    setTheme("light");
                } else if (currentTheme === "light") {
                    setTheme("dark");
                } else {
                    setTheme("auto");
                }
            } else {
                // Auto (light) -> Dark -> Light
                if (currentTheme === "auto") {
                    setTheme("dark");
                } else if (currentTheme === "dark") {
                    setTheme("light");
                } else {
                    setTheme("auto");
                }
            }
        }

        function initTheme() {
            // set theme defined in localStorage if there is one, or fallback to auto mode
            const currentTheme = localStorage.getItem("theme");
            currentTheme ? setTheme(currentTheme) : setTheme("auto");
        }

        function setupTheme() {
            // Attach event handlers for toggling themes
            const buttons = document.getElementsByClassName("theme-toggle");
            Array.from(buttons).forEach((btn) => {
                btn.addEventListener("click", cycleTheme);
            });
            initTheme();
        }

        setupTheme();
    });
<<<<<<< HEAD
>>>>>>> c25daed (change)
=======
<<<<<<< HEAD
=======
=======
=======
>>>>>>> bca57da (change)
=======
>>>>>>> b57a7f8 (admin static files)
=======
>>>>>>> 98751f7 (admin static files)
    function setTheme(mode) {
        if (mode !== "light" && mode !== "dark" && mode !== "auto") {
            console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
            mode = "auto";
        }
        document.documentElement.dataset.theme = mode;
        localStorage.setItem("theme", mode);
    }

    function cycleTheme() {
        const currentTheme = localStorage.getItem("theme") || "auto";
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

        if (prefersDark) {
            // Auto (dark) -> Light -> Dark
            if (currentTheme === "auto") {
                setTheme("light");
            } else if (currentTheme === "light") {
                setTheme("dark");
            } else {
                setTheme("auto");
            }
        } else {
            // Auto (light) -> Dark -> Light
            if (currentTheme === "auto") {
                setTheme("dark");
            } else if (currentTheme === "dark") {
                setTheme("light");
            } else {
                setTheme("auto");
            }
        }
    }

    function initTheme() {
        // set theme defined in localStorage if there is one, or fallback to auto mode
        const currentTheme = localStorage.getItem("theme");
        currentTheme ? setTheme(currentTheme) : setTheme("auto");
    }

    window.addEventListener('load', function(_) {
        const buttons = document.getElementsByClassName("theme-toggle");
        Array.from(buttons).forEach((btn) => {
            btn.addEventListener("click", cycleTheme);
        });
    });

    initTheme();
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> a420006 (production settings)
=======
=======
>>>>>>> b57a7f8 (admin static files)
=======
=======
=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> c63776d (admin static files)
>>>>>>> f670750 (admin static files)
    window.addEventListener('load', function(e) {

        function setTheme(mode) {
            if (mode !== "light" && mode !== "dark" && mode !== "auto") {
                console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
                mode = "auto";
            }
            document.documentElement.dataset.theme = mode;
            localStorage.setItem("theme", mode);
        }

        function cycleTheme() {
            const currentTheme = localStorage.getItem("theme") || "auto";
            const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

            if (prefersDark) {
                // Auto (dark) -> Light -> Dark
                if (currentTheme === "auto") {
                    setTheme("light");
                } else if (currentTheme === "light") {
                    setTheme("dark");
                } else {
                    setTheme("auto");
                }
            } else {
                // Auto (light) -> Dark -> Light
                if (currentTheme === "auto") {
                    setTheme("dark");
                } else if (currentTheme === "dark") {
                    setTheme("light");
                } else {
                    setTheme("auto");
                }
            }
        }

        function initTheme() {
            // set theme defined in localStorage if there is one, or fallback to auto mode
            const currentTheme = localStorage.getItem("theme");
            currentTheme ? setTheme(currentTheme) : setTheme("auto");
        }

        function setupTheme() {
            // Attach event handlers for toggling themes
            const buttons = document.getElementsByClassName("theme-toggle");
            Array.from(buttons).forEach((btn) => {
                btn.addEventListener("click", cycleTheme);
            });
            initTheme();
        }

        setupTheme();
    });
<<<<<<< HEAD
>>>>>>> c25daed (change)
=======
<<<<<<< HEAD
=======
=======
=======
>>>>>>> bca57da (change)
    function setTheme(mode) {
        if (mode !== "light" && mode !== "dark" && mode !== "auto") {
            console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
            mode = "auto";
        }
        document.documentElement.dataset.theme = mode;
        localStorage.setItem("theme", mode);
    }

    function cycleTheme() {
        const currentTheme = localStorage.getItem("theme") || "auto";
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

        if (prefersDark) {
            // Auto (dark) -> Light -> Dark
            if (currentTheme === "auto") {
                setTheme("light");
            } else if (currentTheme === "light") {
                setTheme("dark");
            } else {
                setTheme("auto");
            }
        } else {
            // Auto (light) -> Dark -> Light
            if (currentTheme === "auto") {
                setTheme("dark");
            } else if (currentTheme === "dark") {
                setTheme("light");
            } else {
                setTheme("auto");
            }
        }
    }

    function initTheme() {
        // set theme defined in localStorage if there is one, or fallback to auto mode
        const currentTheme = localStorage.getItem("theme");
        currentTheme ? setTheme(currentTheme) : setTheme("auto");
    }

    window.addEventListener('load', function(_) {
        const buttons = document.getElementsByClassName("theme-toggle");
        Array.from(buttons).forEach((btn) => {
            btn.addEventListener("click", cycleTheme);
        });
    });

    initTheme();
<<<<<<< HEAD
>>>>>>> a420006 (production settings)
=======
=======
    window.addEventListener('load', function(e) {

        function setTheme(mode) {
            if (mode !== "light" && mode !== "dark" && mode !== "auto") {
                console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
                mode = "auto";
            }
            document.documentElement.dataset.theme = mode;
            localStorage.setItem("theme", mode);
        }

        function cycleTheme() {
            const currentTheme = localStorage.getItem("theme") || "auto";
            const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

            if (prefersDark) {
                // Auto (dark) -> Light -> Dark
                if (currentTheme === "auto") {
                    setTheme("light");
                } else if (currentTheme === "light") {
                    setTheme("dark");
                } else {
                    setTheme("auto");
                }
            } else {
                // Auto (light) -> Dark -> Light
                if (currentTheme === "auto") {
                    setTheme("dark");
                } else if (currentTheme === "dark") {
                    setTheme("light");
                } else {
                    setTheme("auto");
                }
            }
        }

        function initTheme() {
            // set theme defined in localStorage if there is one, or fallback to auto mode
            const currentTheme = localStorage.getItem("theme");
            currentTheme ? setTheme(currentTheme) : setTheme("auto");
        }

        function setupTheme() {
            // Attach event handlers for toggling themes
            const buttons = document.getElementsByClassName("theme-toggle");
            Array.from(buttons).forEach((btn) => {
                btn.addEventListener("click", cycleTheme);
            });
            initTheme();
        }

        setupTheme();
    });
>>>>>>> c25daed (change)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> bca57da (change)
>>>>>>> c63776d (admin static files)
<<<<<<< HEAD
>>>>>>> f670750 (admin static files)
=======
=======
>>>>>>> b57a7f8 (admin static files)
<<<<<<< HEAD
>>>>>>> c5b4b76 (admin static files)
=======
=======
>>>>>>> bca57da (change)
>>>>>>> c63776d (admin static files)
>>>>>>> f670750 (admin static files)
>>>>>>> 98751f7 (admin static files)
>>>>>>> 76a1a11 (admin static files)
}
