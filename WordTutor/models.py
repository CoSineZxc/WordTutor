from django.db import models


# Create your models here.
class userinfo(models.Model):
    username = models.CharField("用户名", max_length=20)
    password = models.CharField("密码", max_length=50)
    ifheadimg= models.BooleanField("是否有头像",default=False)
    slogan=models.CharField("个性签名", max_length=200,default='')


    def __str__(self):  # 设置在django后台显示字段名称
        return self.username

class wordinfo(models.Model):
    spell = models.CharField("拼写", max_length=30)
    mean = models.CharField("含义", max_length=100)

    def __str__(self):  # 设置在django后台显示字段名称
        return self.spell

class bookinfo(models.Model):
    bookname = models.CharField("单词书名", max_length=30)
    wordnum = models.IntegerField("单词数量")
    user=models.ManyToManyField(userinfo,through='userbook')
    word=models.ManyToManyField(wordinfo)

    def __str__(self):  # 设置在django后台显示字段名称
        return self.bookname


class noteinfo(models.Model):
    userid = models.ForeignKey('userinfo',on_delete=models.CASCADE)
    notename = models.CharField("单词本名", max_length=30)
    wordnum = models.IntegerField("单词数量")
    finishnum = models.IntegerField("完成数量")
    word=models.ManyToManyField(wordinfo)

    def __str__(self):  # 设置在django后台显示字段名称
        return self.notename

class userbook(models.Model):
    userid = models.ForeignKey(userinfo,on_delete=models.CASCADE)
    bookid = models.ForeignKey(bookinfo,on_delete=models.CASCADE)
    finishnum = models.IntegerField("用户完成数量")
