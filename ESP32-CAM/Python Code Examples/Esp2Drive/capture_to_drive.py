import cv2
import urllib.request
import numpy as np
import time
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

url="http://192.168.5.25/cam-hi.jpg"
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
 
count=0
 
 
gauth = GoogleAuth()
gauth.LocalWebserverAuth()       
drive = GoogleDrive(gauth)
folder = "1T_ERl2luPeeVyt48L8yZDSgngw76-jyn"
 
while True:
    img_resp=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
    frame=cv2.imdecode(imgnp,-1)
    
    cv2.imshow("live transmission", frame)
 
    key=cv2.waitKey(5)
    
    if key==ord('k'):
        count+=1
        t=str(count)+'.png'
        cv2.imwrite(t,frame)
        print("image saved as: "+t)
        f= drive.CreateFile({'parents':[{'id':folder}],'title':t})
        f.SetContentFile('1.png')
        f.Upload()
        print("image uploaded as: "+t)
        
    if key==ord('q'):
        break
    else:
        continue
 
cv2.destroyAllWindows()