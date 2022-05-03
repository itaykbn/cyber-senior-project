



window.addEventListener('load', (event) => {

    $("#profile_pic").change(function() {
        readURL(this);
    });
})
// constants
//
const reg_user = new RegExp(/^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$/);

// Minimum eight characters, at least one uppercase letter, one lowercase letter and one number:
const reg_pass = new RegExp(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/);

const reg_name = new RegExp(/[A-Za-z]/)

//email standard
const reg_email = RegExp(/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/);


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#imagePreview').css('background-image', 'url('+e.target.result +')');
            $('#imagePreview').hide();
            $('#imagePreview').fadeIn(650);
        }
        reader.readAsDataURL(input.files[0]);
    }
}


function LoginFormValidation()
{
    var username = document.getElementById("id_username").value.trim();
    var password1 = document.getElementById("id_password").value.trim();

    if(username.match(reg_user) == null)
    {
        alert("Username can only contain letters, numbers and '_' ");
        return false;
    }

    else if(password1.match(reg_pass) == null)
    {
        alert("Password should be minimum eight characters, at least one uppercase letter, one lowercase letter and one number");

        return false;
    }

    else
    {
        return true;
    }
}
function RegistrationFormValidation()
{
    // get from doc
    var username = document.getElementById("id_username").value.trim();
    var first_name = document.getElementById("id_first_name").value.trim();
    var last_name = document.getElementById("id_last_name").value.trim();
    var email = document.getElementById("id_email").value.trim();
    var password1 = document.getElementById("id_password1").value.trim();
    var password2 = document.getElementById("id_password2").value.trim();

    /*
    hood = [username,first_name,last_name,email,password1,password2]
    hood_string = ""
    for (let i = 0; i < hood.length; i++) {

        hood_string += i + ")" + hood[i] + "\n"
    }

    alert(hood_string)


    console.log("before: '" + last_name +"'")
    console.log("after: '" + last_name.trim() +"'")

    */


    if(username.match(reg_user) == null)
    {
        alert("Username can only contain letters, numbers and '_' ");
        return false;
    }

    else if(first_name.match(reg_name) == null)
    {
        alert("First name should include letters only");
        return false;
    }
    else if(last_name.match(reg_name) == null)
    {
        alert("Last name should include letters only");
        return false;
    }

    else if(email.match(reg_email) == null)
    {
        alert("Invalid email address");
        return false;
    }

    else if(password1.match(reg_pass) == null)
    {
        alert("Password should be minimum eight characters, at least one uppercase letter, one lowercase letter and one number");

        return false;
    }
    else if(password1 != password2)
    {
        alert("Passwords don't match");
        return false;
    }
    else
    {
        return true;
    }

}
