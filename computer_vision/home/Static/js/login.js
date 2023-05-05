
window.onload = function () {

    var btn_signin = document.querySelector("#btn-signin")
    var btn_register = document.querySelector("#btn-register")

    var register_form = document.querySelector("#register-form")
    var login_form = document.querySelector("#login-form")

    function toggle_element() {
        btn_signin.classList.toggle("hide")
        btn_register.classList.toggle("hide")
        register_form.classList.toggle("hide")
        login_form.classList.toggle("hide")
    }

    btn_signin.addEventListener("click", function (e) {
        e.preventDefault()
        toggle_element()
    })

    btn_register.addEventListener("click", function (e) {
        e.preventDefault()
        toggle_element()
    })

}