import threading
import socket
import time
import json
  
host = '127.0.0.1' # endereço IP do servidor
port = 41905       # porta disponibilizada pelo servidor
buffer = 1024      # definição do tamanho do buffer
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM == TCP.
server.bind((host,port)) #IP e porta que o servidor deve aguardar a conexão
server.listen(10)#Define o limite de conexões.

users = [] #Lista de usuarios e nomes
names = []

def broadcast(msg): #mensagem para todos usuarios
    for user in users:
        user.send(msg)

def handle(user): #verifica estado do usuario
    while True:
        try:
            msg = user.recv(buffer)
            print(f'{msg}')
            broadcast(msg)
        except:
            i = users.index(user)
            users.remove(user)
            user.close()
            name = names[i]
            print(f'{name} desconectou.'.encode('ascii'))
            broadcast(f'{name} saiu do chat.\n'.encode('ascii'))
            names.remove(name)
            break
        
def userSend(user):#envia lista de usuarios conectados
    while True:
        try:
            time.sleep(3)
            msg = json.dumps({"USERS":names})
            broadcast(msg.encode('ascii'))
        except Exception as e:
            print(e)
            break

def main():
    while True:
        user,addr = server.accept()
        print(f'{addr} conectado!\n')
        user.send('NAME'.encode('ascii'))
        name = user.recv(buffer).decode('ascii')
        names.append(name)
        users.append(user)
        time.sleep(1)
        print(f'{name} entrou!\n')
        user.send('Conectado ao servidor!\n'.encode('ascii'))
        broadcast(f'{name} entrou no chat!\n'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(user,))
        thread.start()
        thread2 = threading.Thread(target=userSend, args=(user,))
        thread2.start()
main()
