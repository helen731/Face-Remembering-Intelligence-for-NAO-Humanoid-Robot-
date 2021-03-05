#!/usr/bin/env python
# 
import socket
import threading
import time
import sys
import os
import struct
import cv2 
import requests  
import json
import numpy as np
import random

color = (0,0,0)
classfier=cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
classfier.load('F:\opencv\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')

def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('192.168.0.101', 10002))
        s.listen(1)
    except socket.error as msg:
        print msg
        sys.exit(1)
    print 'Waiting connection...'
    while 1:
        sc, sc_name = s.accept()
        infor = sc.recv(1024)
        length, file_name = infor.decode().split('|')
        if length and file_name:
            newfile = open('./image' + str(random.randint(1, 10000)) + '.jpg', 'wb')
            print('length {},filename {}'.format(length, file_name))
            sc.send(b'ok')
            
            file = b''
            total = int(length)
            get = 0
            while get < total:
                data = sc.recv(1024)
                file += data
                get = get + len(data)
            print('should recv{},actually receive{}'.format(length, len(file)))
            if file:
                print('acturally length:{}'.format(len(file)))
                newfile.write(file[:])
                newfile.close()

                im = cv2.imread(newfile.name)
                size = im.shape[0:2]
                image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                cv2.equalizeHist(image, image)
    
                divisor=8
                h, w = size
                minSize=(int(w/divisor), int(h/divisor))
                faceRects = classfier.detectMultiScale(image, 1.2, 2, cv2.CASCADE_SCALE_IMAGE,minSize)
    

                #show the face on image
                if len(faceRects)>0:
                    for faceRect in faceRects: 
                        x, y, w, h = faceRect
                        cv2.rectangle(image, (x, y), (x+w, y+h), color)
                    cv2.namedWindow('test',0)
                    cv2.startWindowThread()
                    cv2.imshow('test', image)
                    cv2.waitKey(6000)
                    cv2.destroyAllWindows()

                    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'  
                    files = {'image_file':open(newfile.name, 'rb')}  
                    payload = {'api_key': 'jNuf-YDxS5D87boGYwX3qTk8BmnaWq-3',  
                               'api_secret': 'IN1eOxLufvNFCk_BOwwhYVLeQlDSrrGc',  
                               'return_landmark': 0,  
                               'return_attributes':'gender,age'}  
   
                    r1 = requests.post(url,files=files,data=payload)  
                    data1=json.loads(r1.text) 
                    print r1.text 
                    face_token = data1['faces'][0]['face_token']

                    sc.send(b'detected')

                    #check if a leader
                    ifleader = sc.recv(1024)
                    if 'check' == ifleader.decode():
                        url = 'https://api-cn.faceplusplus.com/facepp/v3/search'  
                        payload = {'api_key': 'jNuf-YDxS5D87boGYwX3qTk8BmnaWq-3',  
                                   'api_secret': 'IN1eOxLufvNFCk_BOwwhYVLeQlDSrrGc',  
                                   'outer_id':'leader',  
                                   }  
                        files = {'image_file':open(newfile.name, 'rb')}  
                        r = requests.post(url,files=files,data=payload)  
                        data=json.loads(r.text)  
                        print r.text  
                        if data["results"][0]["confidence"]>=data["thresholds"]["1e-5"]:  
                            print'\n is leader'
                            sc.send(b'leader')
                        else:  
                            print '\n not leader '
                            sc.send(b'member') 
        sc.close()

if __name__ == '__main__':
    socket_service()
