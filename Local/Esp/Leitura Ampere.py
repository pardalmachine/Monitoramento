import time
adc = machine.ADC(machine.Pin(36))
adc.atten(adc.ATTN_10DB)
adc.width(adc.WIDTH_10BIT)

def LeValor():
    Media=0
    ValorAcumulado=0
    VoltsPorUnidade=0.004887586
    ValorFinal=0
    for i in range(100):
        ValorAdc = adc.read()-511
        ValorAcumulado+=ValorAdc**2

    ValorSensor = ((ValorAcumulado/100)**(1/2))*VoltsPorUnidade
    ValorFinal=ValorSensor/0.066

while True:
    print(LeValor())
    time.sleep(1)


