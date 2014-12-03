"""
Name:                         Restauran Searcher
Version:                      1.0
Author:                       Daxeel Soni
Description:                  As a base evaluation, Restaurant Searcher is ideal for quickly 
                              finding out the contact details of famous restaurants or food courts, 
                              along with their precise location, anywhere on the globe. Some cities 
                              might not display any results, although this could be the cause of the 
                              lack of information about that location in the database from which the 
                              program retrieves data, and not the application itself.
Publisher:                    Daxeel Soni
Publisher's website:          www.about.me/daxeel
Download EXE:                 www.bit.ly/foodcity
API Copyrights:               Locu API (www.locu.com)
Status:                       First Release (Next release is in under development)
Copyright notice, terms & conditions:
(c) Copyrights 2014 by Daxeel Soni. All rights reserved.
This work may be modified, reproduced, distributed, performed, and displayed for any purpose
but must acknowledge "Daxeel Soni". 
Copyright is retained and must be preserved. The work is provided as is; no warranty is provided,
and users accept all the liability.
"""

############################
#IMPORTING REQUIRED MODULES
############################
import urllib.request as urllib2
import os
import json
import webbrowser
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
mycolor = '#FF5D40' #Color for scren background color
root = Tk() #Intializing Tkinter main window
root.geometry('800x610') #Tkinter window screen size
root.resizable(0, 0) #Restriction in maximize and minize action on window
##############################
#CHECKING INTERNET CONNECTION
##############################
x = os.system("ping -n 1  google.com")
if x == 1:
    tkinter.messagebox.showerror('No internet connection','Your device must be connected to an internet connection to use this software. Try again after connecting to internet.')
    root.destroy()
root.title('Restaurant Searcher')
if "nt" == os.name:
        root.wm_iconbitmap(bitmap = "rs.ico")
root.configure(bg=mycolor) #Changin color to 'mycolor' from default color

lbl = ttk.Label(root, text=' ', background=mycolor).pack()

#######################
#MAIN SEARCH FUNCTION
#######################
def search():
    if len(ent.get()) > 0:
        T.config(state=NORMAL)
        query = ent.get()
        total = 0
        api_key = 'b8874df6687805209926a0bed34d719c80f95945'
        url = 'https://api.locu.com/v1_0/venue/search/?api_key=' + api_key
        locality = query.replace(' ', '%20')
        final_url = url + "&locality=" + locality + "&category=restaurant"
        json_obj = urllib2.urlopen(final_url)
        data = json.loads(json_obj.readall().decode('utf-8'))

        T.delete('1.0', END)

        for item in data['objects']:
            total = total + 1
            T.insert(END,'\n---------------------------------------------------\nNAME    : %s'%(item['name']))
            if str(item['phone']) != 'None':
                T.insert(END,'\nPHONE   : %s'%(str(item['phone'])))
            else:
                T.insert(END,'\nPHONE   : Not found')
            if str(item['street_address']) != 'None':
                T.insert(END,'\nADDRESS : %s'%(str(item['street_address'])))
            else:
                T.insert(END,'\nADDRESS : Not found')
            if str(item['website_url']) != 'None':
                T.insert(END,'\nWEBSITE : %s'%(str(item['website_url'])))
            else:
                T.insert(END,'\nWEBSITE : Not found')
            T.insert(END,'\nID      : %s'%(str(item['id'])))
        T.insert(END,'\n---------------------------------------------------\n' + str(total) + ' results found\n---------------------------------------------------')
        T.config(state=DISABLED)
    else:
        tkinter.messagebox.showerror('Error','Please enter city to search restaurants.')

def about():
    tkinter.messagebox.showinfo('About','Restaurant Searcher\nCreator : Daxeel Soni (twitter.com/daxeelsoni)\nPowered by Locu')

frm_mn = ttk.Frame(root)
ent = ttk.Entry(frm_mn, width=70, foreground='#4C8400', justify=CENTER)
ent.pack(side=LEFT)
ent.insert("5", "Enter city name")
lbl = ttk.Label(frm_mn, text=' ', background=mycolor).pack(side=LEFT)
btn1 = ttk.Button(frm_mn, text='Search Restaurants', width=30, command=search)
btn1.pack(side=LEFT)
frm_mn.pack()

lbl = ttk.Label(root, text=' ', background=mycolor).pack()

tescfrm = ttk.Frame(root)
scr = ttk.Scrollbar(tescfrm, orient=VERTICAL)
T = Text(tescfrm, width=500, height=30)
scr.config(command=T.yview)
T.config(yscrollcommand=scr.set)
scr.pack(side="right", fill="y")
T.pack(fill="both")
tescfrm.pack()

T.insert(END, 'Search Results will be displayed here.')
T.config(state=DISABLED)

lbl = ttk.Label(root, text=' ', background=mycolor).pack()


def view_map():
    root2 = Tk()
    root2.title('Restaurant ID')
    if "nt" == os.name:
        root2.wm_iconbitmap(bitmap = "rs.ico")
    root2.resizable(0, 0)
    m1 = ttk.Entry(root2, width=40)
    m1.pack(side=LEFT)
    m1.insert("5", "Enter restaurant ID")

    def find_map():
        query = ent.get()
        total = 0
        api_key = 'b8874df6687805209926a0bed34d719c80f95945'
        url = 'https://api.locu.com/v1_0/venue/' + m1.get() + '/?api_key=' + api_key
        json_obj = urllib2.urlopen(url)
        data = json.loads(json_obj.readall().decode('utf-8'))
        lat, long = None, None
        if len(m1.get()) > 0 and len(data['not_found']) == 0:
            for item in data['objects']:
                if m1.get() == item['id']:
                    lat = str(item['lat'])
                    long = str(item['long'])
            webbrowser.open('http://maps.google.com/?q=' + lat + ',' + long)
            root2.destroy()
        else:
            tkinter.messagebox.showerror('Error','Invalid restaurant ID. Try again after entering valid ID')
            root2.destroy()

    m2 = ttk.Button(root2, text='Show Map', command=find_map)
    m2.pack(side=LEFT)
    root2.mainloop()

mn_frm = ttk.Frame(root)
btn1 = ttk.Button(mn_frm, text='View on map', width=30, command=view_map)
btn1.pack(side=LEFT)
lbl = ttk.Label(mn_frm, text=' ', background=mycolor).pack(side=LEFT)
btn2 = ttk.Button(mn_frm, text='About', width=10, command=about)
btn2.pack(side=LEFT)
mn_frm.pack()

root.mainloop()
