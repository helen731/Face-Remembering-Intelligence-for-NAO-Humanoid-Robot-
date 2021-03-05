import argparse
import naoqi
from naoqi import ALProxy
import socket
import sys      # sys.exit() 
#import almath   # 
import thread   # 
import time     # 

robotIP = "172.20.10.7"
robotPORT = 9559

address = ('172.20.10.2', 10002)
photoCaptureProxy = ALProxy("ALPhotoCapture", robotIP, robotPORT)
tts=ALProxy("ALTextToSpeech", robotIP, robotPORT)
photoCaptureProxy.setResolution(2)
photoCaptureProxy.setPictureFormat("jpg")
asr = ALProxy("ALSpeechRecognition", robotIP, robotPORT)
memProxy = ALProxy("ALMemory","172.20.10.7",robotPORT)


def takephoto(): 
        print(' Please put your face in front of me!')
        tts.say(' Please put your face in front of me!')
        time.sleep(3)
        photo = photoCaptureProxy.takePicture("/home/nao/", "testMember")
        print('Ready to send{}'.format(photo))
        send(photo)
        
        

def send(photo):   
    #for photo in photos[0]:
        
        print('sending {}'.format(photo))
        data = file_deal(photo)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('172.20.10.2', 10002))
        except socket.error as msg:
            print msg
            sys.exit(1)
        sock.send('{}|{}'.format(len(data), file).encode())
        reply = sock.recv(1024)
        if 'ok' == reply.decode():
            go = 0
            total = len(data)
            while go < total:
                data_to_send = data[go:go + 1024]
                sock.send(data_to_send)
                go += len(data_to_send)
            reply = sock.recv(1024)
            if 'detected' == reply.decode():
                print('{} send successfully'.format(photo))
                sock.send(b'check')
                ifleader = sock.recv(1024)
                if ifleader == 'leader':
                    setTime()
                elif ifleader == 'member':
                    print('You are not allowed to set time.')
                    tts.say('You are not leader, and not allowed to set time.')
                    tts.say('Please ask the leader to set time.')
            else:
                tts.say('no face, try again')
                print('No face, try again')
                takephoto()
                
        sock.close()
     


def setTime():
   
    asr.setLanguage("English")
    vocabulary = ["one","five","ten","fifteen","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
    asr.setVocabulary(vocabulary, False)
    print 'Speech recognition engine started'
    while True:
            tts.say('Hello leader! How many minutes do you need for the meeting? Please tell me the number.')
            tts.say('Only multiples of ten that below ninety or multiples of ten that below twenty is allowed.')
            asr.subscribe("Test_ASR")
            time.sleep(10)
            val = memProxy.getData("WordRecognized")
            if (val[0] == "one" and val[1]>= 0.4):
                print('one')
                tts.say('Time start')
                print('Time start')
                time.sleep(60)
                tts.say('time out')
                print('Time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "five" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(300)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "ten" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(600)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "fifteen" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(900)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "twenty" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(1200)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "thirty" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(1800)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "forty" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(2400)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "fifty" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(3000)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "sixty" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(3600)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "seventy" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(4200)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "eighty" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(4800)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            elif (val[0] == "ninety" and val[1]>= 0.4):
                tts.say('Time start')
                time.sleep(5400)
                tts.say('time out')
                asr.unsubscribe("Test_ASR")
                break
            else:
                tts.say('Try again')
                print('Try again')
                asr.unsubscribe("Test_ASR")
    tts.say('If you need another slot of time, please say leader to me, or say finish to me')
    


def file_deal(file_path):
    mes = b''
    try:
        file = open("testMember.jpg",'rb')
        mes = file.read()
    except:
        print('error{}'.format(file_path))
    else:
        file.close()
        return mes

if __name__ == '__main__':
    print 'Speech recognition engine started'
    tts.say('Hi, welcome to the set time mode. If you are a leader, please say word leader to me. Only leader can set time.')
    print('Hi, welcome to the set time mode.')
    print('If you are a leader, please say word leader to me. Only leader can set time.')
    while True:
        asr.setLanguage("English")
        vocabulary = ["leader","finish"]
        asr.setVocabulary(vocabulary, False)
        asr.subscribe("Test_ASR")
        time.sleep(10)
        #try:
        val = memProxy.getData("WordRecognized")
        if (val[0] == "leader" and val[1]>= 0.4):
            print('leader')
            asr.unsubscribe("Test_ASR")
            takephoto()
        elif (val[0] == "finish" and val[1] >= 0.4):
            print('finish')
            asr.unsubscribe("Test_ASR")
            sys.exit()
        else:
            tts.say('Try again')
            print('Try again')
            asr.unsubscribe("Test_ASR")
   