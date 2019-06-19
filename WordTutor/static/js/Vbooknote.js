function initial_vbooknavbar(book)
{
    var username=$.cookie("username");
    var img_dir=$.cookie("img_dir");
    $("#txt_username").text(username);
    document.getElementById("img_icon").src = img_dir;
    //$("#img_icon").src=img_dir;
}