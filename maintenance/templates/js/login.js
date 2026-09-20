document.addEventListener("DOMContentLoaded", function () {

    const togglePassword =
        document.getElementById("togglePassword");

    const password =
        document.getElementById("password");

    const eyeIcon =
        document.getElementById("eyeIcon");


    /*
    ========================================================
    PASSWORD SHOW / HIDE
    ========================================================
    */

    if (
        togglePassword &&
        password &&
        eyeIcon
    ) {

        togglePassword.addEventListener(
            "click",
            function () {

                if (password.type === "password") {

                    password.type = "text";

                    togglePassword.setAttribute(
                        "aria-label",
                        "Hide password"
                    );

                    eyeIcon.innerHTML = `
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M3 3l18 18"
                        />

                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M10.5 10.5
                               a2.5 2.5 0 0 0 3 3"
                        />

                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M6.7 6.7
                               C4.2 8.2 2.5 10.5 2.5 12
                               c0 0 3.5 6 9.5 6
                               1.8 0 3.4-.5 4.8-1.2"
                        />

                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M17.3 17.3
                               C19.8 15.8 21.5 13.5 21.5 12
                               c0 0-3.5-6-9.5-6
                               -1.1 0-2.1.2-3 .5"
                        />
                    `;

                } else {

                    password.type = "password";

                    togglePassword.setAttribute(
                        "aria-label",
                        "Show password"
                    );

                    eyeIcon.innerHTML = `
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            d="M2.25 12
                               s3.75-6 9.75-6
                               9.75 6 9.75 6
                               -3.75 6-9.75 6
                               -9.75-6-9.75-6z"
                        />

                        <circle
                            cx="12"
                            cy="12"
                            r="2.5"
                        />
                    `;

                }

            }
        );

    }


    /*
    ========================================================
    LOGIN FORM VALIDATION
    ========================================================
    */

    const loginForm =
        document.querySelector("form");

    const username =
        document.getElementById("username");


    if (loginForm) {

        loginForm.addEventListener(
            "submit",
            function (event) {

                let valid = true;


                /*
                ------------------------------------------------
                USERNAME
                ------------------------------------------------
                */

                if (
                    username &&
                    username.value.trim() === ""
                ) {

                    valid = false;

                    username.classList.add(
                        "border-red-500",
                        "ring-2",
                        "ring-red-200"
                    );

                    username.focus();

                }


                /*
                ------------------------------------------------
                PASSWORD
                ------------------------------------------------
                */

                if (
                    password &&
                    password.value.trim() === ""
                ) {

                    valid = false;

                    password.classList.add(
                        "border-red-500",
                        "ring-2",
                        "ring-red-200"
                    );

                    if (
                        username &&
                        username.value.trim() !== ""
                    ) {

                        password.focus();

                    }

                }


                /*
                ------------------------------------------------
                STOP SUBMISSION IF INVALID
                ------------------------------------------------
                */

                if (!valid) {

                    event.preventDefault();

                }

            }
        );

    }


    /*
    ========================================================
    REMOVE ERROR STYLE WHEN USER TYPES
    ========================================================
    */

    if (username) {

        username.addEventListener(
            "input",
            function () {

                this.classList.remove(
                    "border-red-500",
                    "ring-2",
                    "ring-red-200"
                );

            }
        );

    }


    if (password) {

        password.addEventListener(
            "input",
            function () {

                this.classList.remove(
                    "border-red-500",
                    "ring-2",
                    "ring-red-200"
                );

            }
        );

    }

});