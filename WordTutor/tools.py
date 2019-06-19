import hashlib
from PIL import Image
import os, os.path, re
import random



def md5_psd(password):
    m = hashlib.md5()
    m.update(password.encode("utf-8"))
    return m.hexdigest()

def searchFile(pathname, filename):  # 参数1要搜索的路径，参数2要搜索的文件名，可以是正则表代式
    fname=None
    for root, dirs, files in os.walk(pathname):
        for file in files:
            if re.match(filename, file):
                fname = os.path.abspath(os.path.join(root, file))
                fname=fname.replace("\\",'/')
                start=fname.find("/static")
                fname='.'+fname[start:]
    return fname

def ChgImgSize(ImgDir):
    im = Image.open(ImgDir)
    (x, y) = im.size  # read image size
    if x!=100 or y!=100:
        x = 100
        y = 100
    out = im.resize((x, y), Image.ANTIALIAS)  # resize image with high-quality
    out.save(ImgDir, quality = 95)

def GetImgType(imgname):
    imgname=imgname.split('.')
    imgname=imgname[-1]
    return imgname

def CreateRand(allnum,locnow):
    rslt=[]
    while len(rslt)<2:
        a=random.randint(0, allnum-1)
        if a not in rslt and a!=locnow:
            rslt.append(a)
    return rslt

if __name__=="__main__":
    # a = searchFile("./static/images/usericon", "user_"+str(1)+"\..*")

    # ChgImgSize(a)
    a=CreateRand(20,2)
    print(a)