import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import json

host = '127.0.0.1' # endereço IP do servidor 
port = 41905       # porta disponibilizada pelo servidor
buffer = 1024     #buffer de mensagens

class Client: #classe cliente
    def __init__(self,host,port):
        self.UIdone = False
        self.run = True
        self.user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Criação de socket TCP do cliente
        self.user.connect((host,port))# Conecta ao servidor em IP e porta especifica

        msg = tkinter.Tk()
        msg.withdraw()
        self.name = simpledialog.askstring("Nome:","Escreva seu nome",parent = msg)#caixa de nome

        UIthread = threading.Thread(target=self.UI)#iniciando threads de interface e recebimento de mensagens
        UIthread.start()
        receiveThread = threading.Thread(target=self.receive)
        receiveThread.start()

    def UI(self):#configurando interface do usuario
        self.window = tkinter.Tk()#janela
        self.window.config(width = 500,height = 500,bg = "#99cccc")
                              
        self.chatTxt = tkinter.Label(self.window,text = "Chat:",bg = "#99cccc")#text chat
        self.chatTxt.config(font =("Arial",16))
        self.chatTxt.pack(padx = 20,pady = 3)
        self.chatTxt.place(relx = 0,rely = 0.030,relheight = 0.060,relwidth = 1.000)

        self.chatArea = tkinter.scrolledtext.ScrolledText(self.window)#area de mensagens
        self.chatArea.pack(padx = 20,pady = 5)
        self.chatArea.config(state = 'disable')
        self.chatArea.place(relx = 0.03,rely = 0.100,relheight = 0.750,relwidth = 0.700)

        self.chatTxt = tkinter.Label(self.window,text = "Users:",bg = "#99cccc")#text users
        self.chatTxt.config(font =("Arial",10))
        self.chatTxt.pack(padx = 20,pady = 3)
        self.chatTxt.place(relx = 0.800,rely = 0.040,relheight = 0.060,relwidth = 0.100)

        self.userArea = tkinter.scrolledtext.ScrolledText(self.window)#area users
        self.userArea.pack(padx = 20,pady = 5)
        self.userArea.config(state = 'disable')
        self.userArea.place(relx = 0.750,rely = 0.1,relheight = 0.750,relwidth = 0.220)

        self.inputBox = tkinter.Text(self.window,height = 3)#caixa de escrita
        self.inputBox.pack(padx = 20,pady = 5)
        self.inputBox.place(relx = 0.03,rely = 0.900,relheight = 0.060,relwidth = 0.700)

        self.sendButton = tkinter.Button(self.window,text = "Enviar",command = self.write)#botão de enviar
        self.sendButton.config(font =("Arial",12))
        self.sendButton.pack(padx = 20,pady = 5)
        self.sendButton.place(relx = 0.750,rely = 0.900,relheight = 0.060,relwidth = 0.220)
                                                                  
        self.UIdone = True
        self.window.protocol("WM_DELETE_WINDOW",self.stop)#verifica de usuario fechou o chat
        self.window.mainloop()
    

    def write(self):#envio de mensagem
        msg = f"{self.name}: {self.inputBox.get('1.0','end')}"
        self.user.send(msg.encode('ascii'))
        self.inputBox.delete('1.0','end')#limpa input

    def stop(self):#finaliza cliente
        self.run = False
        self.window.destroy()
        self.user.close()
        exit(0)

    def receive(self): #receptor de mensagens
        while self.run:
            try:
                msg = self.user.recv(buffer).decode('ascii')
                if msg == 'NAME':
                    self.user.send(self.name.encode('ascii'))
                else:
                    try:
                        if self.UIdone:
                            msg = json.loads(msg)
                            m = msg.get("USERS")
                            self.userArea.config(state = 'normal')
                            self.userArea.delete('0.0','end')
                            for u in m:
                                self.userArea.config(state = 'normal')
                                self.userArea.insert('end',u + '\n')
                                self.userArea.yview('end')
                                self.userArea.config(state = 'disable')
                    except:
                        if self.UIdone:
                            self.chatArea.config(state = 'normal')
                            self.chatArea.insert('end',msg)
                            self.chatArea.yview('end')
                            self.chatArea.config(state = 'disable')
            except:
                self.user.close()
                break  
client = Client(host,port)
