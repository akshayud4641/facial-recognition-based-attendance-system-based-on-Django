import cv2
import numpy as np



faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0);
rec=cv2.face.LBPHFaceRecognizer_create();
rec.read('trainingData.yml')
id=0
count=0
font=cv2.FONT_HERSHEY_COMPLEX_SMALL
while(True):
    count+=1
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        if conf < 85:
            cv2.putText(img,str(id),(x,y+h),font,5,255,2);
            print("The detected face's Id's are:\n"+str(id))
            
        else:
            cv2.putText(img,"unknown",(x,y+h),font,1,255);
            print("New face found ")
            inp=str(input("yes/no to save the face"))
            if (inp=='yes'):
                import dataset_creator
                import trainer
                import detector
    if cv2.waitKey(1)==13 or count==1:
        break
cam.release()
cv2.destroyAllWindows()
