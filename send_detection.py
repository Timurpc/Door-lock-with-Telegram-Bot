import telepot
import sys

bot = telepot.Bot('your-token')

pic = sys.argv[1]

if pic.endswith("snapshot.jpg"):
    cap = ('snapshot')

else:
    cap = ('motion detected')


bot.sendPhoto(yourid, photo=open(pic, 'rb'), caption=cap)

exit(0)    
