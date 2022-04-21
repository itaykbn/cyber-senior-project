var HTMLS = [];

var flag = false;



window.addEventListener('load', (event) => {
    var pull_index = 0;
    answer =  AJAX_query(pull_index);

    HTMLS = answer[0];
    flag = answer[1];


    load_images();
    //alert("balls")
})


function AJAX_query(pull_index){
        var tmp = null;
        var finish = null;

        $.ajax({
        type: 'GET',
        async: false,
        url: '/ajax_request/',
        data: {"index":pull_index,"type":"profile"},
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


};


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
})




function load_images(num_images = 2)
{
    while(HTMLS.length > 0)
    {
        const post_panel = $("#gallery");
        gallery.insertAdjacentHTML("beforeend",HTMLS[0]);
        HTMLS.shift();
        console.log("brosky" + 0)
        console.log("hood\n" + HTMLS[0])
    }


}