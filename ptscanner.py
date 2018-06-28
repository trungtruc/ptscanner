from winreg import*
import os
from tkinter import *
import tkinter.filedialog
from tkinter import ttk
from tkinter import messagebox
import psutil

#gloabal variables
first_dict = {}
second_dict = {}
var = 0
path = ""
first_process = {}
second_process = {}


#folder dialog
def OpenDir ():
    window.directory = tkinter.filedialog.askdirectory()
    return window.directory

#file dialog
def OpenFile():
    window.filename = tkinter.filedialog.askopenfilename()
    return window.filename

# Cac root key
hives = {
    "HKEY_CLASSES_ROOT" : HKEY_CLASSES_ROOT,
    "HKEY_CURRENT_USER" : HKEY_CURRENT_USER,
    "HKEY_LOCAL_MACHINE" : HKEY_LOCAL_MACHINE,
    "HKEY_USERS" : HKEY_USERS,
    "HKEY_CURRENT_CONFIG" : HKEY_CURRENT_CONFIG
}

# Parse key name
def ParseKey(key):
    parts = key.split("\\")
    root_hive_name = parts[0]
    root_hive = hives.get(root_hive_name)
    partial_key = "\\".join(parts[1:])

    if not root_hive:
        raise Exception('root hive "{}" was not found'.format(root_hive_name))

    return partial_key, root_hive



def GetSubkey(key):
    partical_key, root_hive = ParseKey(key)

    with ConnectRegistry(None, root_hive) as reg:
        with OpenKey(reg, partical_key) as key_object:
            numbers_subkeys = QueryInfoKey(key_object)[0]
            try:
                for count in range(numbers_subkeys):
                    subkey_name = EnumKey(key_object, count)
                    yield subkey_name
            except:
                pass


def GetValue(key):
    partical_key, root_hive = ParseKey(key)
    data = []
    try:
        with ConnectRegistry(None, root_hive) as reg:
            with OpenKey(reg, partical_key) as key_object:
                numbers_value = QueryInfoKey(key_object)[1]
                try:
                    for count in range(numbers_value):
                        name = EnumValue(key_object, count)[0:2]
                        data.append(name)
                except:
                    pass
    except:
        pass
    return data


def join(path, *paths):
    path = path.strip('/\\')
    paths = map(lambda x: x.strip('/\\'), paths)
    paths = list(paths)
    result = os.path.join(path, *paths)
    result = result.replace('/', '\\')
    return result


def GetPath(key):
    key_level1 = key
    partical_key, root_hive = ParseKey(key_level1)
    path = []
    path.append(key_level1)
    with ConnectRegistry(None, root_hive) as reg:
        try:
            with OpenKey(reg, partical_key) as key_object:
                numbers_subkey = QueryInfoKey(key_object)[0]
                if numbers_subkey:
                    for count in range(numbers_subkey):
                        level2 = EnumKey(key_object, count)
                        key_level2 = key_level1 + "\\" + level2
                        path.append(key_level2)
                        partical_key, root_hive = ParseKey(key_level2)
                        try:
                            with OpenKey(reg, partical_key) as key_object_level3:
                                numbers_subkey = QueryInfoKey(key_object_level3)[0]
                                if numbers_subkey:
                                    for count in range(numbers_subkey):
                                        level3 = EnumKey(key_object_level3, count)
                                        key_level3 = key_level2 + "\\" + level3
                                        path.append(key_level3)
                                        partical_key, root_hive = ParseKey(key_level3)
                                        try:
                                            with OpenKey(reg, partical_key) as key_object_level4:
                                                numbers_subkey = QueryInfoKey(key_object_level4)[0]
                                                if numbers_subkey:
                                                    for count in range(numbers_subkey):
                                                        level4 = EnumKey(key_object_level4, count)
                                                        key_level4 = key_level3 + "\\" + level4
                                                        path.append(key_level4)
                                                        partical_key, root_hive = ParseKey(key_level4)
                                                        try:
                                                            with OpenKey(reg, partical_key) as key_object_level5:
                                                                numbers_subkey = QueryInfoKey(key_object_level5)[0]
                                                                if numbers_subkey:
                                                                    for count in range(numbers_subkey):
                                                                        level5 = EnumKey(key_object_level5, count)
                                                                        key_level5 = key_level4 + "\\" + level5
                                                                        path.append(key_level5)
                                                                        partical_key, root_hive = ParseKey(key_level5)
                                                                        try:
                                                                            with OpenKey(reg, partical_key) as key_object_level6:
                                                                                numbers_subkey = QueryInfoKey(key_object_level6)[0]
                                                                                if numbers_subkey:
                                                                                    for count in range(numbers_subkey):
                                                                                        level6 = EnumKey(key_object_level6, count)
                                                                                        key_level6 = key_level5 + "\\" + level6
                                                                                        path.append(key_level6)
                                                                                        partical_key, root_hive = ParseKey(key_level6)
                                                                                        
                                                                                        with OpenKey(reg, partical_key) as key_object_level7:
                                                                                            numbers_subkey = QueryInfoKey(key_object_level7)[0]
                                                                                            if numbers_subkey:
                                                                                                for count in range(numbers_subkey):
                                                                                                    level7 = EnumKey(key_object_level7, count)
                                                                                                    key_level7 = key_level6 + "\\" + level7
                                                                                                    path.append(key_level7)
                                                                                                    partical_key, root_hive = ParseKey(key_level7)
                                                                                                    with OpenKey(reg, partical_key) as key_object_level8:
                                                                                                        numbers_subkey = QueryInfoKey(key_object_level8)[0]
                                                                                                        if numbers_subkey:
                                                                                                            for count in range(numbers_subkey):
                                                                                                                level8 = EnumKey(key_object_level8, count)
                                                                                                                key_level8 = key_level7 + "\\" + level8
                                                                                                                path.append(key_level8)
                                                                                        
                                                                        except:
                                                                            pass
                                                        except:
                                                            pass
                                        except:
                                            pass
                        except:
                            pass
        except:
            pass                               
    return path



def takesnapshot(order):
    if order == "first":
        global first_dict
        first_dict = {}
    if order == "second":
        global second_dict
        second_dict = {}
    if str(mode.get()) == "registry":
        allkey = []            
        key = []
        count = 0
        root = [HKEY_CLASSES_ROOT, HKEY_CURRENT_CONFIG, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, HKEY_USERS]
        openkey = ConnectRegistry(None, HKEY_CLASSES_ROOT)
        num = QueryInfoKey(openkey)[0]
        for i in range(num):
            subkey = EnumKey(openkey, i)
            count = count + 1
            key.append(subkey)
        CloseKey(openkey)
        for i in range(num):
            allkey.append('HKEY_CLASSES_ROOT\\' + key[i]) 


        key = []
        openkey = ConnectRegistry(None, HKEY_CURRENT_CONFIG)
        num = QueryInfoKey(openkey)[0]
        for i in range(num):
            subkey = EnumKey(openkey, i)
            count = count + 1
            key.append(subkey)
        CloseKey(openkey)
        for i in range(num):
            allkey.append('HKEY_CURRENT_CONFIG\\' + key[i]) 


        key = []
        openkey = ConnectRegistry(None, HKEY_CURRENT_USER)
        num = QueryInfoKey(openkey)[0]
        for i in range(num):
            subkey = EnumKey(openkey, i)
            count = count + 1
            key.append(subkey)
        CloseKey(openkey)
        for i in range(num):
            allkey.append('HKEY_CURRENT_USER\\' + key[i])    


        key = []
        openkey = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        num = QueryInfoKey(openkey)[0]
        for i in range(num):
            subkey = EnumKey(openkey, i)
            count = count + 1
            key.append(subkey)
        CloseKey(openkey)
        for i in range(num):
            allkey.append('HKEY_LOCAL_MACHINE\\' + key[i])    


        key = []
        openkey = ConnectRegistry(None, HKEY_USERS)
        num = QueryInfoKey(openkey)[0]
        for i in range(num):
            subkey = EnumKey(openkey, i)
            count = count + 1
            key.append(subkey)
        CloseKey(openkey)
        for i in range(num):
            allkey.append('HKEY_USERS\\' + key[i])          
        dem = 0
        for key in range(count):
            for key_name in GetPath(allkey[key]):
                value = GetValue(key_name)
                dem = dem + 1
                if value:
                    #save key in sub dict
                    sub_dict = {key_name : value}
                    if order == "first":
                        first_dict.update(sub_dict)
                    if order == "second":
                        second_dict.update(sub_dict)
        
        messagebox.showinfo("Information", "Registry snapshot completed!")
    if str(mode.get()) == "system":
        for root, direct, files in os.walk("C:/Windows/system32") :
            sub_dict = {root : files}
            if order == "first":
                first_dict.update(sub_dict)
            if order == "second":
                second_dict.update(sub_dict)
        messagebox.showinfo("Information", "System32 snapshot completed!")
    if str(mode.get()) == "process":
        p = psutil.pids()
        count = len(p)
        if order == "first":    
            for id in p:
                process = psutil.Process(id)
                sub_data = {id:process.name()}
                first_dict.update(sub_data)
        else: 
            for id in p:
                process = psutil.Process(id)
                sub_data = {id:process.name()}
                second_dict.update(sub_data)
        messagebox.showinfo("Information", "Process snapshot completed!")
    if order == "first":
        secondshot.configure(state="normal")
        firstshot.configure(state='disabled') 
    else:
        secondshot.configure(state="disabled") 

def shot_and_save(order):
    global path
    takesnapshot(order)
    # Registry and System mode
    if order == "first":
        if path == "":
            file_object = open("1stsnapshot.txt","w", encoding="utf-8")
        else:
            file_object = open(path + "/1stsnapshot.txt", "w", encoding = "utf-8")
        for key, value in first_dict.items():
            file_object.write(str(key) + " !=! " + str(value) + "\n")
    if order == "second":
        if path == "":
            file_object = open("2ndsnapshot.txt","w", encoding="utf-8")
        else:
            file_object = open(path + "/2ndsnapshot.txt", "w", encoding="utf-8")
        for key, value in second_dict.items():
            file_object.write(str(key) + " !=! " + str(value) + "\n")
    
    file_object.close()


def loadsnapshot(order):
    if order == "first":
        global first_dict
    if order == "second":
        global second_dict
    filename = OpenFile()
    file_object = open(filename, "r", encoding = "utf-8")
    for line in file_object:
        (key,value) = line.strip().split(' !=! ')
        if order == "first":
            first_dict[key]=value
        if order == "second":
            second_dict[key]=value
    file_object.close()
    messagebox.showinfo("Information", "Load file completed!")
    if order == "first":
        secondshot.configure(state="normal")
        firstshot.configure(state='disabled')
    else:
        secondshot.configure(state="disabled")

    

def compare():
    global first_dict
    global second_dict
    global path
    count = 0
    #length of dict 1st
    length = len(first_dict)
    if path == "":
        file_object = open("Report.txt","w", encoding="utf-8")
    else:
        file_object = open(path + "/Report.txt", "w", encoding = "utf-8")

    first_dict_key = list(first_dict.keys())
    second_dict_key = list(second_dict.keys())

    for second_key in second_dict_key:
        # type str
        second_value = str(second_dict.get(second_key))

        for first_key in first_dict_key:
            count = count + 1
            if second_key == first_key:
                first_value = str(first_dict.get(first_key))
                if second_value == first_value:
                    index = first_dict_key.index(first_key)
                    del first_dict_key[index]
                    length = length - 1
                    break
                else:
                    exact_second_value = second_value[1:-1]
                    exact_first_value = first_value[1:-1]
                    parts_second_value = exact_second_value.split('),')
                    parts_first_value = exact_first_value.split('),')
                    file_object.write('\nUpdate: ' +  str(second_key) + '\n')
                    numbers = len(parts_second_value)
                    for counter in range(numbers-1):
                        if parts_second_value[counter] != parts_first_value[counter]:               
                            file_object.write('Before:\n' + str(parts_first_value[counter]) + ')\n')
                            file_object.write('After:\n' + str(parts_second_value[counter]) + ')\n\n')
                    index = first_dict_key.index(first_key)
                    del first_dict_key[index]
                    length = length - 1
                    break
            if first_key != second_key and count == length:
                file_object.write('\nNew\n' + str(second_key) + '\n')
                file_object.write(str(second_value) + '\n')
        count = 0
    for key in first_dict_key:
        file_object.write("Deleted:\n")
        file_object.write(str(key)+"\n")
    file_object.close
    messagebox.showinfo("Information", "Completed!")
    firstshot.configure(state="normal")
    secondshot.configure(state="normal")



# GUI Window
window = Tk()
window.title("PTScanner")
window.geometry('300x180')
mode = StringVar()
mode.set("registry")
#checkbox
registry= Radiobutton(window, text='Registry', variable=mode, value="registry").grid(row=1, column = 0)
system =  Radiobutton(window, text='System', variable=mode, value="system").grid(row=2, column = 0)
memory =  Radiobutton(window, text='Process', variable=mode, value="process").grid(row=3, column = 0)

firstshot = Menubutton(window, relief='raised', width=15, text='1st shot')
firstshot.grid(row=1, column=2)
firstshot.menu = Menu(firstshot)
firstshot.menu.add_command(label='Shot', underline=0, command=lambda:takesnapshot("first"))
firstshot.menu.add_command(label='Shot and Save', underline=0, command=lambda:shot_and_save("first"))
firstshot.menu.add_command(label='Load', underline=0, command=lambda:loadsnapshot("first"))
firstshot['menu'] = firstshot.menu
    
secondshot = Menubutton(window, relief='raised', width=15, text='2nd shot', state = 'disabled')
secondshot.grid(row=2, column=2)
secondshot.menu = Menu(secondshot)
secondshot.menu.add_command(label='Shot', underline=0, command=lambda:takesnapshot("second"))
secondshot.menu.add_command(label='Shot and Save', underline=0, command=lambda:shot_and_save("second"))
secondshot.menu.add_command(label='Load', underline=0, command=lambda:loadsnapshot("second"))
secondshot['menu'] = secondshot.menu

# Button compare
btncompare = Button(master=window, text='Compare', command=compare).grid(row=8, column=1)

# Choose folder save file
def ChoosePath ():
    global txtvar
    global path
    mypath = OpenDir()
    txtvar.set(mypath)
    path = txtvar.get()

label = Label(window, text ='').grid(row=5, column=0)
label = Label(window, text='').grid(row=7, column=0)

lboutput = Label(window, text='Output: ').grid(row=6, column=0)
txtvar = StringVar()
entry = Entry(window, textvariable=txtvar, insertwidth=400).grid(row=6, column=1)

chooseFolder = Button(master=window, text="Choose folder", command=ChoosePath).grid(row =6, column=2)

window.mainloop()



