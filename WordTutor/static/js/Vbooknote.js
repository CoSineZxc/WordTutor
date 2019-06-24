function initial_vnavbar(book)
{
    var username=$.cookie("username");
    var img_dir=$.cookie("img_dir");
    $("#txt_username").text(username);
    document.getElementById("img_icon").src = img_dir;
    //$("#img_icon").src=img_dir;
}

function show_answer()
{
    document.getElementById("answer").style.visibility="visible";
}

function hidden_answer()
{
    document.getElementById("answer").style.visibility="hidden";
}

function check_spell()
{
    var realSpell=$("#real_spell").text();
    var userSpell=$("#edt_spell").val();
    if(!userSpell)
    {
        alert("请输入拼写");
    }
    else if(realSpell==userSpell)
    {
        //$("#show_spell_result").removeClass()
        $("#show_spell_result").attr("class", "form-group has-success");
        alert("拼写正确");
    }
    else
    {
        $("#show_spell_result").attr("class", "form-group has-error");
        alert("拼写错误");
        var userSpell=$("#edt_spell").val("");
    }
}

function check_mean()
{
    var realmean=$("#real_mean").text();
    var usermean=$("input:radio:checked").val();
    if(!usermean)
    {
        alert("请做出选择");
    }
    else if(realmean==usermean)
    {
        //$("#show_spell_result").removeClass()
        $("#show_mean_result").attr("class", "form-group has-success");
        alert("选择正确");
    }
    else
    {
        $("#show_mean_result").attr("class", "form-group has-error");
        alert("选择错误");
    }
}

function Init_Add2Note_popwindows()
{
    var userid=$.cookie("userid");
    var form_data = new FormData();
    form_data.append("userid", userid);
    var word=$("#real_spell").text();
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
                    $trTemp.append("<div class='col-xs-4'><button class='btn btn-xs' onclick='Add2Note(\"" + notedata[i] + "\",\""+word+"\")'>+</button></div>");
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

function Add2Note(note,word)
{
    var userid=$.cookie("userid");
    var form_data = new FormData();
    form_data.append("userid", userid);
    form_data.append("notename", note);
    form_data.append("addword", word);
    $.ajax({
        type: "POST",
        url: "/add_word2note/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            alert(returndata);
        }
    });
}

function move2last()
{
    var nowli=$("#selected");
    var nowword=nowli.text();
    var preli=$("#selected").prev();
    var preword=preli.text();
    if(preword=="")
    {
        alert("第一个啦");
    }
    else
    {
        $("#selected").removeClass("list-group-item-success");
        $("#selected").removeAttr('id');
        nowli.attr('id',nowword);
        preli.remove('id');
        preli.attr('id',"selected");
        $("#selected").addClass("list-group-item-success");
        ChgWordNow(preword);
    }

}

function move2next()
{
    var nowli=$("#selected");
    var nextli=$("#selected").next();
    var nextword=nextli.text();
    var nowword=nowli.text();
    if(nextword=="")
    {
        alert("最后一个啦");
    }
    else
    {
        $("#selected").removeClass("list-group-item-success");
        $("#selected").removeAttr('id');
        nowli.attr('id',nowword);
        nextli.remove('id');
        nextli.attr('id',"selected");
        $("#selected").addClass("list-group-item-success");
        ChgWordNow(nextword);
    }
}

function jmp2word(word)
{
    var oldli=$("#selected");
    var word_old=$("#selected").text();
    var futureli=$("#"+word);
    $("#selected").removeClass("list-group-item-success");
    $("#selected").removeAttr('id');
    oldli.attr('id',word_old);
    futureli.remove('id');
    futureli.attr('id',"selected");
    $("#selected").addClass("list-group-item-success");
    ChgWordNow(word);
}

function ChgWordNow(word)
{
    $("#show_spell_result").attr("class","form-group");
    $("#show_mean_result").attr("class","form-group");
    $('#voice_test').attr('src',"http://dict.youdao.com/dictvoice?audio="+word);
    var voice_test=$('#voice_test').get('0');
    voice_test.load();
    $("#real_spell").text(word);
    $('#real_voice').attr('src',"http://dict.youdao.com/dictvoice?audio="+word);
    var real_voice=$('#real_voice').get('0');
    real_voice.load();
    var form_data = new FormData();
    form_data.append("newword", word);
    $.ajax({
        type: "POST",
        url: "/word_next/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            return_data = JSON.parse(returndata);
            var truemean=return_data["true_mean"];
            $("#real_mean").text(truemean);
            var select_list=return_data["Select_answer"];
            var radio_group=$("#radio_group");
            radio_group.empty();
            for(var i=0;i<3;i++)
            {
                var $trTemp = $("<div class='radio'></div>");
                $trTemp.append("<input type=\"radio\" name=\"optionsRadios\" value=\""+select_list[i]+"\"/>"+select_list[i]);
                $trTemp.appendTo("#radio_group");
            }
        }
    });
}

function delete_word()
{
    var userid=$.cookie("userid");
    var word=$("#real_spell").text();
    var notename=$("#notename").text();
    var form_data=new FormData;
    form_data.append("userid",userid);
    form_data.append("notename",notename);
    form_data.append("delword", word);
    $.ajax({
        type: "POST",
        url: "/word_del/",
        data: form_data,
        processData: false,
        contentType: false,
        success: function (returndata) {
            alert(returndata);
        }
    });
}