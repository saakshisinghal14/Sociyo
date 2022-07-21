
import threading
import socket

host='127.0.0.1' #hostname
port=55558
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("socket is build")
server.bind((host,port))
server.listen()

clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break
def receive():
    while True:
        client,address=server.accept()
        print('connected with',address)
        client.send('nick'.encode('ascii'))
        nickname=client.recv(1024).decode('ascii')  
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined to the chat'.encode('ascii'))
        client.send("connected to the server".encode('ascii'))
        
        thread=threading.Thread(target=handle,args=(client,))
        thread.start()

print("Server is wait for clients....")
receive()



               
