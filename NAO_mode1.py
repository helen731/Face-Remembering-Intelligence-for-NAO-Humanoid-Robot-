import argparse
import naoqi
from naoqi import ALProxy
import socket
import sys      # sys.exit() 
#import almath   # 
import thread   # 
import time     # 

robotIP = "172.20.10.7"
robotPORT = "9559"

address = ('172.20.10.2', 10002)
photoCaptureProxy = ALProxy("ALPhotoCapture", "172.20.10.7", 9559)
tts=ALProxy("ALTextToSpeech","172.20.10.7", 9559)
photoCaptureProxy.setResolution(2)
photoCaptureProxy.setPictureFormat("jpg")
asr = ALProxy("ALSpeechRecognition", "172.20.10.7", 9559)
memProxy = ALProxy("ALMemory","172.20.10.7",9559)
next = 'no'

def takephoto(): 
    global next
    #while True:
    tts.say('Hi, welcome to the acquaintance mode! Please put your face in front of me.')
    print('Hi, welcome to the acquaintance mode! Please put your face in front of me.')
    time.sleep(3)
    photo = photoCaptureProxy.takePicture("/home/nao/", "member")
    print('Ready to send{}'.format(photo))
    send(photo)
    
def send(photo):   
    #for photo in photos[0]:
        global next
        next = 'no'
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
                global ifleader
                ifleader = ifleaderMethod()
                if ifleader == 'yes':
                    sock.send(b'leader')
                elif ifleader == 'no':
                    sock.send(b'member')
                success = sock.recv(1024)
                if 'no' != success:
                    tts.say('You are added to the group.')
                    print('You are added to the group.')
            else:
                tts.say('no face, try again')
                print('No face, try again')
                takephoto()
                
        sock.close()
        #next = 'yes'


def ifleaderMethod():
    global isleader
    isleader = 'notvalid'
    tts.say('Are you a leader?')
    print('Are you a leader?')
    asr.setLanguage("English")
    vocabulary = ["yes","no"]
    asr.setVocabulary(vocabulary, False)
    print 'Speech recognition engine started'
    while True:
        #try:
            asr.subscribe("Test_ASR")
            time.sleep(10)
            val = memProxy.getData("WordRecognized")
            print(val[0])
            if (val[0] == "yes" and val[1]>= 0.4):
                isleader = 'yes'
                asr.unsubscribe("Test_ASR")
                print('Yes')
                break
            elif (val[0] == "no" and val[1]>= 0.4):
                isleader = 'no'
                asr.unsubscribe("Test_ASR")
                print('No')
                break
            else:
                tts.say('Try again')
                asr.unsubscribe("Test_ASR")
    return isleader

def file_deal(file_path):
    mes = b''
    try:
        file = open("member.jpg",'rb')
        mes = file.read()
    except:
        print('error{}'.format(file_path))
    else:
        file.close()
        return mes

if __name__ == '__main__':
    print 'Speech recognition engine started'
    tts.say('Hi, this is meeting assistant. You can say start, next or finish to me!')
    print('Hi, this is meeting assistant.')
    print('You can say start, next or finish to me!')
    while True:
        
        asr.setLanguage("English")
        vocabulary = ["start","finish","next"]
        asr.setVocabulary(vocabulary, False)
        asr.subscribe("Test_ASR")
        time.sleep(5)
        #try:
        val = memProxy.getData("WordRecognized")
        if (val[0] == "start" and val[1]>= 0.4):
            print('Start')
            asr.unsubscribe("Test_ASR")
            takephoto()
               
        elif (val[0] == "finish" and val[1]>= 0.4):
            print('Finish')
            asr.unsubscribe("Test_ASR")
            sys.exit()
        elif (val[0] == "next" and val[1]>= 0.4):
            print('Next')
            asr.unsubscribe("Test_ASR")
            takephoto() 
                
        else:
            tts.say('Try again')
            print('Try again')
            asr.unsubscribe("Test_ASR")
        #except:
            #print("error speech recognition")