import sys

palabra = sys.argv[1]
key = int(sys.argv[2])

cifrado = ""
    
for i in palabra:
    if i.isalpha():
        letra = ord(i)
            
        if i.islower():    
            cifrado = cifrado + chr((letra - 97 + key) % 26 + 97)
                
        elif i.isupper():
            cifrado = cifrado + chr((letra - 65 + key) % 26 + 65)
                
    else:
        cifrado = cifrado + " "
            
print(cifrado)

        
        