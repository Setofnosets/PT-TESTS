# Casos de uso:
# 1. Modificar intervalo de medición
# 2. Modificar Formato de salida
# 3. Actualizar datos de pantalla
# 4. Modificar red y contraseña

from machine import Pin, I2C, ADC, SoftI2C, UART
import ssd1306
import dht
import machine
import time
import socket
import select
import time, utime

RX = 34
TX = 12
SCL = 22
SDA = 21

gps = UART(1, baudrate=9600, rx=RX, tx=TX)

buffer = bytearray(255)

TIMEOUT = False
FIX_STATUS = False

timeout = 20
gps_measure = "b'$GPGGA"
latitude = ""
longitude = ""
satellites = ""
GPStime = ""
info = ""
stolen = False

# Condiciones Anormales
conditions = {
    'Ubicacion modificada': lambda x, y: abs(x - y) > 0.001,
    'Tiempo de respuesta excedido': lambda x: time.time() > x,
    'Temperatura fuera de rango': lambda x: x < 0 or x > 50
}

active_conditions = [] # Default

def do_connect(network_name='INFINITUMFE9D_2.4', network_password='u5YK4Z49Rt'):
    oled = screen()
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        oled.text('connecting to network...', 0, 0)
        oled.show()
        sta_if.active(True)
        sta_if.connect(network_name, network_password)
        while not sta_if.isconnected():
            pass

def screen():
    oled_width = 128
    oled_height = 64
    i2c = SoftI2C(scl=Pin(SCL), sda=Pin(SDA), freq=10000)
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.fill(0)
    oled.text('Connecting...', 0, 0)
    return oled

def measure_temp():
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    return str(temp) + ' ' + str(hum)

# https://aprs.gids.nl/nmea/
def getGPS(gpsModule, sentence):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime

    timeout = time.time() + measure_interval
    while True:
        info = ""
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
        print(parts)

        # GPGGA - Global Positioning System Fix Data
        # GPGSV - GPS Satellites in View
        # GPRMC - Recommended Minimum Specific GPS/TRANSIT Data
        # GPVTG - Track Made Good and Ground Speed
        if (sentence == "b'$GPGGA" == parts[0] and len(parts) == 15):
            if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                print(buff)
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = "-"+longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                info = "Lat: " + latitude + "\nLong: " + longitude + "\nSat: " + satellites + "\nTime: " + GPStime
                break
        elif (sentence == "b'$GPVTG" == parts[0] and len(parts) >= 9):
            if (parts[1] and parts[5]):
                print(buff)
                info = "Speed: " + parts[5]
                break
        elif (sentence == "b'$GPGSV" == parts[0] and len(parts) >= 7):
            if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6]):
                print(buff)
                satellites = parts[3]
                info = "Sat: " + satellites + "\nElevation: " + parts[4] + "\nAzimuth: " + parts[5] + "\nSNR: " + parts[6]
                break
        elif (sentence == "b'$GPRMC" == parts[0] and len(parts) >= 10):
            if (parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7] and parts[9]):
                print(buff)
                latitude = convertToDegree(parts[3])
                if (parts[4] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[5])
                if (parts[6] == 'W'):
                    longitude = "-"+longitude
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                info = "Lat: " + latitude + "\nLong: " + longitude + "\nTime: " + GPStime + "\nSpeed: " + parts[7] + "\nDate: " + parts[9]
                break
        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)
    return info

def convertToDegree(RawDegrees):
    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat / 100)
    nexttwodigits = RawAsFloat - float(firstdigits * 100)

    Converted = float(firstdigits + nexttwodigits / 60.0)
    Converted = '{0:.6f}'.format(Converted)
    return str(Converted)

# Default: temperatura y humedad
mode = 1
def display_mode(oled, mode, info):
    if info == "":
        return
    oled.fill(0)
    if mode == 1:
        temp = info.split(' ')[0]
        hum = info.split(' ')[1]
        oled.text("Temperature: " + temp, 0, 0)
        oled.text("Humidity: " + hum, 0, 10)
    elif mode == 2:
        data = info.split('\n')
        for i in range(len(data)):
            oled.text(data[i], 0, i*10)
    oled.show()

def measures(mode):
    if mode == 1:
        return measure_temp()
    elif mode == 2:
        return getGPS(gps, gps_measure)

def evaluate_conditions(active_conditions):
    for condition in active_conditions:
        if condition == 'Ubicacion modificada':
            return conditions[condition](pastLatitude, latitude)
        elif condition == 'Tiempo de respuesta excedido':
            return conditions[condition](timeout)
        elif condition == 'Temperatura fuera de rango':
            return conditions[condition](temp)
    return False

oled = screen()

measure_interval = 1 #default interval
temp = 0
hum = 0

d = dht.DHT11(machine.Pin(4))

#Create server socket
serversocket = socket.socket()

#Bind to port
port = 49152
serversocket.bind(('', port))

#Start listening
serversocket.listen(0)

#Accept a connection
serversocket.setblocking(False)
#c, addr = serversocket.accept()
#print('Got connection from', addr)

poller = select.poll()
#poller.register(c, select.POLLIN)
c = None

#Main loop
while True:
    try:
        #If connection is lost, try to accept a new one
        if not c:
            pastLatitude = latitude
            pastLongitude = longitude
            info = measures(mode)

            if evaluate_conditions(active_conditions):
                print("Condiciones anormales detectadas")
                stolen = True
                continue

            print(info)
            display_mode(oled, mode, info)

            c, addr = serversocket.accept()
            print('Got connection from', addr)
            poller.register(c, select.POLLIN)

            time.sleep(measure_interval)
            continue
        else:
            # Poll and wait for specified time
            y = poller.poll(measure_interval * 1000)
            if stolen:
                mssg = "Condicion anormal: " + info + "\nDate: " + str(time.localtime()) + "\nCondition: " + str(active_conditions)
                c.send(mssg.encode())
                stolen = False
            # If no data is received, measure temperature, humidity and GPS data
            if not y:
                pastLatitude = latitude
                pastLongitude = longitude
                info = measures(mode)
                if evaluate_conditions(active_conditions):
                    print("Condiciones anormales detectadas")
                    stolen = True
                    continue
                print(info)
                display_mode(oled, mode, info)
                continue
            else:
                # If data is received, send temperature, humidity and GPS data and update information
                x = c.recv(1024).decode()
                print("Command: " + x)
                # Separar comas
                x = x.split(',')

                # 1. Modificar intervalo de medición
                # 2. Modificar Formato de salida
                # 3. Actualizar datos de pantalla
                # 4. Modificar red y contraseña
                if x[0] == "1":
                    # El cliente envía un nuevo intervalo de medición
                    # Timeout de 8 segundos
                    measure_interval = int(x[1])
                    print("New interval: " + str(measure_interval))
                    continue
                elif x[0] == "2":
                    # Modificar formato de salida GPS
                    # b'$GPGGA: Latitud, Longitud, Satélites, Hora
                    # b'$GPVTG: Velocidad, Rumbo
                    # b'$GPGSV: Satélites visibles
                    # b'$GPRMC: Hora, Latitud, Longitud, Velocidad
                    gps_measure = x[1]
                    print("New GPS format: " + gps_measure)
                    continue
                elif x[0] == "3":
                    # Actualizar datos de pantalla
                    # 1. Mostrar temperatura y humedad
                    # 2. Mostrar GPS
                    format = int(x[1])
                    mode = format
                    print("New display mode: " + str(mode))
                    continue
                elif x[0] == "4":
                    # Modificar red y contraseña
                    network = x[1]
                    print("New network: " + network)
                    password = x[2]
                    print("New password: " + password)
                    do_connect(network, password)
                    continue
                elif x[0] == "5":
                    # Condiciones
                    # 1. Ubicación
                    # 2. Timeout
                    # 3. Temperatura
                    condition = x[1]
                    if condition == "1":
                        active_conditions.append('Ubicacion modificada')
                    elif condition == "2":
                        active_conditions.append('Tiempo de respuesta excedido')
                    elif condition == "3":
                        active_conditions.append('Temperatura fuera de rango')
                    print("New condition: " + condition)
                if x[0] == "6":
                    c = None
                    continue
                else:
                    info = measures(mode)
                    display_mode(oled, mode, info)
                    continue
                FIX_STATUS = False
                continue
    except Exception as e:
        print(e)
        continue
    except KeyboardInterrupt:
        break
    except OSError:
        continue
    except ValueError:
        continue
    except RuntimeError:
        continue
    except MemoryError:
        continue
    except Exception:
        continue