from tkinter import *
import socket
import json
import re
import subprocess
import threading
from tkinter import messagebox
from apscheduler.schedulers.background import BackgroundScheduler

def run():

    def executar_programa1():
        subprocess.run(['python', "./funcoes/traffic_analyzer.py"])
    
    def executar_programa2():
        subprocess.run(['python', './main.py'])
    
    # Cria as threads para executar os programas
    thread1 = threading.Thread(target=executar_programa1)
    thread2 = threading.Thread(target=executar_programa2)
    
    # Inicia as threads
    thread1.start()
    thread2.start()
    
    # Aguarda as threads terminarem
    thread1.join()
    thread2.join()

    print("Programas finalizados.")


def graficosHome(self):
    data = handle_socket_connection(50001)
    if data != None:
        #TRAFEGO
        total = 500
        trafego = (data['total']/(total+0.000000000000000000000000000001))*100
        if data['total']/total <= 1:
            createPieChart(self,[100-trafego, trafego],["#1C064A","#9664FF"],310,310,200,200)
        Ttext = Label(self, text=str(total)+".00 MB",font="Ebrima 12 bold",bg="white",fg="#341575")
        Ttext.place(x=365,y=530)
        Ttltext = Label(self, text=str(data['total'])+" MB", width = 10, font="Ebrima 12 bold",bg="white",fg="#9664FF")
        Ttltext.place(x=355,y=550)
        #DOWNLOADS
        download = (data['download']/(data['total']+0.00000000000000000000000001))*100
        if download <= 1:
            createPieChart(self,[99.99, 0.01],["#1C064A","#9664FF"],750,280,120,120)
        else:
            createPieChart(self,[100-download, download],["#9664FF","#1C064A"],750,280,120,120)
        Dtext = Label(self, text=str(data['download'])+" MB", width = 10,font="Ebrima 12 bold",bg="white",fg="#341575")
        Dtext.place(x=750,y=400)
        #UPLOADS
        upload = (data['upload']/(data['total']+0.00000000000000000000000001))*100
        if upload <= 1:
            createPieChart(self,[99.99, 0.01],["#1C064A","#9664FF"],750,510,120,120)
        else:
            createPieChart(self,[100-upload, upload],["#9664FF","#1C064A"],750,510,120,120)
        Utext = Label(self, text=str(data['upload'])+" MB", width = 10,font="Ebrima 12 bold",bg="white",fg="#341575")
        Utext.place(x=750,y=630)
        #DNS
        dns = (data['domain']/(data['total']+0.00000000000000000000000001))*100
        if dns <= 5:
            createPieChart(self,[99.99, 0.01],["#1C064A","#9664FF"],950,280,120,120)
        else:
            createPieChart(self,[100-dns, dns],["#9664FF","#1C064A"],950,280,120,120)
        DNStext = Label(self, text=str(data['domain'])+" MB", width = 10,font="Ebrima 12 bold",bg="white",fg="#341575")
        DNStext.place(x=960,y=400)
        #HTTPS
        https = (data['https']/(data['total']+0.00000000000000000000000001))*100
        if https <= 5:
            createPieChart(self,[99.99, 0.01],["#1C064A","#9664FF"],950,510,120,120)
        else:
            createPieChart(self,[100-https, https],["#9664FF","#1C064A"],950,510,120,120)
        Htext = Label(self, text=str(data['https'])+" MB", width = 10,font="Ebrima 12 bold",bg="white",fg="#341575")
        Htext.place(x=960,y=630)
        #SSDP
        ssdp = (data['ssdp']/(data['total']+0.00000000000000000000000001))*100
        if ssdp <= 5:
            createPieChart(self,[99.99, 0.01],["#1C064A","#9664FF"],1150,280,120,120)
        else:
            createPieChart(self,[100-ssdp, ssdp],["#9664FF","#1C064A"],1150,280,120,120)
        Stext = Label(self, text=str(data['ssdp'])+" MB", width = 10,font="Ebrima 12 bold",bg="white",fg="#341575")
        Stext.place(x=1160,y=400)
        #OTHERS
        others = (data['others']/(data['total']+0.00000000000000000000000001))*100
        if others <= 5:
            createPieChart(self,[99.99, 0.01],["#1C064A","#9664FF"],1150,510,120,120)
        else:
            createPieChart(self,[100-others, others],["#9664FF","#1C064A"],1150,510,120,120)
        Otext = Label(self, text=str(data['others'])+" MB", width = 10,font="Ebrima 12 bold",bg="white",fg="#341575")
        Otext.place(x=1160,y=630)
    else:
        messagebox.showinfo("Erro", "Habilite o package tracer ou espere a chegada de dados.")

def graficoSpeed(self):
    data = handle_socket_connection(50000)
    
    if hasattr(self,'Dntext'):
            Dntext.destroy()
    if hasattr(self,'Uptext'):
            Uptext.destroy()

    Dntext = Label(self, text=str(data['download_speed'])+" MB/s", width = 10,font="Ebrima 20 bold",bg="white",fg="#341575")
    Dntext.place(x=320,y=400)
    Uptext = Label(self, text=str(data['upload_speed'])+" MB/s", width = 10,font="Ebrima 20 bold",bg="white",fg="#341575")
    Uptext.place(x=970,y=400)
        
        


def createPieChart(self, PieV, colV, x, y, width, height):
    if hasattr(self, 'canvas'):
        self.canvas.destroy()

    canvas = Canvas(self,width=width,height=height,bg='#FFFFFF',highlightbackground='#FFFFFF')
    canvas.place(x=x,y=y)
    st = 0
    coord = 0, 0, width, height
    for val,col in zip(PieV,colV):    
        canvas.create_arc(coord,start=st,extent = val*3.6,fill=col,outline=col)
        st = st + val*3.6 


def convert_size_to_bytes(size_str):
    size_str = size_str.upper()
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4, "PB": 1024**5}
    pattern = re.compile(r'(\d*\.?\d+)([a-zA-Z]+)')
    match = pattern.match(size_str)

    if not match:
        raise ValueError("Tamanho inválido")

    size = float(match.group(1))
    unit = match.group(2)

    if unit not in units:
        raise ValueError("Unidade inválida")

    return float((size * units[unit])/1024**2)

def handle_socket_connection(port):

    if port == 50001:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', port))

                while True:
                    data = s.recv(500000)
                    if not data:
                        break
                    data_received = data.decode()[1:].replace('\\','').replace('\n','').replace("'",'')
                    json_data = json.loads(data_received)
                    https=domain =ssdp=others=download=upload =0
                    try:
                        download += convert_size_to_bytes(json_data["https"]["download"])
                    except:
                        download += 0

                    try:
                        download += convert_size_to_bytes(json_data["domain"]["download"])
                    except:
                        download += 0

                    try:
                        download += convert_size_to_bytes(json_data["ssdp"]["download"])
                    except:
                        download += 0

                    try:
                        download += convert_size_to_bytes(json_data["others"]["download"])
                    except:
                        download += 0

                    try:
                        upload += convert_size_to_bytes(json_data["https"]["upload"])
                    except:
                        upload += 0

                    try:
                        upload += convert_size_to_bytes(json_data["domain"]["upload"])
                    except:
                        upload += 0
                    
                    try:
                        upload += convert_size_to_bytes(json_data["ssdp"]["upload"])
                    except:
                        upload += 0
                    
                    try:
                        upload += convert_size_to_bytes(json_data["others"]["upload"])
                    except:
                        upload += 0

                    try:
                        https = convert_size_to_bytes(json_data["https"]["total"])
                    except:
                        https += 0

                    try:
                        domain = convert_size_to_bytes(json_data["domain"]["total"])
                    except:
                        domain += 0

                    try:
                        ssdp =  convert_size_to_bytes(json_data["ssdp"]["total"])
                    except:
                        ssdp += 0

                    try:
                        others = convert_size_to_bytes(json_data["others"]["total"])
                    except:
                        others += 0

                    values = {
                        'https': round(https,3),
                        'domain': round(domain,3),
                        'ssdp': round(ssdp,3),
                        'others': round(others,3),
                        'upload': round(upload,3),
                        'download': round(download,3),
                        'total': round(round(download,3)+round(upload,3),3)
                    }

                    return values
                
        except Exception as e:
            print(f"Erro na porta{e}")
    elif port == 50000:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', port))

                while True:
                    data = s.recv(500000)
                    if not data:
                        break
                    data_received = data.decode()[1:].replace('\\','').replace('\n','').replace("'",'')
                    json_data = json.loads(data_received)
                    download_speed = upload_speed = 0
                    for pid in json_data:
                        try:
                            download_speed += convert_size_to_bytes(json_data[pid]["download_speed"])
                        except:
                            download_speed += 0
                        try:
                            upload_speed += convert_size_to_bytes(json_data[pid]["upload_speed"])
                        except:
                            upload_speed += 0
                    values = {
                        'upload_speed': round(download_speed,3),
                        'download_speed': round(upload_speed,3)
                    }

                    return values
                        
        except Exception as e:
            print(f"Erro na porta{e}")