import network
from main import main
import time
import webrepl
#import upip
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("xpto", "mercado000")
ct=0
print("publicador funcionou")

while station.isconnected()==False:
    time.sleep(0.5)
    ct+=1
    if ct>10:
        print("nao conectou")
        break


print("agora conector na rede")    
webrepl.start()
prg = main()

prg.Start()
#upip.install('micropython-uasyncio')
#upip.install('micropython-umqtt.simple')
#upip.install('micropython-umqtt.robust')

#import network
#import webrepl
#station = network.WLAN(network.STA_IF)
#station.active(True)
#station.connect("xpto", "mercado000")
#webrepl.start()


#import network
#station = network.WLAN(network.STA_IF)
#station.active(True)
#station.connect("xpto", "mercado000")