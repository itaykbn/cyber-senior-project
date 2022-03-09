
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
                $('#uri').val(croppedImageDataURL);

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