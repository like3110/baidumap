from tkinter import *
import win32clipboard
from tkinter.ttk import Combobox
import win32con
import base64
from Crypto import Random
from Crypto.Cipher import AES

def writeclipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, text)
    win32clipboard.CloseClipboard()

def decrypt(encryptedPassword):
    base64Decoded = base64.b64decode(encryptedPassword)
    unpad = lambda s: s[:-(s[-1])]
    iv = base64Decoded[:AES.block_size]
    key = base64Decoded[-32:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plainPassword = unpad(cipher.decrypt(base64Decoded[:-32]))[AES.block_size:]
    return plainPassword


def getPassword(plainPassword):
    def pad(s):
        x = AES.block_size - len(s) % AES.block_size
        return s + (chr(x) * x)
    paddedPassword = pad(plainPassword)
    iv = Random.OSRNG.new().read(AES.block_size)
    key = Random.OSRNG.new().read(32)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encryptedPassword = base64.b64encode(iv + cipher.encrypt(paddedPassword) + key)
    return encryptedPassword

def getPw():
    passwd = e1.get()
    type = typeChosen.get()
    if type == '加密':
        res = getPassword(passwd)
    else:
        res = decrypt(passwd)
    writeclipboard(res)
    pw.set(res)

root = Tk()
root.title("密码转换")
root.geometry("960x100")#width x height;
s3=Label(root,text="转换类型：")
s3.grid(row=1,column=1,sticky=W)
type = StringVar()
typeChosen = Combobox(root, width=12, textvariable=type,state="readonly")
typeChosen['values'] = ('加密','解密')     # 设置下拉列表的值
typeChosen.grid(row=1,column=2,sticky=W)      # 设置其在界面中出现的位置  column代表列   row 代表行
typeChosen.current(0)
s1=Label(root,text="明文：")
s1.grid(row=2,column=1,sticky=W)
e1=Entry(root,width='120')
e1.grid(row=2,column=2,sticky=W)
s2=Label(root,text="密文：")
s2.grid(row=3,column=1,sticky=W)
pw = StringVar()
Entry(root,textvariable=pw,state="readonly",width='120').grid(row=3,column=2,sticky=W)
submit = Button(root,text="执行复制到剪切板", command=getPw)
submit.grid(row=4,column=2,sticky=W)
root.mainloop()