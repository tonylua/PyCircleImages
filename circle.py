import os
import re
import sys
from PIL import Image, ImageFilter, ImageDraw, ImageOps

def make_circle(path, maxS = 220):
    origImg = Image.open(path)
    bgBlur = ImageFilter.GaussianBlur(radius=6.18)
    
    if origImg.mode in ("RGBA", "P"):
        origImg = origImg.convert('RGB')
    
    h,w = origImg.size
    maxSize = max(h, w)
    bgSize = (maxSize, maxSize)
    imgPosi = (int((maxSize - h) / 2), int((maxSize - w) / 2))
    
    img = origImg.copy()
    img = img.resize(bgSize)
    img = img.filter(bgBlur)
    img.paste(origImg, imgPosi)
    
    mask = Image.new('L', bgSize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bgSize, fill=255)
    
    img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    img.putalpha(mask)

    if maxSize > maxS:
        img = img.resize((maxS, maxS))
    
    return img

if (len(sys.argv) > 1 and re.search(r'^--file=', sys.argv[1])):
    d = sys.argv[1][7:]
    d = d.split(',')
else:
    d = os.listdir(r"./gods/")
    d = map(lambda path: 'gods/' + path, d)

for file_name in d:
    if (re.search(r'\.(png|jpg|jpeg)$', file_name, re.I)):
        file_name = re.sub(r'^./', '', file_name)
        img = make_circle('./' + file_name)
        save_name = re.sub(r'gods/', '', file_name)
        save_name = re.sub(r'(jpg|jpeg)$', 'png', save_name.lower())
        if not os.path.exists('./circle_versions/'):
            os.mkdir('./circle_versions/')
        img.save('./circle_versions/' + save_name)
        print(save_name + '...saved!')
#  img = make_circle('./mnemosyne.jpg')
#  img.show()
