import os
import tkinter.scrolledtext as st
from tkinter import *
from tkinter import messagebox as m
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import steno.hover as ho
import steno.audio as aud
import steno.database as db
import steno.image as image_

root = Tk()
root.title('Stegnography')
root.config(bg='white')
root.resizable(False, False)

icon_filename = 'images/l2'

if "nt" == os.name:
    icon_filename = f"{icon_filename}.ico"
else:
    icon_filename = f"@{icon_filename}.xbm"

root.wm_iconbitmap(icon_filename)

# centering the main window
root_h, root_w = 300, 400
s_w = root.winfo_screenwidth()
s_h = root.winfo_screenheight()
x_coor = int((s_w / 2) - (root_w / 2))
y_coor = int((s_h / 2) - (root_h / 2))
root.geometry("{}x{}+{}+{}".format(root_w, root_h, x_coor, y_coor))

# defining the fonts used and images
cas = ('times newroman', 10)
cas_big = ('times newroman', 20)
img = PhotoImage(file="images/noshow.png").subsample(4, 4)
img2 = PhotoImage(file="images/show.png").subsample(4, 4)

def image_steno():
    """Image steganography function"""
    img_win = Toplevel(master=root, bg='white')
    img_win.title('Image steganography')
    img_win.geometry('515x260')
    img_win.wm_iconbitmap('images/l2.ico')
    im_lb = Label(img_win, text='Image -Steganography', bg='white', fg='black', font=cas_big)
    im_lb.place(x=150, y=100)

    def em_img():
        """Image steganography functions"""
        global file, mess
        select_lb = Label(img_win, text='Select File:', font=cas, bg='grey', fg='#fa05bd')
        select_lb.place(x=5, y=50)
        file_im = Entry(img_win, width=55, font=cas, relief='ridge')
        file_im.place(x=7, y=75)
        file_im.place(x=7, y=75)
        file_im.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global file
            file = askopenfilename(parent=img_win, initialdir=os.getcwd(), title='Select File to ENCRYPT',
                                   filetypes=[('Image files', '.png')], defaultextension='.png')
            file_im.delete(0, END)
            file_im.insert(0, file)
            select_lb.config(text='Selected File:')

        se_bu = Button(img_win, text='Browse', bg='white', font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def pan():
            """Opens message prompt to enter message"""
            global mess
            message = Toplevel(img_win)
            message.title('Enter Message')
            message.resizable(False, False)
            message.wm_iconbitmap('images/l2.ico')
            lm = Label(message, text='Enter your message that you want to hide:', bg='white', font=cas)
            lm.pack(side=TOP, fill=BOTH)
            ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
            t = st.ScrolledText(message)
            t.config(font=cas)
            t.pack()

            def click(event=None):
                """Collects the message entered by user"""
                global mess
                message.withdraw()
                mess = t.get("1.0", "end-1c")

            bm = Button(message, text='Done(Ctrl+b)', command=click, relief='flat', bg='grey', font=cas)
            bm.pack(side=BOTTOM, fill=BOTH)
            ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
            message.bind('<Control-b>', click)

        b = Button(img_win, command=pan, text='Enter Message', font=cas, bg='white')
        b.place(x=10, y=100)
        ho.CreateToolTip(b, 'Opens a prompt where you can enter message')
        success = Label(img_win, bg='white', font=cas)
        success.place(x=10, y=170)

        def done():
            """Main function which asks for saving file location and then encrypts the data in image file"""
            global file, mess
            m.showinfo('Procedure', 'Where would you like the encrypted file to be saved?\n'
                                    'Select the path in the next window.')
            out = asksaveasfilename(title='Save your encrypted file as', filetypes=[('Image files', '.png')],
                                    defaultextension='.png', initialdir=os.getcwd(), parent=img_win)
            if mess != '' and file != '' and file_im.get() != '' and out != '':
                try:
                    image_.encrypt_image(img_path=file, message=mess, new_path=out)
                    success.config(text='Successfully encrypted message in\n{}'.format(out))
                except FileNotFoundError:
                    image_.encrypt_image(img_path=file_im.get(), message=mess, new_path=out)
                    success.config(text='Successfully encrypted message in\n{}'.format(out))
            else:
                m.showerror('ERROR', 'Something went wrong try again')

        main_bu = Button(img_win, text='Encrypt Message', bg='grey', font=cas, command=done)
        main_bu.place(x=10, y=130)
        ho.CreateToolTip(main_bu, 'Checks everything and encrypts your data')

    def ex_img():
        """Data extracting function of audio steno"""
        global ex_file
        ex_win = Toplevel(root, bg='grey')
        ex_win.title('Image Steno-EXTRACT')
        ex_win.geometry('515x310')
        ex_win.wm_iconbitmap('images/l2.ico')
        ex_lb = Label(ex_win, text='Image -Steganography[EXTRACT]', bg='black', fg='white', font=cas_big)
        ex_lb.place(x=10, y=10)
        file_lb = Label(ex_win, text='Select File:', font=cas, bg='white', fg='black')
        file_lb.place(x=5, y=50)
        file_ex = Entry(ex_win, width=55, font=cas, relief='ridge')
        file_ex.place(x=7, y=75)
        file_ex.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global ex_file
            ex_file = askopenfilename(parent=ex_win, initialdir=os.getcwd(), title='Select File to ENCRYPT',
                                      filetypes=[('Image files', '.png')], defaultextension='.png')
            file_ex.delete(0, END)
            file_ex.insert(0, ex_file)
            file_lb.config(text='Selected File:')

        se_bu = Button(ex_win, text='Browse', bg='grey', font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def extract_data(event=None):
            """Extracts data from the audio file and shows it in a text box"""
            dat = image_.decrypt_image(img_path=ex_file)
            suc_lb = Label(ex_win, text='Hidden message is:', font=cas, fg='soft blue', bg='grey').place(x=6, y=130)
            sh = st.ScrolledText(ex_win, width=60, height=7, font=cas)
            sh.place(x=8, y=155)
            sh.insert(INSERT, dat)
            sh.config(state=DISABLED)

        ex_bu = Button(ex_win, text='Extract Message', bg='grey', font=cas, command=extract_data)
        ex_bu.place(x=10, y=100)
        ho.CreateToolTip(ex_bu, 'Extracts the hidden \ndata & displays it')
        ex_win.bind('<Return>', extract_data)

        qu_bu = Button(ex_win, text='Exit', font=cas, bg='grey', fg='soft blue', command=ex_win.destroy)
        qu_bu.place(x=467, y=278)
        ho.CreateToolTip(qu_bu, 'Exits window')

    bu_en = Button(img_win, text='Encrypt', font=cas, bg='black', fg='white', command=em_img)
    bu_en.place(x=70, y=220)
    ho.CreateToolTip(bu_en, 'Encrypts data in image file')
    bu_ex = Button(img_win, text='Extract', font=cas, bg='black', fg='white', command=ex_img)
    bu_ex.place(x=260, y=220)
    ho.CreateToolTip(bu_ex, 'Extracts data from image file')
    qubu = Button(img_win, text='Exit', font=cas, bg='black', fg='white', command=img_win.destroy)
    qubu.place(x=410, y=220)
    ho.CreateToolTip(qubu, 'Exits window')


def audio_steno():
    """Audio steganography functions"""
    aud_win = Toplevel(master=root, bg='white')
    aud_win.title('Audio Steganography')
    aud_win.geometry('515x260')
    aud_win.wm_iconbitmap('images/l2.ico')
    au_lb = Label(aud_win, text='Audio -Steganography', bg='white', fg='black', font=cas_big)
    au_lb.place(x=150, y=100)

    def em_aud():
        """Audio steno's encrypting function"""
        global file, mess
        select_lb = Label(aud_win, text='Select File:', font=cas, bg='grey', fg='#f20713')
        select_lb.place(x=5, y=50)
        file_au = Entry(aud_win, width=55, font=cas, relief='ridge')
        file_au.place(x=7, y=75)
        file_au.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global file
            file = askopenfilename(parent=aud_win, initialdir=os.getcwd(), title='Select File to ENCRYPT',
                                   filetypes=[('Audio files', '.wav')], defaultextension='.wav')
            file_au.delete(0, END)
            file_au.insert(0, file)
            select_lb.config(text='Selected File:')

        se_bu = Button(aud_win, text='Browse', bg='grey', font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def pan():
            """Opens message prompt to enter message"""
            global mess
            message = Toplevel(aud_win)
            message.title('Enter Message')
            message.resizable(False, False)
            message.wm_iconbitmap('images/l2.ico')
            lm = Label(message, text='Enter your message that you want to hide:', bg='grey', font=cas)
            lm.pack(side=TOP, fill=BOTH)
            ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
            t = st.ScrolledText(message)
            t.config(font=cas)
            t.pack()

            def click(event=None):
                """Collects the message entered by user"""
                global mess
                message.withdraw()
                mess = t.get("1.0", "end-1c")

            bm = Button(message, text='Done(Ctrl+b)', command=click, relief='flat', bg='grey', font=cas)
            bm.pack(side=BOTTOM, fill=BOTH)
            ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
            message.bind('<Control-b>', click)

        b = Button(aud_win, command=pan, text='Enter Message', font=cas, bg='grey')
        b.place(x=10, y=100)
        ho.CreateToolTip(b, 'Opens a prompt where you can enter message')
        success = Label(aud_win, bg='grey', font=cas)
        success.place(x=10, y=170)

        def done():
            """Main function which asks for saving file location and then encrypts the data in audio file"""
            global file, mess
            m.showinfo('Procedure', 'Where would you like the encrypted file to be saved?\n'
                                    'Select the path in the next window.')
            out = asksaveasfilename(title='Save your encrypted file as', filetypes=[('Audio File', '.wav')],
                                    defaultextension='.wav', initialdir=os.getcwd(), parent=aud_win)
            if mess != '' and file != '' and file_au.get() != '' and out != '':
                try:
                    aud.embed(infile=file, message=mess, outfile=out)
                    success.config(text='Successfully encrypted message in\n{}'.format(out))
                except FileNotFoundError:
                    aud.embed(infile=file_au.get(), message=mess, outfile=out)
                    success.config(text='Successfully encrypted message in\n{}'.format(out))
            else:
                m.showerror('ERROR', 'Something went wrong try again')

        main_bu = Button(aud_win, text='Encrypt Message', bg='soft blue', font=cas, command=done)
        main_bu.place(x=10, y=130)
        ho.CreateToolTip(main_bu, 'Checks everything and encrypts your data')

    def ex_aud():
        """Data extracting function of audio steno"""
        global ex_file
        ex_win = Toplevel(root, bg='white')
        ex_win.title('Audio Steno-EXTRACT')
        ex_win.geometry('515x310')
        ex_win.wm_iconbitmap('images/l2.ico')
        ex_lb = Label(ex_win, text='Audio -Steganography[EXTRACT]', bg='white', fg='black', font=cas_big)
        ex_lb.place(x=10, y=10)
        file_lb = Label(ex_win, text='Select File:', font=cas, bg='white', fg='black')
        file_lb.place(x=5, y=50)
        file_ex = Entry(ex_win, width=55, font=cas, relief='ridge')
        file_ex.place(x=7, y=75)
        file_ex.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global ex_file
            ex_file = askopenfilename(parent=ex_win, initialdir=os.getcwd(), title='Select File to ENCRYPT',
                                      filetypes=[('Audio files', '.wav')], defaultextension='.wav')
            file_ex.delete(0, END)
            file_ex.insert(0, ex_file)
            file_lb.config(text='Selected File:')

        se_bu = Button(ex_win, text='Browse', bg='grey', font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def extract_data(event=None):
            """Extracts data from the audio file and shows it in a text box"""
            dat = aud.extract(ex_file)
            suc_lb = Label(ex_win, text='Hidden message is:', font=cas, fg='soft blue', bg='grey').place(x=6, y=130)
            sh = st.ScrolledText(ex_win, width=60, height=7, font=cas)
            sh.place(x=8, y=155)
            sh.insert(INSERT, dat)
            sh.config(state=DISABLED)

        ex_bu = Button(ex_win, text='Extract Message', bg='grey', font=cas, command=extract_data)
        ex_bu.place(x=10, y=100)
        ho.CreateToolTip(ex_bu, 'Extracts the hidden \ndata & displays it')
        ex_win.bind('<Return>', extract_data)

        qu_bu = Button(ex_win, text='Exit', font=cas, bg='grey', fg='soft blue', command=ex_win.destroy)
        qu_bu.place(x=467, y=278)
        ho.CreateToolTip(qu_bu, 'Exits window')

    bu_en = Button(aud_win, text='Encrypt', font=cas, bg='black', fg='white', command=em_aud)
    bu_en.place(x=70, y=220)
    ho.CreateToolTip(bu_en, 'Encrypts data in audio file')
    bu_ex = Button(aud_win, text='Extract', font=cas, bg='black', fg='white', command=ex_aud)
    bu_ex.place(x=230, y=220)
    ho.CreateToolTip(bu_ex, 'Extracts data from audio file')
    qubu = Button(aud_win, text='Exit', font=cas, bg='black', fg='white', command=aud_win.destroy)
    qubu.place(x=410, y=220)
    ho.CreateToolTip(qubu, 'Exits window')


#

lb = Label(root, text="Steganography", font=('times newroman', 20), bg='white', fg='black')
lb.place(x=70, y=40)

image = Button(root, text='Image\nSteganography', relief='flat', bg='#A68064', command=image_steno, font=cas)
image.place(x=75, y=200)
ho.CreateToolTip(image, 'Click here\nto hide your\ndata in an image file')

audio = Button(root, text='Audio\nSteganography', relief='flat', bg='#A68064', command=audio_steno, font=cas)
audio.place(x=170, y=200)
ho.CreateToolTip(audio, 'Click here\nto hide data in\n an audio file.')

root.mainloop()
db.close()
