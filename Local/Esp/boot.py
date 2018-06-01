import network
from main import main
import time
#import upip
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("id", "senha")

while station.isconnected()==False:
    time.sleep(0.5)

print("agora conector na rede")    
prg = main()

prg.Start()
#upip.install('micropython-uasyncio')
#upip.install('micropython-umqtt.simple')
#upip.install('micropython-umqtt.robust')