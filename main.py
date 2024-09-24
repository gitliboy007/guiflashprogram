#
import tkinter as tk
from tkinter import filedialog
import serial
import serial.tools.list_ports
import builtins
from ymodem.Socket import ModemSocket
from ymodem.Protocol import ProtocolType     

import logging
import math
import os
import time
from typing import Optional, Any, Union



import socket
import threading
import time
import struct
import psutil
import sys
import os

MCAST_ADDR = "224.1.1.1"
MCAST_PORT = 65000

MCAST_ADDR1 = "224.1.1.0"
MCAST_PORT1 = 65001


# 分隔符和缓冲区大小
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 2048  # 1024 bytes to keep things simple  4096

# 服务器的 IP 地址和端口
# host = "服务器的IP地址"
host = ""
port = 5001

s = None  # 定义全局套接字变量
is_tcp_burn_running = False  # 定义全局变量，用于指示是否正在进行TCP烧录




INTERFACE_IP = '192.168.0.12'  

ANY = "0.0.0.0"
# sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
# sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# # sock.bind((ANY,65000))
# sock.bind((INTERFACE_IP,65000))
# sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,255)
# sock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,socket.inet_aton(MCAST_ADDR)+socket.inet_aton(ANY))
#sock.setblocking(False)
# mreq = struct.pack("4sl", socket.inet_aton(MCAST_ADDR), socket.INADDR_ANY)
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


# sock1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
# sock1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# sock1.bind((ANY,65001))
# sock1.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,255)
# sock1.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,socket.inet_aton(MCAST_ADDR)+socket.inet_aton(ANY))
#sock1.setblocking(False)





global file_path
global a
global ip_address

ip_address = ''
file_path = ''
serial_io = serial.Serial(baudrate= 115200,bytesize=8, parity='N', stopbits=1, timeout=3)
a = 0


class TaskProgressBar:
    def __init__(self):
        self.bar_width = 50
        self.last_task_name = ""
        self.current_task_start_time = -1

    def show(self, task_index, task_name, total, success):
        if task_name != self.last_task_name:
            self.current_task_start_time = time.perf_counter()
            if self.last_task_name != "":
                print('\n', end="")
            self.last_task_name = task_name

        success_width = math.ceil(success * self.bar_width / total)

        a = "#" * success_width
        b = "." * (self.bar_width - success_width)
        progress = (success_width / self.bar_width) * 100
        cost = time.perf_counter() - self.current_task_start_time
       
        output_text.index
        if success > 1:
            # output_text.delete('1.0', tk.END)
            # output_text.delete('end - 2 lines linestart', 'end - 1 line linestart')
            current_line = output_text.index(tk.INSERT).split('.')[0]
            output_text.delete(f'{current_line}.0', f'{current_line}.end')

        # print(f"\n{task_index} - {task_name} {progress:.2f}% [{a}->{b}]{cost:.2f}s", end="")
        output_text.insert(tk.END, f"{task_index} - {task_name} {progress:.2f}% [{a}->{b}]{cost:.2f}s")
        output_text.update_idletasks()  # 强制Tkinter立即更新界面


def get_ethernet_ip():
    for interface, snics in psutil.net_if_addrs().items():
        print("Interface: ", interface)
        for snic in snics:
            if snic.family == socket.AF_INET:
                print("Interface: ", interface, "Address: ", snic.address)
            if snic.family == socket.AF_INET and '以太网' in interface:
                return snic.address
            if snic.family == socket.AF_INET and 'Ethernet' in interface:                
                return snic.address

ethernet_ip = get_ethernet_ip()
print("Ethernet IP: ", ethernet_ip)








sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
# sock.bind((ANY,65000))
sock.bind((ethernet_ip,65000))
sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,255)
sock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,socket.inet_aton(MCAST_ADDR)+socket.inet_aton(ANY))

hostname = socket.gethostname()
stop_thread = False
def recv_data():
    while True:
        if stop_thread:
           break
        data,address = sock.recvfrom(1024)
        # if address[0] == socket.gethostbyname(hostname):
        #     print(address)
        #     print(data)
        # if address[0] != socket.gethostbyname(hostname):
        if address[0] != ethernet_ip:            
            print(address)
            print(data)


t = threading.Thread(target = recv_data, daemon=True)
t.start()




def open_file():
    # 使用global关键字声明file_path为全局变量
    
    file_path = filedialog.askopenfilename()
    # file_path.set(filedialog.askopenfilename())
    # 设置Entry控件的内容为文件路径
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    if not file_path:
        print("No file selected.")
        return
    print(f"file_name is {file_path}")


def open_serial():
    global serial_io
    port = combo_var.get()
    print(f"Opening serial port {port}...")
    serial_io = serial.Serial(port, 115200,8,"N",1,timeout=3)
    if serial_io.is_open:
        print(f"Serial port {port} is open.")
    else:
        print(f"Failed to open serial port {port}.")

def scan_serial():
    # 获取可用的串口列�??
    ports = serial.tools.list_ports.comports()
    port_names = [port.device for port in ports]
    combo_var.set(port_names[0] if port_names else "请检查串口连�??")
    combo = tk.OptionMenu(root, combo_var, *port_names)
    print(f"Scanning serial port {port_names}...")

class OutputRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

# 重定义print函数，将其输出重定向到Text控件
def print(*args, **kwargs):
    kwargs['file'] = OutputRedirector(output_text)
    builtins.print(*args, **kwargs)




# global num 
# global a 
# global data3 
# global data2 
# global data4 


def Udp_burn1():
    num = 1
   
    global a, data2, data3, data4  # 声明要使用的全局变量
    data2 = "Reset"
    data3 = "Erase"
    data4 = "SendOver"
    a = "b"
    file_path = entry.get()
    if not file_path:
        print("No file selected.")
        global is_udp_burn_running
        is_udp_burn_running = False
        return


    # file1 = open("LWIP_MULTICAST.bin","rb")
    file1 = open(file_path,"rb")
    sock.sendto(data2.encode("utf-8"),(MCAST_ADDR,MCAST_PORT))

    print("send  reset command! waiting 22s!!!")
    
    # time.sleep(22)
    for i in range(1, 23):
        
        print(f"等待 {23-i} �?")  # 使用f-string进行字符串格式化
        time.sleep(1)
        # 获取总行�?
        total_lines = int(output_text.index('end-1c').split('.')[0])
        
        # 删除最后一�?
        output_text.delete(f"{total_lines-1}.0", f"{total_lines}.end")

    sock.sendto(data3.encode("utf-8"),(MCAST_ADDR,MCAST_PORT))  #erase
    print("send  Erase command! waiting 3s!!!")
    for i in range(1, 4):
        print(f"等待 {4-i} �?")  # 使用f-string进行字符串格式化
        time.sleep(1)
        # 获取总行�?
        total_lines = int(output_text.index('end-1c').split('.')[0])
        
        # 删除最后一�?
        output_text.delete(f"{total_lines-1}.0", f"{total_lines}.end")

    while True:
        # data,address = sock.recvfrom(1024)
        # print(address)
        # print(data)


        #data1 = "hello,this is a multicast message!"
        data1 = file1.read(512)
        # file1.seek(0,0)
        if not data1:       
            sock.sendto(data4.encode("utf-8"),(MCAST_ADDR,MCAST_PORT))
            print("send  end!!!")
            break
        # print(data1)
        data1 = a.encode() + num.to_bytes(4,"big") + data1
        
        # print("%d",num)
        sock.sendto(data1,(MCAST_ADDR,MCAST_PORT))
        # sock1.sendto(data1, (MCAST_ADDR1, MCAST_PORT1))

        print(f"send to {MCAST_ADDR }:{MCAST_PORT} at {time.strftime('%Y-%m-%d %H %M %S',time.localtime())}--{num}")
        num += 1
        time.sleep(0.2)
    num = 0
    while True:
        data2 = "hello,this is a multicast message!"
        sock.sendto(data2.encode(), (MCAST_ADDR, MCAST_PORT))
        num+=1
        if num > 20:
            break
        time.sleep(0.5)

    stop_thread = True
    t.join()  
    sock.close()
    print("send  over!!!")
    file1.close()
    # sys.exit()
    # sock1.close()
    # global is_udp_burn_running
    is_udp_burn_running = False


def Udp_burn():
    global is_udp_burn_running
    if is_udp_burn_running:
        print("udp_burn is already running.")
        return
    is_udp_burn_running = True



    # 创建一个线程对象，目标函数是Udp_burn
    udp_burn_thread = threading.Thread(target=Udp_burn1, daemon=True)

    # 启动线程
    udp_burn_thread.start()
    # （可选）如果你需要在主线程中等待这个线程完成，可以取消注释下面的�?
    # udp_burn_thread.join()

is_udp_burn_running = False

def link_server1(host, port, max_retries=5):
    # 创建 TCP 套接字
    global s  # 声明 s 为全局变量
    s = socket.socket()
    retry_count = 0

    while retry_count < max_retries:
        try:
            print(f"[+] 连接到 {host}:{port}")
            s.connect((host, port))
            print("[+] 连接成功")
            return s  # 成功连接后返回套接字
        except socket.error as e:
            print(f"连接失败: {e}")
            retry_count += 1
            print(f"重试 {retry_count}/{max_retries} 次...")
            time.sleep(2)  # 等待一段时间后重试

    print("[-] 无法连接到服务器")
    return None  # 如果超过最大重试次数，返回 None

def link_server():  
    global a
    # host = "192.168.1.100"
    host = entryip.get()
    if not host:
        print("+ No ip_address input. please input ip_address.")
        global is_tcp_burn_running
        is_tcp_burn_running = False
        a = 0
        return
    if a:
        print("link_server is already running.")
        return
    socket = link_server1(host, port)
    if socket:
        # 继续进行数据传输等操作
        a = 1
        pass
    else:
        # 处理连接失败的情况
        a = 0
        pass

def Tcp_burn1():
    num = 1
   
    global a, data2, data3, data4 ,s # 声明要使用的全局变量
    data2 = "Reset"
    data3 = "Erase"
    data4 = "SendOver"
    a = "b"
    file_path = entry.get()
    if not file_path:
        print("No file selected.")
        global is_tcp_burn_running
        is_tcp_burn_running = False
        return


    # file1 = open("LWIP_MULTICAST.bin","rb")
    file1 = open(file_path,"rb")
    # 要发送的文件
    filename = file_path
    filesize = os.path.getsize(filename)
    

    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # 发送文件内容
    with open(filename, "rb") as f:
        while True:
            # 读取文件中的数据
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            # 发送数据
            try:
                s.sendall(bytes_read)
            except socket.error as e:
                print(f"发送数据时出错: {e}")
                s.close()
                file1.close()
                is_tcp_burn_running = False
                break

    # 关闭套接字

    print("[+] 发送完成！")
    stop_thread1 = True
    #t.join()  
    s.close()
    a = 0
    #print("send  over!!!")
    file1.close()
    # sys.exit()
    # sock1.close()
    # global is_tcp_burn_running
    is_tcp_burn_running = False




def Tcp_burn():
    global is_tcp_burn_running
    if is_tcp_burn_running:
        print("tcp_burn is already running.")
        return
    is_tcp_burn_running = True

    if not a:
        print("eathrnet is not connected please connect first")
        is_tcp_burn_running = False
        return

    # 创建一个线程对象，目标函数是tcp_burn
    tcp_burn_thread = threading.Thread(target=Tcp_burn1, daemon=True)

    # 启动线程
    tcp_burn_thread.start()
    # （可选）如果你需要在主线程中等待这个线程完成，可以取消注释下面的�?
    # tcp_burn_thread.join()

is_tcp_burn_running = False










# logging.basicConfig(level=logging.DEBUG, format='%(message)s')

 # implementation

def burn_file():
      # 使用global关键字声明file_path为全局变量
    global file_path
    global serial_io
    # def read(size, timeout = 3):
    #     global serial_io
    #     serial_io.timeout = timeout
    #     return serial_io.read(size)
    # # implementation

    # # define write
    # def write(data, timeout = 3):
    #     global serial_io
    #     serial_io.write_timeout = timeout
    #     serial_io.write(data)
    #     serial_io.flush()
    #     return
   
    # serial_io = serial.Serial("COM4", 115200,8,"N",1,timeout=3)

    def read(size: int, timeout: Optional[float] = 3) -> Any:
        global serial_io
        serial_io.timeout = timeout
        return serial_io.read(size)

    def write(data: Union[bytes, bytearray], timeout: Optional[float] = 3) -> Any:
        global serial_io
        serial_io.write_timeout = timeout
        serial_io.write(data)
        serial_io.flush()
        return



    # 获取要发送的文件的路�??
    file_path = entry.get()
    if not file_path:
        print("No file selected.")
        return

    # 打开串口
    port = combo_var.get()
    serial_io.close()
    if serial_io.is_open:
        output_text.insert(tk.END,f"Serial port {port} is already open.")
        output_text.update_idletasks()  # 强制Tkinter立即更新界面
    else:
        serial_io = serial.Serial(port, 115200,8,"N",1,timeout=3)
    if not serial_io.is_open:
        print(f"Failed to open serial port {port}.")
        return
    else:
        output_text.insert(tk.END,f"Serial port {port} is open.")
        output_text.update_idletasks()  # 强制Tkinter立即更新界面


   

    # serial_io.write(b'\x18')  # 发送Ctrl+X，进入YModem模式
    # serial_io.write(b'\x19')  # 发送Ctrl+X，进入YModem模式
    # serial_io.write(b'\x17')  # 发送Ctrl+X，进入YModem模式
    # serial_io.write(b'\x16')  # 发送Ctrl+X，进入YModem模式
    # print(f"Serial recv {serial_io.read(1)} ")   # 读取YModem的应�??

    # socket_args = {
    #     'packet_size':  1024,
    #     'protocol_type':  ProtocolType.YMODEM,
    #     'protocol_type_options': ['YMODEM-G-1K'] 
    # }
    socket_args = {
        'packet_size': 128,
        'protocol_type':  ProtocolType.YMODEM,
        'protocol_type_options': [] 
    }

    # 创建一个YModem对象
    ymodem_obj = ModemSocket(read, write, **socket_args)    
    # create socket
    
    # bn = os.path.basename(file_path)
    # filesize = os.stat(file_path).st_size
    # strSendFileCMD = "AFF " + str(filesize) + " " + bn + "\n"

    # serial_io.write(strSendFileCMD.encode())

    progress_bar = TaskProgressBar()
    
    output_text.insert(tk.END,f"\nSending file {file_path}...")
    output_text.insert(tk.END,"\nWaiting for response .....")
    output_text.update_idletasks()  # 强制Tkinter立即更新界面
    with open(file_path, 'rb') as file: 
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_path = [file_path]
        
        # result = ymodem_obj.send(os.path.abspath(file_path), progress_bar.show)
        result = ymodem_obj.send(file_path,progress_bar.show)
    if result:
        print("File sent successfully.")
    else:
        print("Failed to send file.")

    # 关闭串口
    serial_io.close()


def on_closing():
    # 在这里执行任何必要的清理工作
    print("应用程序正在关闭")
    root.destroy()



root = tk.Tk()
# 设置窗口大小
root.geometry("700x512")
# 设置窗口标题
root.title("Flash Program Ver 1.0")
file_path = tk.StringVar()

# 设置输入控件的长度为70
entry = tk.Entry(root, textvariable=file_path, width=70)
entry.grid(row=0, column=0, padx=(0, 20))




# 创建一个Text控件
output_text = tk.Text(root, height=30, width=95)
output_text.grid(row=2, column=0, columnspan=4, sticky='ew')


# 获取可用的串口列�??
ports = serial.tools.list_ports.comports()
port_names = [port.device for port in ports]

# 创建下拉列表�??
# 创建下拉列表框，设置默认值为串口列表的第一�??
combo_var = tk.StringVar()
combo_var.set(port_names[0] if port_names else "请检查串口连�??")
combo = tk.OptionMenu(root, combo_var, *port_names)
# combo = tk.OptionMenu(root, tk.StringVar(), *port_names)
# 使用grid方法将下拉列表框放置在窗体的左边
combo.grid(row=1, column=0,sticky='w')

scan_serial_button = tk.Button(root, text="Scan Serial", command=scan_serial)
# 使用grid方法将按钮放置在下拉列表框的右侧，距�??100像素
scan_serial_button.grid(row=1, column=0,sticky='e', padx=(0, 320))

open_serial_button = tk.Button(root, text="Open Serial", command=open_serial)
# 使用grid方法将按钮放置在下拉列表框的右侧，距�??100像素
open_serial_button.grid(row=1, column=0,sticky='e', padx=(0, 210))

entryip = tk.Entry(root, textvariable=ip_address, width=15)
entryip.grid(row=1, column=0,sticky='e', padx=(0, 80))

burn_button = tk.Button(root, text="link server", command=link_server)
burn_button.grid(row=1, column=0,sticky='e', padx=(0, 0))


open_button = tk.Button(root, text="Open File", command=open_file)
open_button.grid(row=0, column=2, padx=(0, 20))

burn_button = tk.Button(root, text="ComBurn File", command=burn_file)
burn_button.grid(row=0, column=3)

burn_button1 = tk.Button(root, text="UDPBurn File", command=Udp_burn)
burn_button1.grid(row=1, column=3)

burn_button2 = tk.Button(root, text="TCPBurn File", command=Tcp_burn)
burn_button2.grid(row=1, column=2)

output_text.insert(tk.END, f"Ethernet IP: {ethernet_ip}")
# 绑定关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)


root.mainloop()