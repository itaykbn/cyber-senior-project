var likes_svgs = ['<svg aria-label="Unlike" class="_8-yf5 " color="#ed4956" fill="#ed4956" height="24" role="img" viewBox="0 0 48 48" width="24"><path d="M34.6 3.1c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5s1.1-.2 1.6-.5c1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path></svg>',
'<svg aria-label="Like" class="_8-yf5 " color="#262626" fill="#262626" height="24" role="img" viewBox="0 0 24 24" width="24"><path d="M16.792 3.904A4.989 4.989 0 0121.5 9.122c0 3.072-2.652 4.959-5.197 7.222-2.512 2.243-3.865 3.469-4.303 3.752-.477-.309-2.143-1.823-4.303-3.752C5.141 14.072 2.5 12.167 2.5 9.122a4.989 4.989 0 014.708-5.218 4.21 4.21 0 013.675 1.941c.84 1.175.98 1.763 1.12 1.763s.278-.588 1.11-1.766a4.17 4.17 0 013.679-1.938m0-2a6.04 6.04 0 00-4.797 2.127 6.052 6.052 0 00-4.787-2.127A6.985 6.985 0 00.5 9.122c0 3.61 2.55 5.827 5.015 7.97.283.246.569.494.853.747l1.027.918a44.998 44.998 0 003.518 3.018 2 2 0 002.174 0 45.263 45.263 0 003.626-3.115l.922-.824c.293-.26.59-.519.885-.774 2.334-2.025 4.98-4.32 4.98-7.94a6.985 6.985 0 00-6.708-7.218z"></path></svg>']


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

function handle_like(element){

    let svg_element = element.children[0];

    message = svg_element.ariaLabel;


    element.removeChild(svg_element);

    post_id = element.parentElement.parentElement.parentElement.getAttribute("data-internalid");

    const like_element = element.parentElement.parentElement.getElementsByClassName("likes")[0];


    let like_count = like_element.innerHTML;

    like_count = parseInt(like_count.substring(0, like_count.length - 6))


    if (message == "Like")
    {

        element.insertAdjacentHTML("beforeend",likes_svgs[0]);
        like_count +=1;
        like_element.innerHTML = like_count + " likes";
        report_like(1,post_id)

    }
    else
    {
        element.insertAdjacentHTML("beforeend",likes_svgs[1]);
        like_count -= 1;
        like_element.innerHTML = like_count + " likes";
        report_like(-1,post_id)
    }
}

/*
function handle_comment(element){
    post_id = element.parentElement.parentElement.getAttribute("data-internalid");
    alert(post_id)

    comment = element.parentElement.children[1];

    r = comment.innerHTML;
    console.log(r)

    upload_comment(comment, post_id);
}
*/

function report_like(value,post_id){
        $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type: 'POST',
        async: true,
        url: '/ajax_request/',
        data: {"value": value,"post_id": post_id,"type":"like" },
        dataType: "json",
        success: function(data){
            console.log("success")
        },//success

        error: function (data) {
        // alert the error if any error occured

        }
    });
}

/*
function upload_comment(comment,post_id){
        $.ajax({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
        type: 'POST',
        async: true,
        url: '/ajax_request/',
        data: {"comment":comment, "post_id": post_id,"type": "comment" },
        dataType: "json",
        success: function(data){
            console.log("success")
        },//success

        error: function (data) {
        // alert the error if any error occurred

        }
    });
}
*/
let togglestatus = true;
document.addEventListener("DOMContentLoaded", (event) => {
  console.log("hi");
  const p = document.querySelector(".profile-img");
  p.addEventListener("click", () => {
    if (togglestatus === false) {
      document.querySelector(".drop-down").style.visibility = "hidden";
      /*document
        .querySelector("#home1")
        .setAttribute(
          "d",
          "M45.5 48H30.1c-.8 0-1.5-.7-1.5-1.5V34.2c0-2.6-2.1-4.6-4.6-4.6s-4.6 2.1-4.6 4.6v12.3c0 .8-.7 1.5-1.5 1.5H2.5c-.8 0-1.5-.7-1.5-1.5V23c0-.4.2-.8.4-1.1L22.9.4c.6-.6 1.6-.6 2.1 0l21.5 21.5c.3.3.4.7.4 1.1v23.5c.1.8-.6 1.5-1.4 1.5z"
        );
      */

      togglestatus = true;
    } else if (togglestatus === true) {
      document.querySelector(".drop-down").style.visibility = "visible";
      /*document
        .querySelector("#home1")
        .setAttribute(
          "d",
          "M45.3 48H30c-.8 0-1.5-.7-1.5-1.5V34.2c0-2.6-2-4.6-4.6-4.6s-4.6 2-4.6 4.6v12.3c0 .8-.7 1.5-1.5 1.5H2.5c-.8 0-1.5-.7-1.5-1.5V23c0-.4.2-.8.4-1.1L22.9.4c.6-.6 1.5-.6 2.1 0l21.5 21.5c.4.4.6 1.1.3 1.6 0 .1-.1.1-.1.2v22.8c.1.8-.6 1.5-1.4 1.5zm-13.8-3h12.3V23.4L24 3.6l-20 20V45h12.3V34.2c0-4.3 3.3-7.6 7.6-7.6s7.6 3.3 7.6 7.6V45z"
        );
        */
      togglestatus = false;
    }
  });
});














