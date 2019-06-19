function initial_interface() {
    var userid=$.cookie("userid");
    //alert(username);
    var form_data = new FormData();
    form_data.append("userid",userid);
    $.ajax({
        type: "POST",
        url: "/sethomepage/",
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
                $.cookie("img_dir",img_dir,{ expires: 7, path:'/', secure: false });
                // alert("username: "+username);
                $("#txt_username").text(username);
                $("#txt_username_detail").text(username);
                $("#txt_userslogan").text(slogan);
                document.getElementById("img_icon").src = img_dir;
                document.getElementById("img_icon_detial").src = img_dir;
                // console.log(img_dir);
                for (var i = 0; i < bookdata.length; i++) {
                    var $trTemp = $("<tr></tr>");
                    $trTemp.append("<td><a onclick='openvbook(\""+bookdata[i].bookname+"\")'>" + bookdata[i].bookname + "</a></td>");
                    $trTemp.append("<td>" + bookdata[i].wordnum + "</td>");
                    $trTemp.append('<td><div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: ' + bookdata[i].ratio + '%;"></div> </div></td>');
                    $trTemp.appendTo("#tbdata_book");
                }
                for (i = 0; i < notedata.length; i++) {
                    $trTemp = $("<tr></tr>");
                    $trTemp.append("<td><a onclick='openvnote(\""+notedata[i].notename+"\")'>" + notedata[i].notename + "</a></td>");
                    $trTemp.append("<td>" + notedata[i].wordnum + "</td>");
                    $trTemp.append('<td><div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: ' + notedata[i].ratio + '%;"></div> </div></td>');
                    $trTemp.appendTo("#tbdata_note");
                }

            } else {
                alert("未登录");
                open("/login/", "_self");
            }
        },
        error: function (returndata) {
            alert("未登录");
            open("/login/", "_self");
        }
    });
}

function ChgUserHead() {
    var userid=$.cookie("userid");
    var form_data = new FormData();
    var file_info = $("#newimg")[0].files[0];
    var ftype = $("#newimg").val();
    if (ftype == null) {
        alert("请上传新头像");
        return;
    } else if (!/.(jpg|jpeg|png)$/.test(ftype)) {
        alert("头像图片请上传.png,.jpg,.jpeg格式图片");
        return;
    }
    form_data.append('headimg', file_info);
    form_data.append('userid', userid);
    $.ajax({
        type: "POST",
        url: "/chg_userhead/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            alert(returndata);
            open("/homepage/", "_self");
        },
        error: function (returndata) {
            alert("修改失败");
        }
    });
}

function ChgUserName() {
    var oldusername=$.cookie("username");
    var form_data = new FormData();
    var newname = $("#newname").val();
    if(!newname)
    {
        alert("请输入新用户名");
        return;
    }
    form_data.append("newname", newname);
    form_data.append("oldname", oldusername);
    $.ajax({
        type: "POST",
        url: "/chg_username/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            alert(returndata);
            $.cookie("username",newname);
            open("/homepage/", "_self");
        },
        error: function (returndata) {
            alert("修改失败");
        }
    });
}

function ChgUserSlogan() {
    var username=$.cookie("username");
    var form_data = new FormData();
    var slogan = $("#newslogan").val();
    form_data.append("slogan", slogan);
    form_data.append("username", username);
    $.ajax({
        type: "POST",
        url: "/chg_userslogan/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            alert(returndata);
            open("/homepage/", "_self");
        },
        error: function (returndata) {
            alert("修改失败");
        }
    });
}

function Init_book_popwindows() {
    var userid=$.cookie("userid");
    var form_data = new FormData();
    form_data.append("userid", userid);
    $.ajax({
        type: "POST",
        url: "/init_popwind_book_home/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            return_data = JSON.parse(returndata);
            if (return_data['result'] == 1) {
                var havebookdata = return_data['belong'];
                var unhavebookdata = return_data['unbelong'];
                var parent = document.getElementById("table_have_book");
                var childs = parent.childNodes;
                for (var i = childs.length - 1; i >= 0; i--) {
                    parent.removeChild(childs[i]);
                }
                parent = document.getElementById("table_unhave_book");
                childs = parent.childNodes;
                for (i = childs.length - 1; i >= 0; i--) {
                    parent.removeChild(childs[i]);
                }
                for (i = 0; i < havebookdata.length; i++) {
                    var $trTemp = $("<div></div>");
                    $trTemp.append("<div class='col-xs-8'>" + havebookdata[i] + "</div>");
                    $trTemp.append("<div class='col-xs-4'><button class='btn btn-xs' onclick='del_book(\"" + havebookdata[i] + "\")'>&times;</button></div>");
                    $trTemp.appendTo("#table_have_book");
                }
                for (i = 0; i < unhavebookdata.length; i++) {
                    var $trTemp = $("<div></div>");
                    $trTemp.append("<div class='col-xs-8'>" + unhavebookdata[i] + "</div>");
                    $trTemp.append("<div class='col-xs-4'><button class='btn btn-xs' onclick='add_book(\"" + unhavebookdata[i] + "\")'>+</button></div>");
                    $trTemp.appendTo("#table_unhave_book");
                }
            } else {
                alert("未登录");
                open("/login/", "_self");
            }
        },
        error: function (returndata) {
            alert("未登录");
            open("/login/", "_self");
        }
    });
}

function del_book(book) {
    var userid=$.cookie("userid");
    var form_data = new FormData();
    form_data.append("userid", userid);
    form_data.append("book", book);
    $.ajax({
        type: "POST",
        url: "/del_book_user/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            alert(returndata);
        },
        error: function (returndata) {
            alert("删除失败");
        }
    });
    open("/homepage/", "_self");
}

function add_book(book) {
    var userid=$.cookie("userid");
    var form_data = new FormData();
    form_data.append("book", book);
    form_data.append("userid", userid);
    $.ajax({
        type: "POST",
        url: "/add_book_user/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            alert(returndata);
        },
        error: function (returndata) {
            alert("添加失败");
        }
    });
    open("/homepage/", "_self");
}

function Init_note_popwindows() {
    var userid=$.cookie("userid");
    var form_data = new FormData();
    form_data.append("userid", userid);
    $.ajax({
        type: "POST",
        url: "/init_popwind_note_home/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            return_data = JSON.parse(returndata);
            if (return_data['result'] == 1) {
                var notedata = return_data['note'];
                var parent = document.getElementById("table_have_note");
                var childs = parent.childNodes;
                for (var i = childs.length - 1; i >= 0; i--) {
                    parent.removeChild(childs[i]);
                }
                for (i = 0; i < notedata.length; i++) {
                    var $trTemp = $("<div></div>");
                    $trTemp.append("<div class='col-xs-8'>" + notedata[i] + "</div>");
                    $trTemp.append("<div class='col-xs-4'><button class='btn btn-xs' onclick='del_note(\"" + notedata[i] + "\")'>&times;</button></div>");
                    $trTemp.appendTo("#table_have_note");
                }
            } else {
                alert("未登录");
                open("/login/", "_self");
            }
        },
        error: function (returndata) {
            alert("未登录");
            open("/login/", "_self");
        }
    });
}

function del_note(note) {
    var form_data = new FormData();
    form_data.append("note", note);
    $.ajax({
        type: "POST",
        url: "/del_note_user/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            alert(returndata);
        },
        error: function (returndata) {
            alert("删除失败");
        }
    });
    open("/homepage/", "_self");
}

function add_note() {
    var newnotename = $("#newnote").val();
    var userid=$.cookie("userid");
    if (!newnotename)
    {
        alert("请输入单词本名称");
        return;
    }
    else
    {
        var form_data = new FormData();
        form_data.append("note", newnotename);
        form_data.append("userid", userid);
        $.ajax({
            type: "POST",
            url: "/add_note_user/",
            data: form_data,
            processData: false,
            contentType: false,
            success: function (returndata) {
                alert(returndata);
            },
            error: function (returndata) {
                alert("添加失败");
            }
        });
    }
    open("../homepage/", "_self");
}

function openvbook(bookname=null)
{
    var userid=$.cookie("userid");
    if(bookname==null)
    {
        open("/vocabubook/"+userid.toString()+"/","_self");
    }
    else
    {
        open("/vocabubook/"+userid.toString()+"/"+bookname+"/","_self");
    }
}

function openvnote(notename=null)
{
    var userid=$.cookie("userid");
    if(notename==null)
    {
        open("/vocabunote/"+userid.toString()+"/","_self");
    }
    else
    {
        open("/vocabunote/"+userid.toString()+"/"+notename+"/","_self");
    }
}
