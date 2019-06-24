from django.shortcuts import render, HttpResponse
from django.db.models import Q
import json
import random
from WordTutor.models import *  # 导入数据库操作模块
from WordTutor.tools import *


# Create your views here.

def firstpage(request):
    return render(request, 'login.html')


def login(request):
    if request.method == "POST":  # 判断用户请求如果是post方式
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print("username:" + request.POST.get('username', None))  # 接收用户表单提交的name名称对应的值
        print("password:" + request.POST.get('password', None))
        password = md5_psd(password)
        UserInfo = userinfo.objects.filter(username=username, password=password)
        num = UserInfo.count()
        rslt = {}
        if num == 0:
            rslt["return"] = 0
        else:
            UserInfo = UserInfo.values()
            UserInfo = UserInfo[0]
            userid = UserInfo["id"]
            rslt["userid"] = userid
            rslt["return"] = 1
        print("登录情况: " + str(rslt["return"]))
        rslt = json.dumps(rslt)
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
    if num != 0:  # 数据库中已存在用户
        rslt["return"] = 0
    else:
        rslt["return"] = 1
        newuser = {'username': username,
                   'password': password
                   }
        userinfo.objects.create(**newuser)
    rslt = json.dumps(rslt)
    return HttpResponse(rslt)


def homepage(request):
    return render(request, 'homepage.html')


def sethomepage(request):
    userid = request.POST.get('userid', None)
    data = {}
    if userid != None:
        # 用户名信息
        UserInfo = userinfo.objects.filter(id=userid)
        UserInfo = UserInfo.values()
        UserInfo = UserInfo[0]
        slogan = UserInfo["slogan"]
        ifheadimg = UserInfo["ifheadimg"]
        username = UserInfo["username"]
        headImgDir = None  # "../static/images/user_default.jpg"
        if ifheadimg:
            headImgDir = searchFile("./WordTutor/static/images/usericon", "user_" + str(userid) + "\..*")
            headImgDir = headImgDir[1:]
        if headImgDir == None:
            headImgDir = "/static/images/user_default.jpg"
        # 用户单词本信息
        notelist = []
        NoteInfo = noteinfo.objects.filter(userid=userid)
        NoteInfo = NoteInfo.values()
        noteelem = {}
        for info in NoteInfo:
            noteelem["notename"] = info["notename"]
            noteelem["wordnum"] = info["wordnum"]
            if info["wordnum"] != 0:
                noteelem["ratio"] = info["finishnum"] / info["wordnum"] * 100
            else:
                noteelem["ratio"] = 0
            notelist.append(noteelem)
            noteelem = {}
        # 用户单词书信息
        booklist = []
        BookUserInfo = userbook.objects.filter(userid_id=userid)
        BookUserInfo = BookUserInfo.values()
        bookelem = {}
        for info in BookUserInfo:
            bkid = info["bookid_id"]
            BookInfo = bookinfo.objects.filter(id=bkid)
            BookInfo = BookInfo.values()
            BookInfo = BookInfo[0]
            bkname = BookInfo["bookname"]
            bk_wd_num = BookInfo["wordnum"]
            fnsh_num = info["finishnum"]
            bookelem["bookname"] = bkname
            bookelem["wordnum"] = bk_wd_num
            bookelem["ratio"] = fnsh_num / bk_wd_num * 100
            booklist.append(bookelem)
            bookelem = {}
        data["result"] = 1
        data["username"] = username
        data["slogan"] = slogan
        data["Headdir"] = headImgDir
        data["notes"] = notelist
        data["book"] = booklist
    else:
        data["result"] = 0
    data = json.dumps(data)
    return HttpResponse(data)


def chgUserHead(request):
    userid = request.POST.get('userid', None)
    User = userinfo.objects.filter(id=userid)
    myFile = request.FILES.get('headimg')  # 获取上传的文件，如果没有文件，则默认为None
    if not myFile:
        return HttpResponse('头像修改失败')
    img_root = "./WordTutor/static/images/usericon"
    img_type = GetImgType(myFile.name)
    img_name = "user_" + str(userid) + "." + img_type
    if not os.path.exists(img_root):
        os.makedirs(img_root)
    ifimgexist = searchFile(img_root, "user_" + str(userid) + "\..*")
    if ifimgexist != None:
        oldname = ifimgexist[ifimgexist.find('user_'):]
        os.remove(img_root + '/' + oldname)
    destination = open(os.path.join(img_root, img_name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    User.update(ifheadimg=True)
    ChgImgSize(img_root + "/" + img_name)
    return HttpResponse("头像修改成功")


def chgUserName(request):
    newusername = request.POST.get('newname', None)
    oldusername = request.POST.get('oldname', None)
    User = userinfo.objects.filter(username=oldusername)
    if newusername != None:
        User.update(username=newusername)
        return HttpResponse("用户名修改成功")
    else:
        return HttpResponse("用户名修改失败")


def chgUserSlogan(request):
    slogan = request.POST.get('slogan', None)
    username = request.POST.get('username', None)
    User = userinfo.objects.filter(username=username)
    if slogan != None:
        User.update(slogan=slogan)
        return HttpResponse("个性签名修改成功")
    else:
        return HttpResponse("个性签名修改失败")


def pop_home_book(request):
    userid = request.POST.get('userid', None)
    data = {}
    if userid != None:
        data["result"] = 1
        booklist_user = []
        booklist_no_user = []
        BookUserInfo = userbook.objects.filter(userid_id=userid)
        BookUserInfo = BookUserInfo.values()
        for info in BookUserInfo:
            bkid = info["bookid_id"]
            BookInfo = bookinfo.objects.filter(id=bkid)
            BookInfo = BookInfo.values()
            BookInfo = BookInfo[0]
            bkname = BookInfo["bookname"]
            booklist_user.append(bkname)
        allbook = bookinfo.objects.all()
        allbook = allbook.values()
        for info in allbook:
            bookname = info["bookname"]
            if bookname not in booklist_user:
                booklist_no_user.append(bookname)
        data["belong"] = booklist_user
        data["unbelong"] = booklist_no_user
    else:
        data["result"] = 0
    data = json.dumps(data)
    return HttpResponse(data)


def del_book(request):
    bookname = request.POST.get('book', None)
    userid = request.POST.get('userid', None)
    BookInfo = bookinfo.objects.filter(bookname=bookname)
    BookInfo = BookInfo.values()
    BookInfo = BookInfo[0]
    bookid = BookInfo["id"]
    userbook.objects.filter(userid_id=userid, bookid_id=bookid).delete()
    return HttpResponse("删除成功")


def add_book(request):
    bookname = request.POST.get('book', None)
    userid = request.POST.get('userid', None)
    BookInfo = bookinfo.objects.filter(bookname=bookname)
    BookInfo = BookInfo.values()
    BookInfo = BookInfo[0]
    bookid = BookInfo["id"]
    newbook = {"userid_id": userid,
               "bookid_id": bookid,
               "finishnum": 0}
    userbook.objects.create(**newbook)
    return HttpResponse("添加成功")


def pop_home_note(request):
    userid = request.POST.get('userid', None)
    data = {}
    if userid != None:
        data["result"] = 1
        notelist = []
        NoteInfo = noteinfo.objects.filter(userid=userid)
        NoteInfo = NoteInfo.values()
        for info in NoteInfo:
            notelist.append(info["notename"])
        data["note"] = notelist
    else:
        data["result"] = 0
    data = json.dumps(data)
    return HttpResponse(data)


def del_note(request):
    notename = request.POST.get('note', None)
    noteinfo.objects.filter(notename=notename).delete()
    return HttpResponse("删除成功")


def add_note(request):
    notename = request.POST.get('note', None)
    userid = request.POST.get('userid', None)
    firstword = request.POST.get('firstword', None)
    NoteInfo = noteinfo.objects.filter(userid=userid, notename=notename)
    num = NoteInfo.count()
    if num != 0:
        return HttpResponse("单词本 " + notename + " 已存在")
    else:
        if firstword == None:
            newnote = {"userid_id": userid,
                       "notename": notename,
                       "wordnum": 0,
                       "finishnum": 0
                       }
            noteinfo.objects.create(**newnote)
        else:
            newnote = {"userid_id": userid,
                       "notename": notename,
                       "wordnum": 1,
                       "finishnum": 0
                       }
            noteinfo.objects.create(**newnote)
            Note=noteinfo.objects.filter(userid_id=userid,notename=notename).first()
            word=wordinfo.objects.filter(spell=firstword)
            Note.word.add(*word)
        return HttpResponse("添加成功")


def vocabubook(request, userid, book=None):
    '''
    + 当前选择的单词本（含缺省）V
    + 完成度(?) V
    + 当前单词及相关信息 V
    + 用户全部单词书 V
    + 本书全部单词 V
    :param request:
    :param userid:
    :param book:
    :return:
    '''
    booklist = []
    bookNowName = book
    bookNowId = -1
    bookNowFinish = 0
    word_list = []
    wordNowSpell = None
    wordNowMean = None
    SelectMeanList = []
    UserBook = userbook.objects.filter(userid_id=userid)
    UserBook = UserBook.values()
    for i, info in enumerate(UserBook):
        bkid = info["bookid_id"]
        BookInfo = bookinfo.objects.filter(id=bkid)
        BookInfo = BookInfo.values()
        BookInfo = BookInfo[0]
        bkname = BookInfo["bookname"]
        booklist.append(bkname)
        if i == 0 and book == None:
            bookNowName = bkname
        if bkname == bookNowName:
            bookNowId = BookInfo["id"]
            bookNowFinish = info["finishnum"] / BookInfo["wordnum"] * 100
    book_obj = bookinfo.objects.get(bookname=bookNowName)
    word_obj = book_obj.word.all().values("spell")
    wrongnumlist = CreateRand(len(word_obj), 0)
    wrongmeanlist = []
    for i, wd in enumerate(word_obj):
        if i in wrongnumlist:
            wrongmean = wordinfo.objects.filter(spell=wd["spell"]).values()[0]["mean"]
            wrongmeanlist.append(wrongmean)
        word_list.append(wd["spell"])
    len_word_list = len(word_list)
    wordNowSpell = word_list[0]
    WordInfo = wordinfo.objects.filter(spell=wordNowSpell)
    WordInfo = WordInfo.values()
    WordInfo = WordInfo[0]
    wordNowMean = WordInfo["mean"]
    rightloc = random.randint(0, 2)
    if rightloc == 0:
        SelectMeanList.append(wordNowMean)
        SelectMeanList.append(wrongmeanlist[0])
        SelectMeanList.append(wrongmeanlist[1])
    elif rightloc == 1:
        SelectMeanList.append(wrongmeanlist[0])
        SelectMeanList.append(wordNowMean)
        SelectMeanList.append(wrongmeanlist[1])
    else:
        SelectMeanList.append(wrongmeanlist[0])
        SelectMeanList.append(wrongmeanlist[1])
        SelectMeanList.append(wordNowMean)
    return render(request, 'vocabubook.html', locals())

def AddWord2Note(request):
    userid = request.POST.get('userid', None)
    notename = request.POST.get('notename', None)
    addword = request.POST.get('addword', None)
    Note=noteinfo.objects.filter(userid_id=userid,notename=notename)
    NoteFirst=Note.first()
    word=wordinfo.objects.filter(spell=addword)
    NoteFirst.word.add(*word)
    wordnum=NoteFirst.word.count()
    Note.update(wordnum=wordnum)
    return HttpResponse("添加成功")

def vocabunote(request, userid, note=None):
    '''
    + 当前选择的单词本（含缺省）
    + 当前单词及相关信息
    + 用户全部单词本
    + 本单词本全部单词
    :param request:
    :param userid:
    :param note:
    :return:
    '''
    notelist = []
    noteNowName = note
    noteNowId = -1
    word_list = []
    wordNowSpell = None
    wordNowMean = None
    SelectMeanList = []
    UserNote = noteinfo.objects.filter(userid_id=userid)
    UserNote = UserNote.values()
    for i,info in enumerate(UserNote):
        ntname=info["notename"]
        ntwdnum=info["wordnum"]
        if ntwdnum!=0:
            notelist.append(ntname)
        if i==0and note==None:
            noteNowName=ntname
        if ntname==noteNowName:
            noteNowId=info["id"]
    note_obj=noteinfo.objects.get(notename=noteNowName)
    word_obj=note_obj.word.all().values("spell")
    wrongnumlist = CreateRand(len(word_obj), 0)
    wrongmeanlist = []
    for i, wd in enumerate(word_obj):
        if i in wrongnumlist:
            wrongmean = wordinfo.objects.filter(spell=wd["spell"]).values()[0]["mean"]
            wrongmeanlist.append(wrongmean)
        word_list.append(wd["spell"])
    len_word_list = len(word_list)
    wordNowSpell = word_list[0]
    WordInfo = wordinfo.objects.filter(spell=wordNowSpell)
    WordInfo = WordInfo.values()
    WordInfo = WordInfo[0]
    wordNowMean = WordInfo["mean"]
    rightloc = random.randint(0, 2)
    if rightloc == 0:
        SelectMeanList.append(wordNowMean)
        SelectMeanList.append(wrongmeanlist[0])
        SelectMeanList.append(wrongmeanlist[1])
    elif rightloc == 1:
        SelectMeanList.append(wrongmeanlist[0])
        SelectMeanList.append(wordNowMean)
        SelectMeanList.append(wrongmeanlist[1])
    else:
        SelectMeanList.append(wrongmeanlist[0])
        SelectMeanList.append(wrongmeanlist[1])
        SelectMeanList.append(wordNowMean)
    return render(request, 'vocabunote.html',locals())

def ChgNewWord(request):
    data={}
    newword = request.POST.get('newword', None)
    true_mean=None
    Select_answer=[]
    WordInfo=wordinfo.objects.filter(spell=newword)
    true_mean=WordInfo.values()[0]["mean"]
    AllWordInfo = wordinfo.objects.filter(~Q(spell=newword))
    allnum=AllWordInfo.count()
    allindex=CreateRand(allnum,0)
    rightloc = random.randint(0, 2)
    if rightloc==0:
        Select_answer.append(true_mean)
        Select_answer.append(AllWordInfo.values()[0]["mean"])
        Select_answer.append(AllWordInfo.values()[1]["mean"])
    elif rightloc==1:
        Select_answer.append(AllWordInfo.values()[0]["mean"])
        Select_answer.append(true_mean)
        Select_answer.append(AllWordInfo.values()[1]["mean"])
    else:
        Select_answer.append(AllWordInfo.values()[0]["mean"])
        Select_answer.append(AllWordInfo.values()[1]["mean"])
        Select_answer.append(true_mean)
    data["true_mean"]=true_mean
    data["Select_answer"]=Select_answer
    data = json.dumps(data)
    return HttpResponse(data)

def DelWordNote(request):
    userid = request.POST.get('userid', None)
    notename=request.POST.get('notename', None)
    delword=request.POST.get('delword', None)
    Note_info=noteinfo.objects.filter(userid_id=userid,notename=notename)
    word=wordinfo.objects.filter(spell=delword)
    NoteFirst=Note_info.first()
    NoteFirst.word.remove(*word)
    wordnum = NoteFirst.word.count()
    Note_info.update(wordnum=wordnum)
    return HttpResponse("删除成功")
