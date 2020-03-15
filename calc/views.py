from django.shortcuts import render
from django.http import HttpResponse
import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from collections import OrderedDict
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
import json
import tkinter
import tkinter.messagebox
import os,os.path

# Create your views here.
def login(request):
    return render(request,'login.html')
def home(request):
    username=request.POST['username']
    password=request.POST['password']
    if(username=='username' and password=='password'):
        return render(request,'home.html')
    else:
        return render(request,'login.html')
    

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def dataset_creator(request):
    
    Id=request.POST['id']
    name=request.POST['name']
    dept=request.POST['DEPT']
    sem=request.POST['SEM']
    fileName='StudentDetails/'+dept+'/'+sem+'/'+'StudentDetails.csv'
    file1=pd.read_csv(fileName)
    ID=[]
    f=open(fileName,'rU')
    for line in f:
        cells=line.split(",")
        ID.append(cells[0])
    f.close()
    
    
    
            
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
            #incrementing sample number 
                sampleNum=sampleNum+1
            #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage/"+dept+"/"+sem+"/"+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
        #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
        # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        
        with open('StudentDetails/'+dept+'/'+sem+'/'+'StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
    
            

    return render(request,'home.html',{'id':Id,'name':name})

def trainer():
    dept=request.POST['DEPT']
    sem=request.POST['SEM']
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage/"+dept+"/"+sem)
    recognizer.train(faces, np.array(Id))
    recognizer.save("trainer/"+dept+"/"+sem+"/"+"Trainner.yml")
    res = "Image Trained"
def getImagesAndLabels(path):
    
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    
    faces=[]
    
    Ids=[]
    for imagePath in imagePaths:
        pilImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage,'uint8')
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids


def detector(request):
    dept=request.POST['DEPT']
    sem=request.POST['SEM']

    def trainer():
        recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector =cv2.CascadeClassifier(harcascadePath)
        faces,Id = getImagesAndLabels("TrainingImage/"+dept+"/"+sem)
        recognizer.train(faces, np.array(Id))
        recognizer.save("trainer/"+dept+"/"+sem+"/"+"Trainner.yml")
        res = "Image Trained"
        
    
    trainer()  
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("trainer/"+dept+"/"+sem+"/"+"Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails/"+dept+"/"+sem+"/"+"StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)   
    
    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])  
                                            
            if(conf <68):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                
                tt=str(Id)+"-"+str(aa)
                attendance.loc[len(attendance)] = [Id,str(aa[0]),date,timeStamp]

                
                
                
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            
            if(conf > 40):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)  
             
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')
        
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break   
        
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance/"+dept+"/"+sem+"/"+"Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    file1=pd.read_csv(fileName)
    ID1=[]
    name1=[]
    f=open(fileName,'rU')
    for line in f:
        cells=line.split(",")
        ID1.append(cells[0])
        name1.append(cells[1])
    f.close()
    fileName1='StudentDetails/'+dept+'/'+sem+'/'+'StudentDetails.csv'
    a=pd.read_csv(fileName1)
    ID2=[]
    f1=open(fileName1,'rU')
    for line1 in f1:
        cells1=line1.split(",")
        ID2.append(cells1[0])
    f1.close()

    print(len(ID2))
    cam.release()
    cv2.destroyAllWindows()
    #print(attendance)
    res=attendance
    total=len(name1)-1
    DIR= "Attendance/"+dept+"/"+sem+"/"
    len1= len([length for length in os.listdir(DIR) if os.path.isfile(os.path.join(DIR,length))])
    total1=int((len(ID2)-1)/2)
    absenties=total1-total
    
    
    return render(request,'result2.html',{'name':name1,'id':ID1,'total':total,'length':len1,'totalstudents':total1,'absenties':absenties,'dept':dept,'sem':sem})

def individual(request):
    import glob
    import pandas as pd
    id=request.POST['ID']
    dept=request.POST['DEPT']
    sem=request.POST['SEM']
    DIR= "Attendance/"+dept+"/"+sem+"/"
    len1= len([length for length in os.listdir(DIR) if os.path.isfile(os.path.join(DIR,length))])
    

    a=[]
    a.append(glob.glob("Attendance/ISE/8/*.csv"))
    list=[]
    list1=[]
    count=0
    print(len(a[0]))
    df=pd.read_csv("StudentDetails/"+dept+"/"+sem+"/"+"StudentDetails.csv")
    for i in range(len(a[0])): 		
        list.append(str(a[0][i]))
    for j in range(0,len(list)):
        a=pd.read_csv(list[j])
        f=open(list[j],'rU')
        for line in f:
            cells=line.split(",")
            list1.append(cells[0])
    
    print(list1)
    aa=df.loc[df['Id'] == int(id)]['Name'].values

    
    for k in range(0,len(list1)):
        if(list1[k]==id):
            count+=1
    
    
    print("the student with  id: "+str(id)+" is present for "+str(count)+" classes ")
    
    absent=len1-count
    return render(request,'individual.html',{'attended':count,'Overall':len1,'id':id,'absent':absent,'dept':dept,'sem':sem,'name':str(aa[0])})

def signup(request):
    return render(request,'register.html')

def register(request):
    Name=request.POST['name']
    Username=request.POST['username']
    Password=request.POST['password']
    row = [Name , Username, Password]
    with open('register/register.csv','a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    return render(request,'login.html')

    
    
    