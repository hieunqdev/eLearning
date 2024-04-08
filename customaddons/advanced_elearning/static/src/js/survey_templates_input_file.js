$(".input_file").change(function (event) {
    var names = [];
    var base64 = [];

    if ($(this).get(0).files[0].size > 1048576) {
        alert('File is too big. Please choose a different file!');
    } else {
        var reader = new FileReader();
        var files = event.target.files;
        reader.readAsDataURL(files[0]);

        names.push($(this).get(0).files[0].name);
        $(this).closest('.box_upload').find('.name_file').val(names);

        reader.addEventListener("load", (event) => {
            base64.push(event.target.result.toString().replace(/^data:(.*,)?/, ''));
            $(this).closest('.box_upload').find('.base64_file').val(base64);
        });
    };
});
var fileName_arr = document.querySelectorAll(".name_file");
var fileBase64 = document.querySelectorAll(".base64_file");

for (var i = 0; i < fileName_arr.length; i++) {
    fileName_arr[i].setAttribute("name", i);
};

for (var i = 0; i < fileBase64.length; i++) {
    fileBase64[i].setAttribute("name", i + "base64");
};

