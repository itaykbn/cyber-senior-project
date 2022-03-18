

// constants
const reg_user = new RegExp(/^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$/);

// Minimum eight characters, at least one uppercase letter, one lowercase letter and one number:
const reg_pass = new RegExp(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/);

const reg_first = new RegExp();

const reg_last = new RegExp();

//email standard
const reg_email = RegExp(/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/);




function RegistrationFormValidation()
{
    // get from doc

    var username = document.getElementById().trim();
    var first_name = document.getElementById().trim();
    var last_name = document.getElementById().trim();
    var email = document.getElementById().trim();
    var password1 = document.getElementById().trim();
    var password2 = document.getElementById().trim();


    if(username.match(reg_user) != null)
    {
        if(first_name.match(reg_first) != null)
        {
            if(last_name.match(reg_last) != null)
            {
                if(email.match(reg_email) != null)
                {
                    if(password1.match(reg_pass) != null)
                    {
                        if(password1 == password2)
                        {
                            return true;
                        }
                    }
                }
            }
        }
    }
    return false;
}
