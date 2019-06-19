function initial_vbook(book)
{
    var form_data = new FormData();
    form_data.append("book", book);
    $.ajax({
        type: "POST",
        url: "/setvbook/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            return_data = JSON.parse(returndata);
            if (return_data['result'] == 1) {
                var username = return_data['username'];
                var notedata = return_data['notes'];
                var bookdata = return_data['book'];
                var slogan = return_data['slogan'];
                var img_dir = return_data['Headdir'];
                // alert("username: "+username);
                $("#txt_username").text(username);
                $("#txt_username_detail").text(username);
                $("#txt_userslogan").text(slogan);
                document.getElementById("img_icon").src = img_dir;
                document.getElementById("img_icon_detial").src = img_dir;
                // console.log(img_dir);
                for (var i = 0; i < bookdata.length; i++) {
                    var $trTemp = $("<tr></tr>");
                    $trTemp.append("<td><a href='../vocabubook/'>" + bookdata[i].bookname + "</a></td>");
                    $trTemp.append("<td>" + bookdata[i].wordnum + "</td>");
                    $trTemp.append('<td><div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: ' + bookdata[i].ratio + '%;"></div> </div></td>');
                    $trTemp.appendTo("#tbdata_book");
                }
                for (i = 0; i < notedata.length; i++) {
                    $trTemp = $("<tr></tr>");
                    $trTemp.append("<td><a href='../vocabunote/'>" + notedata[i].notename + "</a></td>");
                    $trTemp.append("<td>" + notedata[i].wordnum + "</td>");
                    $trTemp.append('<td><div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: ' + notedata[i].ratio + '%;"></div> </div></td>');
                    $trTemp.appendTo("#tbdata_note");
                }

            } else {
                alert("未登录");
                open("../login/", "_self");
            }
        },
        error: function (returndata) {
            alert("未登录");
            open("../login/", "_self");
        }
    });
}