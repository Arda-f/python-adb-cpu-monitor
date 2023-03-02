from tkinter import *
import tkinter.ttk as ttk
import threading
from subprocess import *
from time import sleep

adb = ".\\platform-tools\\adb.exe"

class Events:

    def start():
        control_devices = ""
        while True:
            devices = getoutput( adb + " devices")
            if control_devices != devices:
                control_devices = devices
                if list_devices.get_children():
                    for value in list_devices.get_children():
                        list_devices.item(item=value,values=" ")
                devices = devices.splitlines()
                devices.reverse()
                for device in devices:
                    if device.startswith("List") == False:
                        value = device.split("\t")
                        value.insert(2,getoutput( adb + " -s " + value[0] + " shell getprop ro.product.model"))
                        list_devices.insert('',0,values=value)

    def battery():
        control_level = ""
        while True:
            level = getoutput( adb + " -s " + tk.title + " shell dumpsys battery | findstr /r /c:level")
            level = level.strip()
            if level.split(":")[1].strip() != control_level:
                label_charge_per.config(text=level.split(":")[1].strip() + "%")
                control_level = level.split(":")[1].strip()
            control_AC = ""
            AC = getoutput( adb + " -s " + tk.title + " shell dumpsys battery | findstr /r /c:AC")
            AC = AC.strip()
            if AC.split(":")[1].strip() != control_AC:
                label_AC_stat.config(text=AC.split(":")[1].strip())
                control_AC = AC.split(":")[1].strip()
            control_USB = ""
            USB = getoutput( adb + " -s " + tk.title + " shell dumpsys battery | findstr /r /c:USB")
            USB = USB.strip()
            if USB.split(":")[1].strip() != control_USB:
                label_USB_stat.config(text=USB.split(":")[1].strip())
                control_USB = USB.split(":")[1].strip()

    def cpuinfo():
        # if label_device.cget("text") != "adb.exe: device '" + tk.title + "' not found":
            for i in range(200):
                listView_cpu.insert("",i,values="") 
            
            control_cpu = ""
            while True:
                cpu = getoutput( adb + " -s " + tk.title + " shell dumpsys cpuinfo")
                cpu_list = cpu.splitlines()
                cpu_list[0] = ""
                cpu_list[1] = ""
                if control_cpu != cpu_list:
                    control_cpu = cpu_list
                    for i in range(len(cpu_list)):
                        control = cpu_list[i].strip()
                        if control != "":
                            children = listView_cpu.get_children()
                            value = cpu_list[i]
                            value = value.strip()
                            value = value.split("/")
                            value[0] = value[0].split(" ")[0]
                            if len(value) > 1:
                                value[1] = value[1].split(":")[0]
                            listView_cpu.item(item=children[i - 2],values=value)
                    
    def threads():
        charge_thread = threading.Thread(target=Events.battery)
        charge_thread.daemon = True 
        charge_thread.start()

        # AC_thread = threading.Thread(target=Events.AC)
        # AC_thread.daemon = True
        # AC_thread.start()

        # USB_thread = threading.Thread(target=Events.USB)
        # USB_thread.daemon = True
        # USB_thread.start()

        cpu_thread = threading.Thread(target=Events.cpuinfo)
        cpu_thread.daemon = True
        cpu_thread.start()


tk = Tk()

def selectedItem(a):
    item = list_devices.item(item=list_devices.selection())
    if item["values"]:
        tk.title = item["values"][0]
        Events.threads()

# button1 = Button(tk,text="Ram Bilgileri", command=EventListeners.ekle)
# button1.grid(row=1,column=1)

# button2 = Button(tk,text="Hesaplar", command=EventListeners.hesaplar)
# button2.grid(row=1,column=2)

list_devices = ttk.Treeview(
    tk, 
    height=5,
    column=("device_id","status","model"),
    show="headings"
    )

list_devices.heading(column="device_id",text="Device İd")
list_devices.heading(column="status",text="Status")
list_devices.heading(column="model",text="Phone Name")

# list_devices.column(column="device_id",width=110)
# list_devices.column(column="status",width=50)
# list_devices.column(column="model",width=80)

list_devices.grid(row=1,column=0,columnspan=3)

list_devices.bind("<<TreeviewSelect>>", selectedItem)

# button_device = ttk.Button(tk, text="Listele")
# button_device.grid(row=1, column=1)

label_device = ttk.Label(tk)
label_device.grid(row=1,column=3)

label_charge = ttk.Label(tk,text="Güncel Şarj: ")
label_charge.grid(row=2,column=0)

label_charge_per = ttk.Label(tk,text="0%")
label_charge_per.grid(row=2,column=1)

label_AC = ttk.Label(tk, text="AC powered: ")
label_AC.grid(row=3,column=0)

label_AC_stat = ttk.Label(tk, text="")
label_AC_stat.grid(row=3,column=1)

label_USB = ttk.Label(tk, text="USB powered: ")
label_USB.grid(row=4,column=0)

label_USB_stat = ttk.Label(tk, text="")
label_USB_stat.grid(row=4,column=1)

listView_cpu = ttk.Treeview(
    tk,
    columns=("percent","package_name","details"),
    show="headings",
    height=15,
    )
# Add Column
listView_cpu.heading(column="percent",text="Percent")
listView_cpu.heading(column="package_name",text="Package Names")
listView_cpu.heading(column="details",text="Details")
# Set Column Width
listView_cpu.column(column="percent", width=50)
listView_cpu.column(column="package_name", width=300)
listView_cpu.column(column="details", width=100)
listView_cpu.grid(columnspan=3)

start_thread = threading.Thread(target=Events.start)
start_thread.daemon = True 
start_thread.start()

tk.mainloop()