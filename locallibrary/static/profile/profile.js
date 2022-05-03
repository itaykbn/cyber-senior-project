var HTMLS = [];

var flag = false;


window.addEventListener('load', (event) => {


    var pull_index = 0;
    answer =  AJAX_query(pull_index);

    HTMLS = answer[0];
    flag = answer[1];


    load_images();
})

let togglestatus = true;
document.addEventListener("DOMContentLoaded", (event) => {
  console.log("hi");
  const p = document.querySelector(".profile-img");
  p.addEventListener("click", () => {
    if (togglestatus === false) {
      document.querySelector(".drop-down").style.visibility = "hidden";

      togglestatus = true;
    } else if (togglestatus === true) {
      document.querySelector(".drop-down").style.visibility = "visible";

      togglestatus = false;
    }
  });
});

window.addEventListener('scroll',() => {
    if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight){

        if(HTMLS.length > 0)
        {
            load_images();
        }
        else
        {
            //alert("here");
            if(!flag){
                var pull_index = document.getElementsByClassName("gallery-item").length;
                answer =  AJAX_query(pull_index);

                HTMLS = answer[0];
                flag = answer[1];
                load_images();
            }

        }
    }
});


function getCookie(c_name){
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }


function handle_follow(element){
    label = element.getAttribute('aria-label');
    username = element.parentElement.parentElement.children[0].innerHTML;

    if (label == "Follow")
    {
        element.setAttribute('aria-label',"UnFollow");
        element.children[0].innerHTML = "Following";
        element.children[0].style.color = "black";
        element.style.background = "white";
        report_follow(username,1);

    }

    else
    {
        element.setAttribute('aria-label',"Follow");
        element.children[0].innerHTML = "Follow";
        element.children[0].style.color = "white";
        element.style.background = "#0095f6";
        report_follow(username,-1);

    }
}

function handle_click(element){
    console.log("handeling")
    post_id = element.parentElement.getAttribute("data-internalid");


    path = "/posts/" + post_id;
    window.location.assign(path);
}

function AJAX_query(pull_index){
        var username = document.getElementById("username").innerHTML;

        var tmp = null;
        var finish = null;

        $.ajax({
        type: 'GET',
        async: false,
        url: '/ajax_request/',
        data: {"username":username ,"index":pull_index,"type":"profile"},
        dataType: "json",
        success: function(data){
            tmp = data["HTMLS"]
            finish = data["finish"]

        },//success

        error: function (data) {
        // alert the error if any error occured

        }
    });

    return [tmp,finish];


}

function report_follow(username,value){
        $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type: 'POST',
        async: true,
        url: '/ajax_request/',
        data: {"value":value, "username": username,"type": "follow" },
        dataType: "json",
        success: function(data){
            console.log("success")
        },//success

        error: function (data) {
        // alert the error if any error occurred

        }
    });
}

function load_images(num_images = 2){
    while(HTMLS.length > 0)
    {
        const post_panel = $("#gallery");
        gallery.insertAdjacentHTML("beforeend",HTMLS[0]);
        HTMLS.shift();
        console.log("brosky" + 0)
        console.log("hood\n" + HTMLS[0])
    }


}
