from pickletools import pyset
import cv2
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Source image
img = cv2.imread('test.png')

# img manipulation, etc
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)


def detectChars(img):
    hImg,wImg = img.shape[:2]
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(" ")
        x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4]),
        cv2.rectangle(img,(x,hImg-y),(w,hImg-h),(0,0,255),1)
        cv2.putText(img,b[0],(x,hImg-y+10),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50,255),1)

def detectWords(img):
    hImg,wImg = img.shape[:2]
    boxes = pytesseract.image_to_data(img)
    b = boxes.splitlines()
    b = b[1:]
    string = ""
    for i in b:
        i = i.split("\t")
        if len(i)==12:
            if i[11]!="":
                x,y,w,h = int(i[6]),int(i[7]),int(i[8]),int(i[9])
                cv2.rectangle(img,(x,y),(w+x,h+y),(0,0,255),2)
                cv2.putText(img,i[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)
                string+=i[11]
                string+=" "
    print(string)
    print("\n")
                


detectWords(img)
# detectWords(imgNoNoise)

cv2.imshow("result",img)
cv2.waitKey(0)


"""
SO FAR TESTED WITH :
1) GRAYSCALE
2) NOISE FILTER (MEDIAN BLUR) - ksize value 3 & 5
3) CANNY - just doesnt work
4) OPENING - doesnt work either
5) ERODE - makes everything extremely bold and doesnt work either
6) THRESHOLD - doesnt even start, some eror

RESULTS : 
Grayscale and Noise Filter have issues with "leavening (baking soda)"
    Grayscale says "eavity takin soda"
    Noise Filter says "eavi0y set soda"

OTHER INSTANCES INCLUDE:

1) ascorbic acid [dough conditioner] : 
    G : "ascorbic acid [dough conditioner)"
    NF : "ascorbic acid [cou conditioner]"

2) salt, leavening (baking soda, sodium acid pyrophosphate), soybean oil,
    G : "salt, eavity takin soda, sodium acid —pyrophos hate soybean oll,"
    NF : "salt, eavi0y set soda, sodium acid pyrophosphate}, soybean oil,"

3) With IL2.jpg, gray detected it PERFECTLY whereas no noise only detected 2nd half (still perfectly)
    could be due to low resolution compared to IL1.png

4) With IL3.jpg, gray were very close to perfect :(
    G : ALKAL instead of ALKALI
    NF : FOUC ADI instead of FOLIC ACID
        - EMULSEFIER instead of EMULSIFIER (but got it right the 2nd time)
        - CHPS instead of CHIPS
        - COOABUTER instead of COCOA BUTTER
        - Sv LECTHN EMA SFR) VANLAL SAT instead of SOY LECITHIN [EMULSIFIER], VANILLA), SALT
            it got this (somewhat) right before too, maybe because this one was at the bottom?
        - BICARSONA' instead of BICARBONATE
"""