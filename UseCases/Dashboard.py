# Dashboard para connexion a sensor (Desktop)
import socket
import re

# Casos de uso:
# 1. Modificar intervalo de medición
# 2. Modificar Formato de salida
# 3. Actualizar datos de pantalla
# 4. Modificar red y contraseña
def clientSocket():
    s = socket.socket()
    host = '192.168.1.83'
    port = 49152
    s.connect((host, port))
    return s

def sendCommand(s, command):
    s.send(command.encode())

def main():
    print("Dashboard")
    s = clientSocket()
    while True:
        if s.recv(1024).decode() == 'Stolen':
            print("El dispositivo ha sido robado")
            break
        print("1. Modificar intervalo de medición")
        print("2. Modificar Formato de salida GPS")
        print("3. Actualizar datos de pantalla")
        print("4. Modificar red y contraseña")
        print("5. Salir")
        command = input("Ingrese el comando: ")
        if not re.search(r'[1-5]', command):
            print("Comando inválido")
            continue
        if command == '1':
            interval = input("Ingrese el intervalo de medición: ")
            interval = command+','+interval
            sendCommand(s, interval)
        elif command == '2':
            print("Formatos de salida GPS:")
            print("1: b'$GPGGA: Latitud, Longitud, Satélites, Hora")
            print("2: b'$GPVTG: Velocidad, Rumbo")
            print("3: b'$GPGSV: Satélites visibles")
            print("4: b'$GPRMC: Hora, Latitud, Longitud, Velocidad")
            opciones = {'1': 'b\'$GPGGA', '2': 'b\'$GPVTG', '3': 'b\'$GPGSV', '4': 'b\'$GPRMC'}
            format = input("Ingrese el formato de salida de GPS: ")
            if re.search(r'[1-4]', format):
                format = command+','+opciones[format]
                sendCommand(s, format)
        elif command == '3':
            print("Modos de visualización:")
            print("1. Formato Temperatura y Humedad")
            print("2. Formato GPS")
            display = input("Ingrese el modo de visualización: ")
            if re.search(r'[1-2]', display):
                display = command+','+display
                sendCommand(s, display)
        elif command == '4':
            network = input("Ingrese el nombre de la red: ")
            password = input("Ingrese la contraseña de la red: ")
            command = command+','+network+','+password
            sendCommand(s, command)
        elif command == '5':
            sendCommand(s, command)
            break
    s.close()

if __name__ == '__main__':
    main()

