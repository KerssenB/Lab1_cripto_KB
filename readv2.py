import sys
import scapy.all as scapy
from colorama import init, Fore, Style

dic_frecuencias_es = {
    'a': 0.1253, 'b': 0.0142, 'c': 0.0468, 'd': 0.0586, 'e': 0.1368,
    'f': 0.0069, 'g': 0.0101, 'h': 0.0070, 'i': 0.0625, 'j': 0.0044,
    'k': 0.0002, 'l': 0.0497, 'm': 0.0315, 'n': 0.0671, 'o': 0.0868,
    'p': 0.0251, 'q': 0.0088, 'r': 0.0687, 's': 0.0798, 't': 0.0463,
    'u': 0.0393, 'v': 0.0090, 'w': 0.0001, 'x': 0.0022, 'y': 0.0090,
    'z': 0.0052
}

mensajes_descifrados = []

def leer_archivo(pcapng_path):
    mensaje_cifrado = ""
    paquetes = scapy.rdpcap(pcapng_path)
   
    for p in paquetes:
        if p.haslayer(scapy.ICMP):
            data = p[scapy.ICMP].load
            mensaje_cifrado += chr(data[8] if data else "")
            
    # Para mostrar el Desplazamiento 0
    mensajes_descifrados.append(mensaje_cifrado)
    
    return mensaje_cifrado


def descifrar_mensaje(mensaje_cifrado, key):
    mensaje_descifrado = ""
    
    for i in mensaje_cifrado:
        if i.isalpha():
            
            if i.islower():
                mensaje_descifrado += chr((ord(i) - key - 97) % 26 + 97)
            
            elif i.isupper():
                mensaje_descifrado += chr((ord(i) - key - 65) % 26 + 65)
        
        else:
            mensaje_descifrado += i
            
    return mensaje_descifrado


def calcular_frecuencia(mensaje):
    frecuencia_es = {}
    total = 0
    
    for i in mensaje:
        if i.isalpha():
            frecuencia_es[i] = frecuencia_es.get(i, 0) + 1
            total += 1
            
    for letra, frecuencia in frecuencia_es.items():
        frecuencia_es[letra] = frecuencia / total
    
    return frecuencia_es


archivo = sys.argv[1]
mensaje_cifrado = leer_archivo(archivo)

mensaje_correcto = ""
mejor_puntaje = 0

for i in range(1, 26):
    mensaje_descifrado = descifrar_mensaje(mensaje_cifrado, i)
    frecuencia = calcular_frecuencia(mensaje_descifrado)
        
    mensajes_descifrados.append(mensaje_descifrado)

    # Puntuación basada en la frecuencia de letras en español
    puntaje = sum(abs(frecuencia.get(letra, 0) - dic_frecuencias_es.get(letra, 0)) for letra in frecuencia)

    if puntaje < mejor_puntaje or mejor_puntaje == 0:
        mejor_puntaje = puntaje
        mensaje_correcto = mensaje_descifrado

# Imprimir los mensajes
contador = 0

for i in mensajes_descifrados:
    if i != mensaje_correcto:
        print(str(contador) + "\t" + i)
        
    else:
        init(autoreset=True)
        print(Fore.GREEN + str(contador) + "\t" + i)
        
    contador += 1


