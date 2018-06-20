import network
from main import main
import time
#import upip
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("aaaa", "aaaaa")
ct=0
print("publicador funcionou")

while station.isconnected()==False:
    time.sleep(0.5)
    ct+=1
    if ct>10:
        print("nao conectou")
        break


print("agora conector na rede")    
prg = main()

prg.Start()
#upip.install('micropython-uasyncio')
#upip.install('micropython-umqtt.simple')
#upip.install('micropython-umqtt.robust')