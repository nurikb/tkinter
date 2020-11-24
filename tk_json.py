from tkinter import *
from tkinter import ttk
import tkinter as tk
import requests
import json
import tkinter.font as font
from bs4 import BeautifulSoup as bs
from tkinter.filedialog import askopenfilename

root = Tk()
root.title('')
root.iconbitmap(r'favicon.ico')
root.geometry("800x520")
root.resizable(width=False, height=False)


style = ttk.Style()

style.theme_use("vista")

style.configure("Treeview",
                background="silver",
                foreground="black",
                rowheight=25,
                fieldbackground="silver")
style.map('Treeview',
          background=[(' selected', 'blue',)])

# Create Treeframeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=20)

# Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)

my_tree.pack()

tree_scroll.configure(command=my_tree.yview)

my_tree['columns'] = ("TPId","WalletNo","Amount", "Name", "Currency", "Response")

my_tree.column("#0", width=20, minwidth=10)
my_tree.column("TPId", anchor=W, width=120)
my_tree.column("WalletNo", anchor=CENTER, width=80)
my_tree.column("Amount", anchor=W, width=120)
my_tree.column("Name", anchor=W, width=120)
my_tree.column("Currency", anchor=W, width=120)
my_tree.column("Response", anchor=W, width=120)

my_tree.heading("#0", text="", anchor=W)
my_tree.heading("TPId", text="TPId", anchor=W)
my_tree.heading("WalletNo", text="WalletNo", anchor=CENTER)
my_tree.heading("Amount", text="Amount", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Currency", text="Currency", anchor=W)
my_tree.heading("Response", text="Response", anchor=W)

myFont = font.Font(size=13)

filePath = None
global_json_data_list = []
st = 0

def get_path(path):
    global filePath

    search.delete(0, END)
    search.insert(0, path)

    filePath = search.get()
    get_table(json_parse(filePath))

def get_table(json_data):
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="red",)

    except_label.config(text='')

    for i in my_tree.get_children():
        my_tree.delete(i)

    count = 0

    if json_data != None:
        for value in json_data:

            my_tree.insert(parent='', index='end', iid=count, text="Parent",
                           values=(value["TPId"], value["WalletNo"], value["Amount"], value["Name"]+' ' + value["Surname"] , value["Currency"], ''),
                           tags="oddrow",)

            global_json_data_list.append([value["TPId"], value["WalletNo"], value["Amount"], value["Name"], value["Surname"], value["Currency"]])

            count += 1
    else:
        except_label.config(text='Выберите Json файл!', fg='red')

def json_parse(filePath):
    if '.json' in str(filePath):
        json_file = open(filePath)
        json_str = json_file.read()
        json_data = json.loads(json_str)[0]

        return json_data

    else:
        except_label.config(text='Выберите Json файл!', fg='red')

def post(json_data_list):
    global global_json_data_list
    global st

    try:
        for list, item in zip(json_data_list, my_tree.get_children()):

            f = xml_str.replace('<guid>string</guid>', f'<guid>{list[0]}</guid>')
            f = f.replace('<requisite>string</requisite>', f'<requisite>{list[1]}</requisite>')
            f = f.replace('<amount>decimal</amount>', f'<amount>{list[2]}</amount>')
            f = f.replace('<user_comment>string</user_comment>', f'<user_comment>{list[3]} {list[4]}</user_comment>')
            f = f.replace('<user_tin></user_tin>', f'<user_tin>{list[5]}</user_tin>')

            response = requests.post(url, headers=headers, data=f)
            soup = bs(response.content.decode("utf-8"), 'xml')
            accepted = soup.find('PaymentStatus').text

            if response.status_code != 200:
                break

            if accepted != 'Accepted':
                my_tree.item(str(int(item) + st), values=(list[0], list[1], list[2], list[3] + ' ' + list[4], list[5], accepted))
                my_tree.item(str(int(item) + st), tags="evenrow")
                btn_text.set("next")

                st += int(item)+1

                if json_data_list.index(list) == json_data_list.index(json_data_list[-1]):
                    global_json_data_list = list
                else:
                    global_json_data_list = json_data_list[json_data_list.index(list)+1:]

                break

            my_tree.item(str(int(item) + st), values=(list[0], list[1], list[2], list[3] + ' ' + list[4], list[5], accepted))
            btn_text.set("next")

    except:
        except_label.config(
            text='Сервер недоступен',fg='red')

add_Frame = Frame(root)
add_Frame.pack(pady=20)

search = Entry(add_Frame, width=40, bg='white', font=30)
search.grid(row=0, column=0)

search_btn = Button(add_Frame, text="choose file", command=lambda: get_path(askopenfilename()))
search_btn.grid(row=0, column=1)

btn_text = tk.StringVar()
post_btn = Button(root, textvariable=btn_text, bg='#0052cc', fg='#ffffff', command=lambda: post(global_json_data_list))
btn_text.set("post")
post_btn['font'] = myFont
post_btn.pack(pady=20)

except_label = Label(root, text='', font=20)
except_label.pack(pady=20)

url ='http://10.1.3.15/TerminalService.asmx?op=MakePaymentByServiceType'
headers = {'Content-Type': 'text/xml'}

xml_file = open('xml.txt', 'r')
xml_str = xml_file.read()

root.mainloop()
