
window.onload = function() {


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

var canvas  = $("#canvas"),
    context = canvas.get(0).getContext("2d"),
    $result = $('#result');




$('#fileInput').on( 'change', function(){
    if (this.files && this.files[0]) {
      if ( this.files[0].type.match(/^image\//) ) {
        var reader = new FileReader();
        reader.onload = function(evt) {
           $('#fileInput').css('display', 'none');
           $('#fileInputLabel').css('display', 'none');
           $('#select-wrapper').css('display', 'block');
           $('#btnCrop').css('display', 'block');

           var img = new Image();
           img.onload = function() {
             context.canvas.height = img.height;
             context.canvas.width  = img.width;
             context.drawImage(img, 0, 0);
             var cropper = canvas.cropper({
               aspectRatio: 1 / 1
             });
             $('#btnCrop').click(function() {
                // Get a string base 64 data url
                var croppedImageDataURL = canvas.cropper('getCroppedCanvas').toDataURL("image/png"); 
                $result.append( $('<img style="width:450px;height:auto;border: 3px solid black;padding:5px;background:transparent;">').attr('src', croppedImageDataURL) );

                uri_string = croppedImageDataURL.substring(croppedImageDataURL.indexOf(",") +1);
                $('#uri').val(uri_string);

                $('#upload-table').css('display', 'none');


                $('#description-table').css('display', 'block');

             });


             $('#btnRestore').click(function() {
               canvas.cropper('reset');
               $result.empty();
             });

             $('#select-ratio').on('change',function(){
                    values = this.value.split("|");
                    num1 = parseInt(values[0]);
                    num2 = parseInt(values[1]);

                    //alert(num1 + "/" + num2);

                    cropper.aspectRatio = num1/num2;
                    canvas.cropper('destroy');

                    cropper = canvas.cropper({
                            aspectRatio: num1/num2
                    });


             });

           };
           img.src = evt.target.result;
		};
        reader.readAsDataURL(this.files[0]);
      }
      else {
        alert("Invalid file type! Please select an image file.");
      }
    }
    else {
      alert('No file(s) selected.');
    }
});
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