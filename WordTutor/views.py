from django.shortcuts import render, HttpResponse
import json
from WordTutor.models import *  # 导入数据库操作模块
from WordTutor.tools import *

userid=-1



# Create your views here.

def firstpage(request):
    return render(request, 'login.html')


def login(request):
    if request.method == "POST":  # 判断用户请求如果是post方式
        username=request.POST.get('username', None)
        password=request.POST.get('password', None)
        print("username:" + request.POST.get('username', None))  # 接收用户表单提交的name名称对应的值
        print("password:" + request.POST.get('password', None))
        password=md5_psd(password)
        UserInfo=userinfo.objects.filter(username=username,password=password)
        num=UserInfo.count()
        rslt={}
        if num==0:
            rslt["return"]=0
        else:
            rslt["return"]=1
            UserInfo=UserInfo.values()
            UserInfo=UserInfo[0]
            global userid
            userid=UserInfo["id"]
            print("id: "+str(userid))
        print("return: "+ str(rslt["return"]))
        rslt=json.dumps(rslt)
        return HttpResponse(rslt)



def register(request):
    return render(request, 'register.html')

def register_submit(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    print("username:" + username)
    print("password:" + password)
    password = md5_psd(password)
    UserInfo = userinfo.objects.filter(username=username)
    num = UserInfo.count()
    rslt = {}
    if num!=0:  # 数据库中已存在用户
        rslt["return"]=0
    else:
        rslt["return"] = 1
        newuser={'username':username,
                 'password':password
                 }
        userinfo.objects.create(**newuser)
    rslt = json.dumps(rslt)
    return HttpResponse(rslt)

def homepage(request):
    return render(request, 'homepage.html')

def sethomepage(request):
    data = {}
    print("id: " + str(userid))
    username = "未登录"
    if userid != -1:
        # 用户名信息
        UserInfo = userinfo.objects.filter(id=userid)
        UserInfo = UserInfo.values()
        UserInfo = UserInfo[0]
        username = UserInfo["username"]
        slogan=UserInfo["slogan"]
        ifheadimg=UserInfo["ifheadimg"]
        headImgDir=None#"../static/images/user_default.jpg"
        if ifheadimg:
            headImgDir=searchFile("./WordTutor/static/images/usericon", "user_"+str(userid)+"\..*")
            headImgDir='.'+headImgDir
        if headImgDir==None:
            headImgDir="../static/images/user_default.jpg"
        # 用户单词本信息
        notelist=[]
        NoteInfo=noteinfo.objects.filter(userid=userid)
        NoteInfo=NoteInfo.values()
        noteelem={}
        for info in NoteInfo:
            print(info)
            noteelem["notename"]=info["notename"]
            noteelem["wordnum"]=info["wordnum"]
            if info["wordnum"]!=0:
                noteelem["ratio"]=info["finishnum"]/info["wordnum"]*100
            else:
                noteelem["ratio"]=0
            notelist.append(noteelem)
            noteelem={}
        # 用户单词书信息
        booklist=[]
        BookUserInfo=userbook.objects.filter(userid_id=userid)
        BookUserInfo=BookUserInfo.values()
        bookelem={}
        # print(BookUserInfo)
        for info in BookUserInfo:
            bkid=info["bookid_id"]
            print("bookid:"+str(bkid))
            BookInfo=bookinfo.objects.filter(id=bkid)
            BookInfo = BookInfo.values()
            print(BookInfo)
            BookInfo = BookInfo[0]
            bkname = BookInfo["bookname"]
            bk_wd_num=BookInfo["wordnum"]
            fnsh_num=info["finishnum"]
            bookelem["bookname"]=bkname
            bookelem["wordnum"]=bk_wd_num
            bookelem["ratio"]=fnsh_num/bk_wd_num*100
            booklist.append(bookelem)
            bookelem={}
        data["result"]=1
        data["username"] = username
        data["slogan"]=slogan
        data["Headdir"]=headImgDir
        data["notes"]=notelist
        data["book"]=booklist
    else:
        data["result"] = 0
    print("username: " + username)
    data = json.dumps(data)
    return HttpResponse(data)

def chgUserHead(request):
    User = userinfo.objects.filter(id=userid)
    myFile = request.FILES.get('headimg')  # 获取上传的文件，如果没有文件，则默认为None
    if not myFile:
        return HttpResponse('头像修改失败')
    img_root="./WordTutor/static/images/usericon"
    img_type=GetImgType(myFile.name)
    img_name="user_"+str(userid)+"."+img_type
    if not os.path.exists(img_root):
        os.makedirs(img_root)
    ifimgexist=searchFile(img_root,"user_"+str(userid)+"\..*")
    if ifimgexist!=None:
        oldname=ifimgexist[ifimgexist.find('user_'):]
        os.remove(img_root+'/'+oldname)
    destination = open(os.path.join(img_root, img_name), 'wb+')  # 打开特定的文件进行二进制的写操作
    print(myFile, type(myFile))
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    User.update(ifheadimg=True)
    print(img_root+"."+img_name)
    ChgImgSize(img_root+"/"+img_name)
    return HttpResponse("头像修改成功")

def chgUserName(request):
    username = request.POST.get('name', None)
    User = userinfo.objects.filter(id=userid)
    if username!=None:
        User.update(username=username)
        return HttpResponse("用户名修改成功")
    else:
        return HttpResponse("用户名修改失败")

def chgUserSlogan(request):
    slogan=request.POST.get('slogan', None)
    User = userinfo.objects.filter(id=userid)
    if slogan!=None:
        User.update(slogan=slogan)
        return HttpResponse("个性签名修改成功")
    else:
        return HttpResponse("个性签名修改失败")

def pop_home_book(request):
    data={}
    if userid!=-1:
        data["result"]=1
        booklist_user = []
        booklist_no_user=[]
        BookUserInfo = userbook.objects.filter(userid_id=userid)
        BookUserInfo = BookUserInfo.values()
        for info in BookUserInfo:
            bkid = info["bookid_id"]
            BookInfo = bookinfo.objects.filter(id=bkid)
            BookInfo = BookInfo.values()
            print(BookInfo)
            BookInfo = BookInfo[0]
            bkname = BookInfo["bookname"]
            booklist_user.append(bkname)
        allbook=bookinfo.objects.all()
        allbook=allbook.values()
        for info in allbook:
            bookname=info["bookname"]
            if bookname not in booklist_user:
                booklist_no_user.append(bookname)
        print(booklist_user)
        print(booklist_no_user)
        data["belong"]=booklist_user
        data["unbelong"]=booklist_no_user
    else:
        data["result"]=0
    data = json.dumps(data)
    return HttpResponse(data)

def del_book(request):
    bookname=request.POST.get('book', None)
    BookInfo = bookinfo.objects.filter(bookname=bookname)
    BookInfo = BookInfo.values()
    BookInfo = BookInfo[0]
    bookid = BookInfo["id"]
    userbook.objects.filter(userid_id=userid,bookid_id=bookid).delete()
    return HttpResponse("删除成功")

def add_book(request):
    bookname = request.POST.get('book', None)
    BookInfo = bookinfo.objects.filter(bookname=bookname)
    BookInfo = BookInfo.values()
    BookInfo = BookInfo[0]
    bookid = BookInfo["id"]
    newbook={"userid_id":userid,
             "bookid_id":bookid,
             "finishnum":0}
    userbook.objects.create(**newbook)
    return HttpResponse("添加成功")

def pop_home_note(request):
    data={}
    if userid!=-1:
        data["result"] = 1
        notelist=[]
        NoteInfo=noteinfo.objects.filter(userid=userid)
        NoteInfo=NoteInfo.values()
        for info in NoteInfo:
            notelist.append(info["notename"])
        data["note"]=notelist
    else:
        data["result"]=0
    data = json.dumps(data)
    return HttpResponse(data)

def del_note(request):
    notename=request.POST.get('note',None)
    noteinfo.objects.filter(notename=notename).delete()
    return HttpResponse("删除成功")

def add_note(request):
    notename = request.POST.get('note', None)
    NoteInfo=noteinfo.objects.filter(userid=userid, notename=notename)
    num=NoteInfo.count()
    if num!=0:
        return HttpResponse("单词本 "+notename+" 已存在")
    else:
        newnote={"userid_id":userid,
                 "notename":notename,
                 "wordnum":0,
                 "finishnum":0
                 }
        noteinfo.objects.create(**newnote)
        return HttpResponse("添加成功")

def vocabubook(request):

    return render(request, 'vocabubook.html')


def vocabunote(request):
    return render(request, 'vocabunote.html')
