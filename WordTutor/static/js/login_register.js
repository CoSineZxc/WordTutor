function submit_login()
{
    var username=$("#edt_username").val();
    var password=$("#edt_password").val();
    if(!username || !password)
    {
        alert("请输入用户名及密码");
    }
    else
    {
        var form_data = new FormData();
        form_data.append("username",username);
        form_data.append("password",password);
        $.ajax({
            type:"POST",
            url:"/submit_login/",
            data:form_data,
            processData:false,
            contentType:false,
            success:function(returndata){
                return_rslt=JSON.parse(returndata);
                if(return_rslt['return']==0)
                {
                    alert("登录失败");
                    $("#edt_username").val("");
                    $("#edt_password").val("");
                }
                else
                {
                    //alert("username"+username);
                    $.cookie("username",username);
                    $.cookie("password",password);
                    var userid=return_rslt['userid'];
                    $.cookie("userid",userid);
                    open_homepage();
                }
            },
            error:function(returndata){
                alert("登陆失败");
                $("#edt_username").val("");
                $("#edt_password").val("");
            }
        });
    }
}

function open_homepage()
{
    open("../homepage/","_self");
}

function submit_register()
{
    var username=$("#edt_username").val();
    var password=$("#edt_password").val();
    var password_again=$("#edt_password_again").val();
    var isletter = /^[a-zA-Z]+$/.test(password);
    var isnumber=/^[0-9]+$/.test(password);
    var islower=/^[0-9a-z]+$/.test(password);
    var isnormal=/^[0-9a-zA-Z]+$/.test(password);
    if(password!=password_again)
    {
        alert("两次密码输入保持一致");
        $("#edt_password").val("");
        $("#edt_password_again").val("");
    }
    else if(!username||!password||!password_again)
    {
        alert("请填写完整");
    }
    else if(isletter||isnumber||islower||isnormal)
    {
        alert("请在密码中加入数字、字母大小写、及特殊符号");
        $("#edt_password").val("");
        $("#edt_password_again").val("");
    }
    else
    {
        var form_data = new FormData();
        form_data.append("username",username);
        form_data.append("password",password);
        $.ajax({
            type:"POST",
            url:"/submit_register/",
            data:form_data,
            processData:false,
            contentType:false,
            success:function(returndata){
                return_rslt=JSON.parse(returndata);
                if(return_rslt['return']==0)
                {
                    alert("用户名已存在");
                    $("#edt_username").val("");
                    $("#edt_password").val("");
                    $("#edt_password_again").val("");
                }
                else
                {
                    alert("注册成功");
                    open_login();
                }
            },
            error:function(returndata){
                alert("登录失败");
                $("#edt_username").val("");
                $("#edt_password").val("");
            }
        });
    }
}

function open_login()
{
    open("../login/","_self");
}