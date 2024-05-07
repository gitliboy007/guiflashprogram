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


file_path = ''
serial_io = serial.Serial(baudrate= 115200,bytesize=8, parity='N', stopbits=1, timeout=3)



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
        # 删除当前行的旧信息
        output_text.index
        if success > 1:
            # output_text.delete('1.0', tk.END)
            # output_text.delete('end - 2 lines linestart', 'end - 1 line linestart')
            current_line = output_text.index(tk.INSERT).split('.')[0]
            output_text.delete(f'{current_line}.0', f'{current_line}.end')

        # print(f"\n{task_index} - {task_name} {progress:.2f}% [{a}->{b}]{cost:.2f}s", end="")
        output_text.insert(tk.END, f"{task_index} - {task_name} {progress:.2f}% [{a}->{b}]{cost:.2f}s")
        output_text.update_idletasks()  # 强制Tkinter立即更新界面






def open_file():
    # 使用global关键字声明file_path为全局变量
    global file_path
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
    # 获取可用的串口列表
    ports = serial.tools.list_ports.comports()
    port_names = [port.device for port in ports]
    combo_var.set(port_names[0] if port_names else "请检查串口连接")
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



    # 获取要发送的文件的路径
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
    # print(f"Serial recv {serial_io.read(1)} ")   # 读取YModem的应答

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






root = tk.Tk()
# 设置窗口大小
root.geometry("700x512")
# 设置窗口标题
root.title("Flash Program")
file_path = tk.StringVar()

# 设置输入控件的长度为70
entry = tk.Entry(root, textvariable=file_path, width=70)
entry.grid(row=0, column=0, padx=(0, 20))


# 创建一个Text控件
output_text = tk.Text(root, height=30, width=95)
output_text.grid(row=2, column=0, columnspan=4, sticky='ew')


# 获取可用的串口列表
ports = serial.tools.list_ports.comports()
port_names = [port.device for port in ports]

# 创建下拉列表框
# 创建下拉列表框，设置默认值为串口列表的第一项
combo_var = tk.StringVar()
combo_var.set(port_names[0] if port_names else "请检查串口连接")
combo = tk.OptionMenu(root, combo_var, *port_names)
# combo = tk.OptionMenu(root, tk.StringVar(), *port_names)
# 使用grid方法将下拉列表框放置在窗体的左边
combo.grid(row=1, column=0,sticky='w')

scan_serial_button = tk.Button(root, text="Scan Serial", command=scan_serial)
# 使用grid方法将按钮放置在下拉列表框的右侧，距离100像素
scan_serial_button.grid(row=1, column=0,sticky='e', padx=(0, 320))

open_serial_button = tk.Button(root, text="Open Serial", command=open_serial)
# 使用grid方法将按钮放置在下拉列表框的右侧，距离100像素
open_serial_button.grid(row=1, column=0,sticky='e', padx=(0, 210))

open_button = tk.Button(root, text="Open File", command=open_file)
open_button.grid(row=0, column=2, padx=(0, 20))

burn_button = tk.Button(root, text="Burn File", command=burn_file)
burn_button.grid(row=0, column=3)



root.mainloop()