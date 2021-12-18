import os
import re
import sys
from tkinter import font
import qrcode
import tkinter
from tkinter import ttk
from functools import partial
from webbrowser import open_new_tab as link

from app import LOG_FILE

class State:
    address = None

def gen_qr():
    """ Generate QR code server address """

    # Read server log file
    while True:
        with open(LOG_FILE, 'r') as file:
            logs = file.read()
            
            # Search for address server is served on 
            exp = '(http)s*:\/\/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]{2,4}\/'
            State.address = re.search(exp, logs)
        
        # Extract address
        try:
            State.address = State.address.group()
            break
        except AttributeError:

            # Exit if executed independently
            if __name__ == '__main__':
                print('Could not read address of server.')
                exit()
            continue

    # Generate QR code of address
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=2,
    )
    qr.add_data(State.address)
    qr.make(fit=True)

    # Save QR code as image
    qr.make_image().save(resource_path('out.png'))


def window():
    """ Create a GUI """
    root = tkinter.Tk()
    height = 930
    width = 660
    root.title('Kalman')
    root.geometry(f'{width}x{height}')
    root.resizable(0, 0)
    root.iconphoto(False, tkinter.PhotoImage(file=resource_path('kalman.png')))
    
    bgcolor = 'white'
    root.config(background=bgcolor)

    # Read QR code image
    img = tkinter.PhotoImage(file=resource_path('out.png'))

    print(img.height(), img.width())

    title = ttk.Label(root, text='Scan the QR code to get started.')
    title.config(
        background=bgcolor,
        font='Ariel 13 bold',
        wraplength=640,
        justify='center',
    )
    title.pack(pady=(40, 0))
    
    qrcode = ttk.Label(root, image=img, background=bgcolor)
    qrcode.pack()

    address = ttk.Label(root, text=State.address)
    address.config(
        font='Mono 14',
        background=bgcolor,
        foreground='blue',
        cursor='hand2'
    )
    address.bind('<Button-1>', lambda e: link(State.address))
    address.bind('<Enter>', lambda e: address.config(font='Mono 14 underline'))
    address.bind('<Leave>', lambda e: address.config(font='Mono 14'))
    address.pack()

    imaginelenses = ttk.Label(root, text='IMAGINELENSES')
    imaginelenses.config(
        background=bgcolor,
        foreground='lightgrey',
        font='Ariel 13',
        justify='center'
    )
    imaginelenses.pack(pady=(30, 20))
    
    root.mainloop()

    # Delete QR code image
    os.system('rm out.png')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    gen_qr()
    # window()