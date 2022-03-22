import isfreader
from tkinter import *
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
import numpy as np
# import csv

# Function for opening the file explorer window
def browseFiles():
    global filename, filetype
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("ISF/CSV files", "*.isf *.csv"),
                                                       ("all files", "*.*")))
    # Change label contents
    label_file_explorer.configure(text=filename)

    if (filename.split('.')[-1] == 'isf') or (filename.split('.')[-1] == 'ISF'):
        ReadISF()
        filetype = 'isf'
    elif (filename.split('.')[-1] == 'csv') or (filename.split('.')[-1] == 'CSV'):
        button_info['state'] = DISABLED
        button_plot['state'] = NORMAL
        button_writecsv['state'] = DISABLED
        filetype = 'csv'
    else:
        button_info['state'] = DISABLED
        button_plot['state'] = DISABLED
        button_writecsv['state'] = DISABLED
        filetype = ''

# Function for reading ISF
def ReadISF():
    global inf, x, y, name, filename
    try:
        file = isfreader.read_isf(filename)
        x = file[0]
        y = file[1]
        inf = file[2]
        name = filename.split('/')[-1]

        button_info['state'] = NORMAL
        button_plot['state'] = NORMAL
        button_writecsv['state'] = NORMAL
    except:
        messagebox.showerror(title='Error', message='Error while reading ISF')

# Function for writing info to CSV
def WriteCSV():
    try:
        savefile = '.'.join(filename.split('.')[:-1]) + '.csv'
        np.savetxt(savefile, [p for p in zip(x, y)], delimiter=',', fmt='%.12f')
        # writer = csv.writer(open(savefile, 'w', newline=''), delimiter=',')
        # for row in zip(x, y):
        #     writer.writerow(row)
        messagebox.showinfo(title='Saved', message='File saved as ' + savefile)
    except:
        messagebox.showerror(title='Error', message='Error while saving a file')

# Function for showing ISF information
def ShowISFInfo():
    try:
        info_window = Tk()
        info_window.title('Information: ' + name)

        inf_txt = '\n'.join('{} : {}'.format(key, value) for key, value in inf.items())

        text = Text(info_window)
        text.insert(INSERT, inf_txt)
        text.insert(END, "\n")
        text.pack()
    except:
        messagebox.showerror(title='Error', message='Error while processing ISF information')

def ShowPlot():
    if filetype == 'isf':
        ShowISFPlot()
    elif filetype == 'csv':
        ShowCSVPlot()
    else:
        messagebox.showerror(title='Error', message='Not an ISF or CSV file')

# Function for showing ISF plot
def ShowISFPlot():
    try:
        fig = plt.figure("Plot: " + name)
        plt.plot(x, y, linewidth=1)  
        plt.grid(color='0.9', linestyle='-', linewidth=0.5)
        fig.show()
    except:
        messagebox.showerror(title='Error', message='Error while making plot')

# Function for showing CSV plot
def ShowCSVPlot():
    try:
        name = filename.split('/')[-1]
        data = np.genfromtxt(filename, delimiter=',')
        fig = plt.figure("Plot: " + name)
        plt.plot(data[:,0], data[:,1], linewidth=1)  
        plt.grid(color='0.9', linestyle='-', linewidth=0.5)
        fig.show()
    except:
        messagebox.showerror(title='Error', message='Error while making plot')



window = Tk()

window.title('ISFPLOT')
window.geometry("350x150")
window.config(background = "white")
window.resizable(False, False)

# Create a File Explorer
label_file_explorer = Label(window,
                            text = "", height = 2,
                            background = "white")

# Buttons
button_explore = Button(window,
                        text = "Browse Files",
                        command = browseFiles)

button_writecsv = Button(window,
                        text = "Save as CSV",
                        command = WriteCSV)

button_info = Button(window,
                        text = "Show info",
                        command = ShowISFInfo)

button_plot = Button(window,
                        text = "Show plot",
                        command = ShowPlot)

button_info['state'] = DISABLED
button_plot['state'] = DISABLED
button_writecsv['state'] = DISABLED


# Placing everything on grid
label_file_explorer.grid(column = 1, row = 0)
button_explore.grid(column = 0, row = 0, padx=(10, 10), pady=(10, 10))
button_info.grid(column = 0, row = 1, padx=(10, 10), pady=(10, 10))
button_writecsv.grid(column = 1, row = 1, padx=(10, 10), pady=(10, 10))
button_plot.grid(column = 0, row = 2, padx=(10, 10), pady=(10, 10))

window.mainloop()

