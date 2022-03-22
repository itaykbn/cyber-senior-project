HTMLS = [];


function AJAX_query(){
    $.ajax({
        type: 'GET',
        url: '/ajax_request/',
        datatype: "json",
        tryCount : 0,
        retryLimit : 3,
        success: function(data){
                HTMLS = data["HTMLS"]
                alert(data)
        },//success
        error: function(){
            if (textStatus == 'timeout') {
                this.tryCount++;
                if (this.tryCount <= this.retryLimit) {
                    //try again
                    $.ajax(this);
                    return;
                }
                return;
            }
            if (xhr.status == 500) {
                alert("error 500")
            } else {
                alert("error balls are heavy")
            }
            }//error
    });//.ajax
};//AJAX_query


window.addEventListener('scroll',() => {
    if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight){
        if(HTMLS.length > 0)
        {
            load_images()
        }
        else
        {
            AJAX_query()
            load_images()
        }
    }
})


function load_images(num_images = 2)
{
    let i = 0
    while(i<num_images)
    {
        const post_panel = $("#post_pane")

        post_pane.insertAdjacentHTML("beforeend",post_panel)
    }


}


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

classes = ["home","explore","create","compass","heart"];
function change_background(selector)
{
   //classes.forEach((item, index)=>{
	 //   document.getElementsByClassName(item).style.backgroundColor = 'transparent' ;
   //})
   //alert(selector)
   document.getElementsByClassName(selector).style.backgroundColor = 'grey';

}



