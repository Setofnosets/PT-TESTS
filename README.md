# **Descripcion:**
Este proyecto consiste en el desarrollo de un sensor remotamente programable mediante el uso de MicroPython y un microcontrolador de la familia ESP32. Cada carpeta cuenta con un ejemplo del funcionamiento de algún sensor con el microcontrolador.
# **Contenidos:**
* Battery: Pruebas para el módulo AXP2101 de energía como la medicion de la bateria restante
* bots: Bots simples para la comunicación con el protocolo MQTT
* Co2: Utilizacion de un sensor Co2 con I2C
* GPS: Recolección de datos geograficos mediante el módulo NEO-6M
* Lora: Pruebas con la recepción de datos mediante LoRa (No funcional)
* Temp: Medición de temperatura y humedad con el módulo DHT11
* Juntos: Todos los sensores utilizados en el mismo programa (Sin probar)
* UpdateTests: Pruebas para la actualización del dispositivo de manera remota:
 *  ErroresWebREPL: Demostración de la funcionalidad de WebREPL cuando ocurre un error en la ejecución
 *  FTPwebREPL: Demostración de WebREPL donde al enviar un archivo nuevo y reiniciar la tarjeta, se modifica el comportamiento
 *  ParamWebREPL: Demostración de WebREPL donde el comportamiento se cambia al ejecutar una función que toma diferentes parámetros de entrada
 *  ReloadWebREPL: Demostración de WebREPL donde el procesamiento de realiza en un módulo que periodicamente se vuelve a cargar, si se reemplaza el archivo del módulo, el programa carga el nuevo archivo y el comportamiento cambia
 *  TCPSockets: Actualización del dispositivo mediante mensajes transmitidos por una conexión con sockets TCP
 *  UpdateTempTime: Demostración sockets para cambiar el intervalo de medición del módulo DHT11
* UseCases: Demostración de posibles casos de uso del sensor, permite alternar entre medir temperatura y humedad e información geográfica, adicionalmente, permite modificar que sentencia NMEA mostrará 
