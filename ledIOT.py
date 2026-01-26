# Importación de módulos necesarios
import time  # Módulo para funciones relacionadas con el tiempo (no se utiliza en este código, pero está disponible si se necesita).
from machine import Pin  # Importa la clase Pin para controlar los pines GPIO del ESP32.
import network  # Módulo para manejar la conexión WiFi.
import socket  # Módulo para crear y manejar conexiones de red (sockets).

# Configuración de los pines GPIO para los LEDs (número de pin, dirección, valor inicial)
led_pin1 = Pin(12, Pin.OUT, value=0)  # Pin 12 configurado como salida, inicializado apagado.
led_pin2 = Pin(14, Pin.OUT, value=0)  # Pin 14 configurado como salida, inicializado apagado.
led_pin3 = Pin(27, Pin.OUT, value=0)  # Pin 27 configurado como salida, inicializado apagado.
led_pin4 = Pin(2, Pin.OUT, value=0)   # Pin 2 configurado como salida, inicializado apagado.

# Credenciales WiFi
ssid = 'TP-Link_DFC5'  # Nombre de la red WiFi (SSID).
password = '80812401'  # Contraseña de la red WiFi.

# Configuración de la interfaz WiFi
wlan = network.WLAN(network.STA_IF)  # Inicializa la interfaz de cliente WiFi (STA_IF: estación).
wlan.active(True)  # Activa la interfaz WiFi para que pueda buscar redes y conectarse.
wlan.connect(ssid, password)  # Inicia la conexión a la red WiFi con el SSID y la contraseña proporcionados.

# Espera hasta que la conexión WiFi se establezca
while not wlan.isconnected():  # Mientras no esté conectado al WiFi, permanece en este bucle.
    pass  # No realiza ninguna acción dentro del bucle, solo espera.

# Una vez conectado, imprime la información de la conexión
print('Conexión con el WiFi %s establecida' % ssid)  # Imprime un mensaje indicando que la conexión fue exitosa.
print(wlan.ifconfig())  # Muestra la configuración de red actual (IP, máscara, puerta de enlace, DNS).

# Configuración del servidor web
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket TCP/IP.
server_socket.bind(('', 80))  # Asigna el socket a todas las interfaces disponibles ('') en el puerto 80 (HTTP).
server_socket.listen(3)  # Configura el socket para aceptar hasta 3 conexiones simultáneas.

# Función para generar la página web que se muestra al usuario
def web_page():
    # Contenido HTML con botones para encender y apagar cada LED
    html = """
    <h1><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Control Leds</h1></b><br>
    <body> 
        <b>&nbsp;Led 1&nbsp;&nbsp;</b>
        <a href="/?led1=on"><button style='width:100px; height:35px; background-color: #00ff00'>Encender</button></a>&nbsp;&nbsp;
        <a href="/?led1=off"><button style='width:100px; height:35px; background-color: #ff5252'>Apagar</button></a><br><br>
        <b>&nbsp;Led 2&nbsp;&nbsp;</b>
        <a href="/?led2=on"><button style='width:100px; height:35px; background-color: #00ff00'>Encender</button></a>&nbsp;&nbsp;
        <a href="/?led2=off"><button style='width:100px; height:35px; background-color: #ff5252'>Apagar</button></a><br><br>
        <b>&nbsp;Led 3&nbsp;&nbsp;</b>
        <a href="/?led3=on"><button style='width:100px; height:35px; background-color: #00ff00'>Encender</button></a>&nbsp;&nbsp;
        <a href="/?led3=off"><button style='width:100px; height:35px; background-color: #ff5252'>Apagar</button></a><br><br>
        <b>&nbsp;Led 4&nbsp;&nbsp;</b>
        <a href="/?led4=on"><button style='width:100px; height:35px; background-color: #00ff00'>Encender</button></a>&nbsp;&nbsp;
        <a href="/?led4=off"><button style='width:100px; height:35px; background-color: #ff5252'>Apagar</button></a>
    </body>
    """
    return html  # Devuelve el contenido HTML generado.

# Bucle principal del servidor para manejar solicitudes de clientes
while True:
    conn, addr = server_socket.accept()  # Espera y acepta una nueva conexión entrante (conn: conexión, addr: dirección del cliente).
    print('Nueva conexión desde: %s' % str(addr))  # Muestra la dirección IP del cliente que se conectó.
    request = conn.recv(1024)  # Recibe la solicitud HTTP del cliente (hasta 1024 bytes).
    print('Solicitud = %s' % str(request))  # Imprime la solicitud recibida.
    request = str(request)  # Convierte la solicitud a una cadena para su análisis.

    # Analiza la solicitud para determinar qué LED controlar
    if '/?led1=on' in request:  # Si la solicitud contiene '/?led1=on', enciende el LED 1.
        print('Estado: Led 1 Encendido')  # Muestra en consola que el LED 1 está encendido.
        led_pin1.on()  # Enciende el LED conectado al pin 12.
    if '/?led1=off' in request:  # Si la solicitud contiene '/?led1=off', apaga el LED 1.
        print('Estado: Led 1 Apagado')  # Muestra en consola que el LED 1 está apagado.
        led_pin1.off()  # Apaga el LED conectado al pin 12.

    if '/?led2=on' in request:  # Si la solicitud contiene '/?led2=on', enciende el LED 2.
        print('Estado: Led 2 Encendido')
        led_pin2.on()  # Enciende el LED conectado al pin 14.
    if '/?led2=off' in request:  # Si la solicitud contiene '/?led2=off', apaga el LED 2.
        print('Estado: Led 2 Apagado')
        led_pin2.off()  # Apaga el LED conectado al pin 14.

    if '/?led3=on' in request:  # Si la solicitud contiene '/?led3=on', enciende el LED 3.
        print('Estado: Led 3 Encendido')
        led_pin3.on()  # Enciende el LED conectado al pin 27.
    if '/?led3=off' in request:  # Si la solicitud contiene '/?led3=off', apaga el LED 3.
        print('Estado: Led 3 Apagado')
        led_pin3.off()  # Apaga el LED conectado al pin 27.

    if '/?led4=on' in request:  # Si la solicitud contiene '/?led4=on', enciende el LED 4.
        print('Estado: Led 4 Encendido')
        led_pin4.on()  # Enciende el LED conectado al pin 2.
    if '/?led4=off' in request:  # Si la solicitud contiene '/?led4=off', apaga el LED 4.
        print('Estado: Led 4 Apagado')
        led_pin4.off()  # Apaga el LED conectado al pin 2.

    # Genera la respuesta HTTP con la página web
    response = web_page()  # Llama a la función que genera el contenido HTML.
    conn.send('HTTP/1.1 200 OK\n')  # Envía el encabezado HTTP de respuesta.
    conn.send('Content-Type: text/html\n')  # Especifica que el contenido es HTML.
    conn.send('Connection: close\n\n')  # Cierra la conexión después de enviar la respuesta.
    conn.sendall(response)  # Envía todo el contenido de la página HTML.
    conn.close()  # Cierra la conexión con el cliente.
