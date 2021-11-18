import os
import socket
import tkinter
import tkinter.messagebox
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
import demo.neo4j.Neo_Fun as NeoFun
import cv2
import numpy as np
import ftplib

if input() == '1':
    IP = '47.100.93.63'
    PORT = '6666'
else:
    IP = '127.0.0.1'
    PORT = 6666

user = ''
OnlineBox = ''  # 用于显示在线用户的列表框
show = 1  # 用于判断是开还是关闭列表框
users = []  # 在线用户列表
chat = '------Group chat-------'  # 聊天对象

# neo4j数据库
graph = NeoFun.ConnectNeo4j()
# neo4j数据库

# 登陆窗口
LoginUI = tkinter.Tk()
LoginUI.geometry("400x250")
LoginUI.title('用户登陆窗口')
LoginUI.resizable(0, 0)
Label_One = tkinter.Label(LoginUI, width=400, height=250, bg="LightBlue")
Label_One.pack()

Account = tkinter.StringVar()
Account.set('')
Password = tkinter.StringVar()
Password.set('')

pic = tkinter.Label(LoginUI, text='', bg="LightBlue")
pic.place(x=200, y=5, width=100, height=40)

UserAccount = tkinter.Label(LoginUI, text='用户名：', bg="LightBlue")
UserAccount.place(x=50, y=20, width=100, height=40)
UserAccountLabel = tkinter.Entry(LoginUI, width=60, textvariable=Account)
UserAccountLabel.place(x=150, y=25, width=100, height=30)

UserPassword = tkinter.Label(LoginUI, text='密码：', bg="LightBlue")
UserPassword.place(x=50, y=70, width=100, height=40)
UserPasswordLabel = tkinter.Entry(LoginUI, width=60, textvariable=Password)
UserPasswordLabel.place(x=150, y=75, width=100, height=30)


def Login(*args):
    Account0 = UserAccountLabel.get()
    Password0 = UserPasswordLabel.get()
    print(Account0, Password0)
    if not Account0:
        tkinter.messagebox.showwarning('warning', message='用户名为空!')
    elif not Password0:
        tkinter.messagebox.showwarning('warning', message='密码为空!')
    else:
        if not NeoFun.isAccountExist(graph, Account0):
            tkinter.messagebox.showwarning('warning', message='用户名不存在')
        elif NeoFun.isCoupleAccountPassword(graph, Account0, Password0):
            global UA
            UA = Account0
            tkinter.messagebox.showwarning('warning', message='登陆成功')
            LoginUI.destroy()
        else:
            tkinter.messagebox.showwarning('warning', message='用户名或密码不匹配')


def Register(*args):
    Account0 = UserAccountLabel.get()
    Password0 = UserPasswordLabel.get()
    if not Account0:
        tkinter.messagebox.showwarning('warning', message='用户名为空!')
    elif not Password0:
        tkinter.messagebox.showwarning('warning', message='密码为空!')
    else:
        if NeoFun.isAccountExist(graph, Account0):
            tkinter.messagebox.showwarning('warning', message='用户名已存在')
        else:
            NeoFun.RegisterNeo4j(graph, Account0, Password0)
            tkinter.messagebox.showwarning('warning', message='账号注册成功')


LoginButton = tkinter.Button(LoginUI, text="登录", command=Login, bg="Yellow")
LoginButton.place(x=120, y=150, width=40, height=25)
LoginUI.bind('<Return>', Login)

RegisterButton = tkinter.Button(LoginUI, text="注册", command=Register, bg="Yellow")
RegisterButton.place(x=240, y=150, width=40, height=25)

LoginUI.mainloop()

# 建立连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, int(PORT)))
if UA:
    s.send(UA.encode())  # 发送用户名
else:
    s.send('用户名不存在'.encode())
    UA = IP + ':' + PORT

# 聊天窗口
MainBoxUI = tkinter.Tk()
MainBoxUI.geometry("800x480")  # 640*480
MainBoxUI.title('网络聊天室')
MainBoxUI.resizable(False, False)

# 消息界面
MessageBox = ScrolledText(MainBoxUI)
MessageBox.place(x=5, y=0, width=640, height=320)
MessageBox.tag_config('tag1', foreground='red', backgroun="yellow")
MessageBox.insert(tkinter.END, '欢迎来到网络聊天室，请注意网络文明噢', 'tag1')

# 输入框
InputText = tkinter.StringVar()
InputText.set('')
InputTextLabel = tkinter.Entry(MainBoxUI, width=120, textvariable=InputText)
InputTextLabel.place(x=5, y=320, width=580, height=170)

# 在线用户列表
OnlineBox = tkinter.Listbox(MainBoxUI)
OnlineBox.place(x=510, y=0, width=130, height=320)

# 工具箱列表
ToolMessage = tkinter.Listbox(MainBoxUI)
ToolMessage.place(x=640, y=0, width=140, height=480)


def SendImg(*args):
    FilePath = tkinter.filedialog.askopenfilename()
    file = open(FilePath, 'rb')
    ftp = ftplib.FTP()
    ftp.set_debuglevel(2)
    ftp.set_pasv(0)
    ftp.connect('47.100.93.63', 21)
    ftp.login('user', '12345')
    ftp.delete('test.jpg')
    ftp.storbinary('STOR test.jpg', file, 1024)
    ftp.close()
    message = "图片发送成功" + '~' + user + '~' + chat
    pic = cv2.imread(FilePath)
    s.send(message.encode())


def SendVid(*args):
    FilePath = tkinter.filedialog.askopenfilename()
    file = open(FilePath, 'rb')
    ftp = ftplib.FTP()
    ftp.set_debuglevel(2)
    ftp.set_pasv(0)
    ftp.connect('47.100.93.63', 21)
    ftp.login('user', '12345')
    ftp.delete('test.mp4')
    ftp.storbinary('STOR test.mp4', file, 1024)
    ftp.close()
    message = "视频发送成功" + '~' + user + '~' + chat
    pic = cv2.imread(FilePath)
    s.send(message.encode())


def SendFile(*args):
    FilePath = tkinter.filedialog.askopenfilename()
    file = open(FilePath, 'rb')
    ftp = ftplib.FTP()
    ftp.set_debuglevel(2)
    ftp.set_pasv(0)
    ftp.connect('47.100.93.63', 21)
    ftp.login('user', '12345')
    ftp.storbinary('STOR test', file, 1024)
    ftp.close()
    message = "文件发送成功" + '~' + user + '~' + chat
    pic = cv2.imread(FilePath)
    s.send(message.encode())


Picture = tkinter.Button(MainBoxUI, text="发送图片", command=SendImg, bg="gray")
Picture.place(x=640, y=0, width=160, height=40)
Picture = tkinter.Button(MainBoxUI, text="发送视频", command=SendVid, bg="gray")
Picture.place(x=640, y=40, width=160, height=40)
Picture = tkinter.Button(MainBoxUI, text="发送文件", command=SendFile, bg="gray")
Picture.place(x=640, y=80, width=160, height=40)


def send(*args):
    message = InputTextLabel.get() + '~' + user + '~' + chat
    NeoFun.CreateNode(graph, 'message', {"name": InputTextLabel.get(), "sender": user})
    NeoFun.CreateRelationship(graph, 'user', {"name": user}, 'message', {"name": InputTextLabel.get(), "sender": user},
                              'say')
    s.send(message.encode())
    InputText.set('')


sendButton = tkinter.Button(MainBoxUI, text="\n发\n\n\n送", anchor='n', command=send, font=('Helvetica', 18), bg='white')
sendButton.place(x=585, y=320, width=55, height=300)
MainBoxUI.bind('<Return>', send)


def receive():
    global uses
    while True:
        data = s.recv(1024)
        data = data.decode()
        try:
            uses = json.loads(data)
            OnlineBox.delete(0, tkinter.END)
            OnlineBox.insert(tkinter.END, "当前在线用户")
            OnlineBox.insert(tkinter.END, "------Group chat-------")
            for x in range(len(uses)):
                OnlineBox.insert(tkinter.END, uses[x])
            users.append('------Group chat-------')
        except:
            data = data.split('~')
            message = data[0]
            userName = data[1]
            chatwith = data[2]
            if "图片发送成功" in message:
                ftp = ftplib.FTP()
                ftp.set_pasv(0)
                ftp.connect('47.100.93.63', 21)
                ftp.login('user', '12345')
                filename = 'pic.jpg'
                os.remove(filename)
                ftp.retrbinary("RETR test.jpg", open(filename, "ab").write, 1024)
                pic = cv2.imread(filename)
                cv2.imshow('picture', pic)
                cv2.waitKey(0)
            elif "视频发送成功" in message:
                ftp = ftplib.FTP()
                ftp.set_pasv(0)
                ftp.connect('47.100.93.63', 21)
                ftp.login('user', '12345')
                filename = 'vid.mp4'
                # os.remove(filename)
                ftp.retrbinary("RETR test.mp4", open(filename, "ab").write, 1024)
                cap = cv2.VideoCapture(filename)
                while cap.isOpened():
                    ret, frame = cap.read()
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break
                cap.release()
                cv2.destroyAllWindows()
            elif "文件发送成功" in message:
                ftp = ftplib.FTP()
                ftp.set_pasv(0)
                ftp.connect('47.100.93.63', 21)
                ftp.login('user', '12345')
                filename = 'file'
                ftp.retrbinary("RETR test", open(filename, "ab").write, 1024)
            message = '\n' + message
            if chatwith == '------Group chat-------':  # 群聊
                MessageBox.insert(tkinter.END, message)
            elif userName == user or chatwith == user:  # 私聊
                MessageBox.tag_config('tag2', foreground='red')
                MessageBox.insert(tkinter.END, message, 'tag2')
            MessageBox.see(tkinter.END)


r = threading.Thread(target=receive)
r.start()

MainBoxUI.mainloop()
s.close()
