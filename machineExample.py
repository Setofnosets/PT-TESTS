import machine

machine.freq(160000000) # Establece la frecuencia del procesador a 160 MHz

p0 = machine.Pin(0, machine.Pin.OUT) # Designa el pin 0 como salida

p0.value(0) # Establece el pin 0 en bajo
p0.value(1) # Establece el pin 0 en alto

adc = machine.ADC(0) # Designa el pin 0 como entrada analógica
val = adc.read() # Lee el valor de la entrada analógica