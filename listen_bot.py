import time, datetime
import telepot
import RPi.GPIO as GPIO
import requests
import os
import glob
from telepot.loop import MessageLoop
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


now = datetime.datetime.now()

red = 13
green = 6
cnt = 0
pin = 18 # PWM pin num 18





GPIO.setup(pin, GPIO.OUT)






GPIO.setup(red, GPIO.OUT)
GPIO.output(red, 0) #Off initially
#LED green
GPIO.setup(green, GPIO.OUT)
GPIO.output(green, 0) #Off initially



def webcontrol(chat_id, type, cmd):
    req = 'http://localhost:8080/0/'+type+'/'+cmd
    res = requests.get(req)
    bot.sendMessage(chat_id, res.text)





def handle(msg):
    p= GPIO.PWM(pin,50)
    p.start(0)
    chat_id = msg['chat']['id']
    command = msg['text']
    #should work thanks to Winston
    if msg['from']['id'] != your id:
        bot.sendMessage(chat_id, "Sorry this is a personal bot. Access Denied!")
        exit(1)

    print ('Received: %s' % command)

    if 'Open' in command:
        message = "Door "
        if 'door' in command:
            message = message + "unlocked "
            GPIO.output(green, 1)
            p.ChangeDutyCycle(2)
            GPIO.output(red, 0)
            print ("door unlocked")
        message = message
        bot.sendMessage (chat_id, message)

    if 'Close' in command:
        message = "Door "
        if 'door' in command:
            message = message + "locked"
            GPIO.output(red, 1)
            p.ChangeDutyCycle(7)
            GPIO.output(green, 0)
            print ("door locked")
        message = message
        bot.sendMessage (chat_id, message)
    p.stop()


    if command == '/snapshot':
        requests.get('http://localhost:8080/0/action/snapshot')
    elif command == '/status':
        webcontrol(chat_id, 'detection', 'status')
    elif command == '/pause':
        webcontrol(chat_id, 'detection', 'pause')
    elif command == '/resume':
        webcontrol(chat_id, 'detection', 'start')
    elif command == '/check':
        webcontrol(chat_id, 'detection', 'connection')
    elif command == '/time':
        bot.sendMessage(chat_id, 'now is '+str(datetime.datetime.now()))
    elif command == '/video':
        # the most recent video in this particular folder of complete vids
        video = max(glob.iglob('/home/pi/motion/detected/video/*.mp4'), key=os.path.getctime)
        # send video, adapt the the first argument to your own telegram id
        bot.sendVideo(your id, video=open(video, 'rb'), caption='last video')

# adapt the following to the bot_id:bot_token
bot = telepot.Bot('Your-token')

MessageLoop(bot, handle).run_as_thread()
print ('I am listening ...')

while 1:
    time.sleep(10)
