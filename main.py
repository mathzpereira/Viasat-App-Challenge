import tkinter as tk
from tkinter import font as tkfont
from funcoes import *

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Righteous', size=18)
        self.base_font = tkfont.Font(family='Righteous', size=13)
        self.title("AppChallenge")
        self.iconbitmap("./img/viasat.ico")

        width_janela = 1366
        height_janela = 768
        width_tela = self.winfo_screenwidth()
        height_tela = self.winfo_screenheight()
        pos_x = int((width_tela - width_janela) / 2)
        pos_y = int((height_tela - height_janela) / 2)

        self.geometry("{}x{}+{}+{}".format(width_janela, height_janela, pos_x, pos_y))

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (Home, Speed):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class Base(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(bg='white')
        
        #IMPORTANDO AS IMAGENS
        self.nav = tk.PhotoImage(file="./img/nav.png")
        self.home = tk.PhotoImage(file="./img/home.png")
        self.velocity = tk.PhotoImage(file="./img/velocity.png")
        self.total = tk.PhotoImage(file="./img/total.png")
        self.tipoTrafego = tk.PhotoImage(file="./img/tipoTrafego.png")
        self.download = tk.PhotoImage(file="./img/download.png")
        self.upload = tk.PhotoImage(file="./img/upload.png")
        self.apps = tk.PhotoImage(file="./img/apps.png")
        self.download_back = tk.PhotoImage(file="./img/download_back.png")
        self.upload_back = tk.PhotoImage(file="./img/upload_back.png")
        self.configuracoes = tk.PhotoImage(file="./img/configuracoes.png")
        self.dns = tk.PhotoImage(file="./img/dns.png")
        self.https = tk.PhotoImage(file="./img/https.png")
        self.ssdp = tk.PhotoImage(file="./img/ssdp.png")
        self.others = tk.PhotoImage(file="./img/others.png")
        self.viasat = tk.PhotoImage(file="./img/viasat.png")
        self.reload = tk.PhotoImage(file="./img/reload.png")

        #NAVBAR
        self.label = tk.Label(self, image=self.nav, bd=0, bg='#FFFFFF').place(x=0, y=200)
        self.home_button = tk.Button(self, image=self.home, bd=0, bg="#1A0547", activebackground='#1A0547', command=lambda:controller.show_frame("Home")).place(x=8, y=210)
        self.speed_button = tk.Button(self, image=self.velocity, bd=0, bg="#1A0547", activebackground='#1A0547', command=lambda:controller.show_frame("Speed")).place(x=8, y=375)
        self.label = tk.Label(self, image=self.viasat, bd=0, bg='#FFFFFF').place(x=40, y=40)


class Home(Base):
    def __init__(self, parent, controller):

        Base.__init__(self, parent, controller)
        controller.attributes()

        #TRAFEGO
        tk.Label(self, image=self.total, bd=0, bg='#FFFFFF').place(x=150, y=80)
        tk.Label(self, image=self.tipoTrafego, bd=0, bg='#FFFFFF').place(x=700, y=80)
        #DOWNLOADS
        tk.Label(self, image=self.download, bd=0, bg='#3C1A85').place( x=720, y=230)
        #UPLOADS
        tk.Label(self, image=self.upload, bd=0, bg='#311370').place( x=720, y=460)
        #DNS
        tk.Label(self, image=self.dns, bd=0, bg='#5228AC').place( x=920, y=230)
        #HTTPS
        tk.Label(self, image=self.https, bd=0, bg='#3C1A84').place( x=920, y=460)
        #SSDP
        tk.Label(self, image=self.ssdp, bd=0, bg='#5029A3').place( x=1120, y=230)
        #OTHERS
        tk.Label(self, image=self.others, bd=0, bg='#3D1B86').place( x=1120, y=460)
        
        graficosHome(self)
        
        def rodar():
            graficosHome(self)
        scheduler = BackgroundScheduler()
        scheduler.add_job(rodar, 'interval', seconds=3)
        scheduler.start()
        

class Speed(Base):

    def __init__(self, parent, controller):
        Base.__init__(self, parent, controller)

        #DOWNLOAD E UPLOAD
        tk.Label(self, image=self.download_back, bd=0, bg='#FFFFFF').place(x=150, y=80)
        tk.Label(self, image=self.upload_back, bd=0, bg='#FFFFFF').place(x=800, y=80)

        graficoSpeed(self)
        
        def rodar():
            graficoSpeed(self)
        scheduler = BackgroundScheduler()
        scheduler.add_job(rodar, 'interval', seconds=3)
        scheduler.start()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

