from django.test import TestCase
import hashlib

if __name__=="__main__":

    # Create your tests here.
    def md5_psd(password):
        m = hashlib.md5()
        m.update(password.encode("utf-8"))
        return m.hexdigest()


    # print(md5_psd("123456"))

    import os, os.path, re


    def searchFile(pathname, filename):  # 参数1要搜索的路径，参数2要搜索的文件名，可以是正则表代式
        matchedFile = []
        for root, dirs, files in os.walk(pathname):
            for file in files:
                if re.match(filename, file):
                    fname = os.path.abspath(os.path.join(root, file))
                    # print(fname)
                    matchedFile.append(fname)
        return matchedFile

    # a=searchFile("./static/images/usericon","user_1\..*")
    # print(a)

    from PIL import Image

    def ChgImgSize(ImgDir):
        im = Image.open(ImgDir)
        (x, y) = im.size  # read image size
        if x!=100 or y!=100:
            x = 100
            y = 100
        out = im.resize((x, y), Image.ANTIALIAS)  # resize image with high-quality
        out.save(ImgDir, quality = 95)

    # a=searchFile("./static/images/usericon","user_"+str(1)+"..*")
    #
    # ChgImgSize(a[0])

    def GetImgType(imgname):
        imgname=imgname.split('.')
        imgname=imgname[-1]
        return imgname

    a=GetImgType("124.jpg")
    print(a)
