import os

import tkinter as tk

from tkinter import ttk
from tkinter import filedialog
from tkinter import font as tkfont

from ttkwidgets.autocomplete import AutocompleteEntryListbox

from matplotlib import gridspec
from matplotlib import pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import LogFormatter
from matplotlib.ticker import LogFormatterExponent
from matplotlib.ticker import LogFormatterMathtext
from matplotlib.ticker import NullLocator
from matplotlib.ticker import ScalarFormatter

import numpy as np

if __name__ == "__main__":
    import setup

from textio import DataFrame
from textio import RegText
from textio import LogASCII
from textio import Excel
from textio import IrrText
from textio import WSchedule
from textio import VTKit

# AUXILIARY FUNCTIONS TO CHOOSE INHERITANCE PATH

def getdata(data=None):

    if data is None:
        dbase = object
    elif data=="frame":
        dbase = DataFrame
    elif data=="excel":
        dbase = Excel
    elif data=="vtkit":
        dbase = VTKit
    elif data=="wschedule":
        dbase = WSchedule
    elif data=="logascii":
        dbase = LogASCII
    elif data=="nptext":
        dbase = RegText

    return dbase

# Main Visualizers

def TimeView(data=None):

    base = getdata(data)

    class TimeViewClass(base):

        legendpos = (
            "best","right",
            "upper left","upper center","upper right",
            "lower left","lower center","lower right",
            "center left","center","center right",
            )

        drawstyles = (
            'default','steps','steps-pre','steps-mid','steps-post',
            )

        linestyles = (
            ('-',    "solid line"),
            ('--',   "dashed line"),
            ('-.',   "dash dot line"),
            (':',    "dotted line"),
            (None,   "None Line"),
            (' ',    "Empty Space"),
            ('',     "Empty String"),
            )

        markers = (
            (None, "no marker"),
            ('.',  "point marker"),
            (',',  "pixel marker"),
            ('o',  "circle marker"),
            ('v',  "triangle down marker"),
            ('^',  "triangle up marker"),
            ('<',  "triangle left marker"),
            ('>',  "triangle right marker"),
            ('1',  "tri down marker"),
            ('2',  "tri up marker"),
            ('3',  "tri left marker"),
            ('4',  "tri right marker"),
            ('s',  "square marker"),
            ('p',  "pentagon marker"),
            ('*',  "star marker"),
            ('h',  "hexagon1 marker"),
            ('H',  "hexagon2 marker"),
            ('+',  "plus marker"),
            ('x',  "saltire marker"),
            ('D',  "diamond marker"),
            ('d',  "thin diamond marker"),
            ('|',  "vline marker"),
            ('_',  "hline marker"),
            )

        linecolors = (
            ('b', "blue"),
            ('g', "green"),
            ('r', "red"),
            ('c', "cyan"),
            ('m', "magenta"),
            ('y', "yellow"),
            ('k', "black"),
            ('w', "white"),
            )

        template0 = {
            "name": "Standard",
            #
            "subplots": [1,1],
            "title": [""],
            "twinx": [False],
            "xlabel": ["x-axis"],
            "ylabel": ["y-axis"],
            "legends": [True],
            "xticks": [None],
            "yticks": [None],
            "grid": [True],
            #
            "sublines": [[3]],
            "xaxes": [[(0,1),(0,1),(0,1)]],
            "yaxes": [[(0,2),(0,3),(0,4)]],
            "colors": [[6,0,2]],
            "markers": [[0,0,0]],
            "linestyles": [[0,1,0]],
            "drawstyles": [[0,0,0]],
            }

        template1 = {
            "name": "Standard-dual horizontal stack",
            #
            "subplots": [1,2],
            "twinx": [False,False],
            "title": ["Left","Right"],
            "xlabel": ["x-axis","x-axis"],
            "ylabel": ["y-axis","y-axis"],
            "legends": [True,True],
            "xticks": [None,None],
            "yticks": [None,None],
            "grid": [True,True],
            #
            "sublines": [[1],[2]],
            "xaxes": [[(0,1)],[(0,1),(0,1)]],
            "yaxes": [[(0,2)],[(0,3),(0,4)]],
            "colors": [[6],[0,2]],
            "markers": [[0],[0,0]],
            "linestyles": [[0],[0,0]],
            "drawstyles": [[0],[0,0]],
            }

        template2 = {
            "name": "Standard-dual vertical stack",
            #
            "subplots": [2,1],
            "twinx": [False,False],
            "title": ["Top","Bottom"],
            "xlabel": ["x-axis","x-axis"],
            "ylabel": ["y-axis","y-axis"],
            "legends": [True,True],
            "xticks": [None,None],
            "yticks": [None,None],
            "grid": [True,True],
            #
            "sublines": [[1],[2]],
            "xaxes": [[(0,1)],[(0,1),(0,1)]],
            "yaxes": [[(0,2)],[(0,3),(0,4)]],
            "colors": [[6],[0,2]],
            "markers": [[0],[0,0]],
            "linestyles": [[0],[0,0]],
            "drawstyles": [[4],[0,0]],
            }

        template3 = {
            "name": "Standard-quadruple",
            #
            "subplots": [2,2],
            "twinx": [False,False,False,False],
            "title": ["NW","NE","SW","SE"],
            "xlabel": ["x-axis","x-axis","x-axis","x-axis"],
            "ylabel": ["y-axis","y-axis","y-axis","y-axis"],
            "legends": [True,True,True,False],
            "xticks": [None,None,None,None],
            "yticks": [None,None,None,None],
            "grid": [True,True,True,True],
            #
            "sublines": [[1],[1],[1],[0]],
            "xaxes": [[(0,1)],[(0,1)],[(0,1)],[]],
            "yaxes": [[(0,2)],[(0,3)],[(0,4)],[]],
            "colors": [[6],[0],[2],[0]],
            "markers": [[0],[0],[0],[0]],
            "linestyles": [[0],[0],[0],[0]],
            "drawstyles": [[0],[0],[0],[0]],
            }

        templates = (
            template0,template1,template2,template3,
            )

        def __init__(self,window,**kwargs):

            super().__init__(**kwargs)

            self.dirname = os.path.dirname(__file__)

            self.root = window

        def set_plot(self):

            # configuration of window pane
            self.pane_NS = ttk.PanedWindow(self.root,orient=tk.VERTICAL,width=1000)

            self.frame_body = ttk.Frame(self.root,height=450)

            self.pane_NS.add(self.frame_body,weight=1)

            self.footer = tk.Listbox(self.root,height=5)

            self.pane_NS.add(self.footer,weight=0)

            self.pane_NS.pack(expand=1,fill=tk.BOTH)

            # configuration of top pane
            self.pane_EW = ttk.PanedWindow(self.frame_body,orient=tk.HORIZONTAL)

            self.frame_side = ttk.Frame(self.frame_body)

            self.pane_EW.add(self.frame_side,weight=0)

            self.frame_plot = ttk.Frame(self.frame_body)

            self.pane_EW.add(self.frame_plot,weight=1)

            self.pane_EW.pack(side=tk.LEFT,expand=1,fill=tk.BOTH)

            self.frame_plot.columnconfigure(0,weight=1)
            self.frame_plot.columnconfigure(1,weight=0)

            self.frame_plot.rowconfigure(0,weight=1)
            self.frame_plot.rowconfigure(1,weight=0)

            self.figure = plt.Figure()
            self.canvas = FigureCanvasTkAgg(self.figure,self.frame_plot)

            self.plotbox = self.canvas.get_tk_widget()
            self.plotbox.grid(row=0,column=0,sticky=tk.NSEW)        

            self.plotbar = VerticalNavigationToolbar2Tk(self.canvas,self.frame_plot)
            self.plotbar.update()
            self.plotbar.grid(row=0,column=1,sticky=tk.N)

            # configuration of top left pane
            self.pane_ns = ttk.PanedWindow(self.frame_side,orient=tk.VERTICAL,width=300)

            self.itembox = AutocompleteEntryListbox(self.frame_side,height=250,padding=0)

            self.itembox.content = self.itemnames.tolist()
            self.itembox.config(completevalues=self.itembox.content,allow_other_values=True)

            self.itembox.listbox.bind('<<ListboxSelect>>',lambda event: self.set_lines(event))

            self.pane_ns.add(self.itembox,weight=1)

            self.tempbox = ttk.Frame(self.frame_side,height=200)

            self.tempbox.rowconfigure(0,weight=0)
            self.tempbox.rowconfigure(1,weight=1)

            self.tempbox.columnconfigure(0,weight=1)
            self.tempbox.columnconfigure(1,weight=0)
            self.tempbox.columnconfigure(2,weight=0)

            self.tempbox.label = ttk.Label(self.tempbox,text="Graph Templates")
            self.tempbox.label.grid(row=0,column=0,sticky=tk.EW)

            self.tempbox.iconadd = tk.PhotoImage(file=os.path.join(self.dirname,"graphics","Add","Add-9.png"))
            self.tempbox.iconedit = tk.PhotoImage(file=os.path.join(self.dirname,"graphics","Edit","Edit-9.png"))
            self.tempbox.icondel = tk.PhotoImage(file=os.path.join(self.dirname,"graphics","Delete","Delete-9.png"))

            self.tempbox.buttonadd = ttk.Button(self.tempbox,image=self.tempbox.iconadd,command=lambda:self.get_template("add"))
            self.tempbox.buttonadd.grid(row=0,column=1)

            self.tempbox.buttonedit = ttk.Button(self.tempbox,image=self.tempbox.iconedit,command=lambda:self.get_template("edit"))
            self.tempbox.buttonedit.grid(row=0,column=2)

            self.tempbox.buttondel = ttk.Button(self.tempbox,image=self.tempbox.icondel,command=lambda:self.get_template("delete"))
            self.tempbox.buttondel.grid(row=0,column=3)

            self.tempbox.listbox = tk.Listbox(self.tempbox,exportselection=False)
            self.tempbox.listbox.grid(row=1,column=0,columnspan=4,sticky=tk.NSEW)

            for template in self.templates:
                self.tempbox.listbox.insert(tk.END,template.get("name"))

            self.curtemp = {}

            self.tempbox.listbox.bind('<<ListboxSelect>>',lambda event: self.set_axes(event))

            self.pane_ns.add(self.tempbox,weight=1)

            self.pane_ns.pack(expand=1,fill=tk.BOTH)

        def set_axes(self,event):

            if not self.tempbox.listbox.curselection():
                return

            if self.curtemp == self.templates[self.tempbox.listbox.curselection()[0]]:
                return
            
            self.curtemp = self.templates[self.tempbox.listbox.curselection()[0]]

            naxrows,naxcols = self.curtemp.get("subplots")

            twinx = self.curtemp.get("twinx")

            self.curtemp["flagMainAxes"] = []

            for flagTwinAxis in twinx:
                self.curtemp["flagMainAxes"].append(True)
                if flagTwinAxis: self.curtemp["flagMainAxes"].append(False)

            if hasattr(self,"axes"):
                self.figure.clear()
                # [self.figure.delaxes(axis) for axis in self.axes]

            self.axes = []

            for index,flagMainAxis in enumerate(self.curtemp.get("flagMainAxes")):

                index_main = sum(self.curtemp.get("flagMainAxes")[:index+1])-1

                if flagMainAxis:
                    axis = self.figure.add_subplot(naxrows,naxcols,index_main+1)
                else:
                    axis = self.axes[-1].twinx()
                    
                if flagMainAxis and self.curtemp.get("title")[index_main] is not None:
                    axis.set_title(self.curtemp.get("title")[index_main])

                if flagMainAxis and self.curtemp.get("xlabel")[index_main] is not None:
                    axis.set_xlabel(self.curtemp.get("xlabel")[index_main])

                if self.curtemp.get("ylabel")[index] is not None:
                    axis.set_ylabel(self.curtemp.get("ylabel")[index])

                if flagMainAxis and self.curtemp.get("xticks")[index_main] is not None:
                    axis.set_xticks(self.curtemp.get("xticks")[index_main])

                if self.curtemp.get("yticks")[index] is not None:
                    axis.set_yticks(self.curtemp.get("yticks")[index])

                if flagMainAxis and self.curtemp.get("grid")[index_main] is not None:
                    axis.grid(self.curtemp.get("grid")[index_main])

                self.axes.append(axis)

                # for tick in axis0.get_xticklabels():
                #     tick.set_rotation(45)

            status = "{} template has been selected.".format(self.curtemp.get("name"))

            self.footer.insert(tk.END,status)
            self.footer.see(tk.END)

            self.figure.set_tight_layout(True)

            self.canvas.draw()

        def set_lines(self,event):

            if self.itembox.listbox.curselection():
                itemname = self.itemnames[self.itembox.listbox.curselection()[0]]
            else:
                return

            if not hasattr(self,"axes"):
                status = "No template has been selected."
                self.footer.insert(tk.END,status)
                self.footer.see(tk.END)
                return

            for attrname in self.attrnames:
                if hasattr(self,attrname):
                    getattr(self,attrname).filter(0,keywords=[itemname],inplace=False)

            if hasattr(self,"lines"):
                [line.remove() for line in self.lines]
                    
            self.lines = []

            self.plotbar.update()

            for index,axis in enumerate(self.axes):

                xaxes = self.curtemp.get("xaxes")[index]
                yaxes = self.curtemp.get("yaxes")[index]

                colors = self.curtemp.get("colors")[index]
                markers = self.curtemp.get("markers")[index]
                lstyles = self.curtemp.get("linestyles")[index]
                dstyles = self.curtemp.get("drawstyles")[index]

                for xaxis,yaxis,color,marker,lstyle,dstyle in zip(xaxes,yaxes,colors,markers,lstyles,dstyles):
                    line = axis.plot(
                        getattr(self,self.attrnames[xaxis[0]]).running[xaxis[1]],
                        getattr(self,self.attrnames[yaxis[0]]).running[yaxis[1]],
                        color=self.linecolors[color][0],
                        marker=self.markers[marker][0],
                        linestyle=self.linestyles[lstyle][0],
                        drawstyle=self.drawstyles[dstyle],
                        label=getattr(self,self.attrnames[yaxis[0]]).headers[yaxis[1]])[0]
                    self.lines.append(line)

                # if self.curtemp.get("legends")[index]:
                #     axis.legend()

                axis.relim()
                axis.autoscale()
                axis.set_ylim(bottom=0,top=None,auto=True)

            self.figure.set_tight_layout(True)

            self.canvas.draw()

        def get_template(self,manipulation):

            if manipulation=="add":

                self.curtemp = {# when creating a template
                    "name": "",
                    "subplots": [1,1],
                    "title": [""],
                    "twinx": [False],
                    "xlabel": [""],
                    "ylabel": [""],
                    "legends": [False],
                    "xticks": [None],
                    "yticks": [None],
                    "grid": [False],
                    #
                    "sublines": [[0]],
                    "xaxes": [[]],
                    "yaxes": [[]],
                    "colors": [[]],
                    "markers": [[]],
                    "linestyles": [[]],
                    "drawstyles": [[]],
                    }

                self.set_temptop("add") # when adding a new one

            elif manipulation=="edit":

                if not self.tempbox.listbox.curselection(): return # when editing

                self.curtemp = self.templates[self.tempbox.listbox.curselection()[0]] # when editing
                self.set_temptop(tempid=self.tempbox.listbox.curselection()[0]) # editing the existing one
                
            elif manipulation=="delete":
                # deleting a template

                if not self.tempbox.listbox.curselection(): return

                name = self.tempbox.listbox.get(self.tempbox.listbox.curselection())

                item = self.curtemp.get("name").index(name)
                
                self.tempbox.listbox.delete(item)

                self.curtemp.get("name").pop(item)
                # self.curtemp.get("naxrows").pop(item)
                # self.curtemp.get("naxcols").pop(item)

        def set_temptop(self,manipulation,tempid=None):

            if hasattr(self,"temptop"):
                if self.temptop.winfo_exists(): return

            if tempid is not None:
                curtemp = self.templates[tempid]
            else:
                curtemp = {"subplots": [1,1]}
                curtemp["sublines"] = [[1,0]]

            self.temptop = tk.Toplevel()

            self.temptop.title("Template Editor")

            self.temptop.geometry("700x450")

            self.temptop.resizable(0,0)

            self.style = ttk.Style(self.temptop)

            self.style.configure("TNotebook.Tab",width=15,anchor=tk.CENTER)

            self.tempedit = ttk.Notebook(self.temptop)

            # General Properties

            self.tempeditgeneral = tk.Frame(self.tempedit)

            self.tempeditgeneral0 = tk.Frame(self.tempeditgeneral,borderwidth=2,relief=tk.GROOVE)

            self.tempeditgeneral0.templabel = ttk.Label(self.tempeditgeneral0,text="Settings")
            self.tempeditgeneral0.templabel.grid(row=0,column=0,columnspan=2,sticky=tk.W,padx=(10,10),pady=(2,2))

            self.tempeditgeneral0.tempnamelabel = ttk.Label(self.tempeditgeneral0,text="Template Name")
            self.tempeditgeneral0.tempnamelabel.grid(row=1,column=0,sticky=tk.E,padx=(10,10),pady=(2,2))

            self.tempeditgeneral0.tempname = ttk.Entry(self.tempeditgeneral0,width=30)
            self.tempeditgeneral0.tempname.grid(row=1,column=1,padx=(0,20),pady=(2,2),sticky=tk.EW)

            self.tempeditgeneral0.tempname.focus()

            self.tempeditgeneral0.legendLabel = ttk.Label(self.tempeditgeneral0,text="Legend Position")
            self.tempeditgeneral0.legendLabel.grid(row=2,column=0,sticky=tk.E,padx=(10,10),pady=(2,2))

            self.tempeditgeneral0.legend = ttk.Entry(self.tempeditgeneral0,width=30)
            self.tempeditgeneral0.legend.grid(row=2,column=1,padx=(0,20),pady=(2,2),sticky=tk.EW)

            self.tempeditgeneral0.pack(side=tk.LEFT,expand=0,fill=tk.Y)

            self.tempeditgeneral1 = tk.Frame(self.tempeditgeneral,borderwidth=2)

            self.tempeditgeneral1.naxlabel = ttk.Label(self.tempeditgeneral1,text="Number of Axes")
            self.tempeditgeneral1.naxlabel.grid(row=0,column=0,columnspan=2,sticky=tk.EW,padx=(10,2),pady=(2,2))

            self.tempeditgeneral1.naxrowslabel = ttk.Label(self.tempeditgeneral1,text="Rows")
            self.tempeditgeneral1.naxrowslabel.grid(row=1,column=0,sticky=tk.E,padx=(10,10),pady=(2,2))

            self.tempeditgeneral1.naxval0 = tk.StringVar(self.root)
            self.tempeditgeneral1.naxrows = ttk.Spinbox(self.tempeditgeneral1,textvariable=self.tempeditgeneral1.naxval0,from_=1,to=5,command=lambda:self.set_temptopdict("rows"))
            self.tempeditgeneral1.naxrows.grid(row=1,column=1,sticky=tk.EW,padx=(0,2),pady=(2,2))

            self.tempeditgeneral1.naxcolslabel = ttk.Label(self.tempeditgeneral1,text="Columns")
            self.tempeditgeneral1.naxcolslabel.grid(row=2,column=0,sticky=tk.E,padx=(10,10),pady=(2,2))

            self.tempeditgeneral1.naxval1 = tk.StringVar(self.root)
            self.tempeditgeneral1.naxcols = ttk.Spinbox(self.tempeditgeneral1,textvariable=self.tempeditgeneral1.naxval1,from_=1,to=5,command=lambda:self.set_temptopdict("columns"))
            self.tempeditgeneral1.naxcols.grid(row=2,column=1,sticky=tk.EW,padx=(0,2),pady=(2,2))

            self.tempeditgeneral1.pack(side=tk.LEFT,expand=1,fill=tk.BOTH)
            
            self.tempedit.add(self.tempeditgeneral,text="General",compound=tk.CENTER)

            # Axes Properties

            self.tempeditaxes = tk.Frame(self.tempedit)

            self.tempeditaxes0 = tk.Frame(self.tempeditaxes,borderwidth=2,relief=tk.GROOVE)

            self.tempeditaxes0.axislabel = ttk.Label(self.tempeditaxes0,text="Axis List")
            self.tempeditaxes0.axislabel.pack(side=tk.TOP,fill=tk.X)

            self.tempeditaxes0.listbox = tk.Listbox(self.tempeditaxes0)

            self.tempeditaxes0.listbox.pack(side=tk.TOP,expand=1,fill=tk.BOTH)

            self.tempeditaxes0.pack(side=tk.LEFT,expand=0,fill=tk.Y)

            self.tempeditaxes1 = tk.Frame(self.tempeditaxes,borderwidth=2,relief=tk.GROOVE)

            self.tempeditaxes1.entry00 = tk.IntVar(self.root)
            self.tempeditaxes1.check00 = ttk.Checkbutton(self.tempeditaxes1,text="Draw X Twin",variable=self.tempeditaxes1.entry00,command=lambda:self.set_temptopdict("entry00"))
            self.tempeditaxes1.check00.grid(row=0,column=0,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditaxes1.label01 = ttk.Label(self.tempeditaxes1,text="Title")
            self.tempeditaxes1.label01.grid(row=1,column=0,sticky=tk.EW,padx=(30,),pady=(4,))
            self.tempeditaxes1.entry01 = ttk.Entry(self.tempeditaxes1)
            self.tempeditaxes1.entry01.grid(row=1,column=1,sticky=tk.EW,padx=(0,10),pady=(4,))

            self.tempeditaxes1.label02 = ttk.Label(self.tempeditaxes1,text="X Label")
            self.tempeditaxes1.label02.grid(row=2,column=0,sticky=tk.EW,padx=(30,),pady=(4,))
            self.tempeditaxes1.entry02 = ttk.Entry(self.tempeditaxes1)
            self.tempeditaxes1.entry02.grid(row=2,column=1,sticky=tk.EW,padx=(0,10),pady=(4,))

            self.tempeditaxes1.label03 = ttk.Label(self.tempeditaxes1,text="Y-1 Label")
            self.tempeditaxes1.label03.grid(row=3,column=0,sticky=tk.EW,padx=(30,),pady=(4,))
            self.tempeditaxes1.entry03 = ttk.Entry(self.tempeditaxes1,state=tk.NORMAL)
            self.tempeditaxes1.entry03.grid(row=3,column=1,sticky=tk.EW,padx=(0,10),pady=(4,))

            self.tempeditaxes1.label04 = ttk.Label(self.tempeditaxes1,text="Y-2 Label",state=tk.DISABLED)
            self.tempeditaxes1.label04.grid(row=4,column=0,sticky=tk.EW,padx=(30,),pady=(4,))
            self.tempeditaxes1.entry04 = ttk.Entry(self.tempeditaxes1,state=tk.DISABLED)
            self.tempeditaxes1.entry04.grid(row=4,column=1,sticky=tk.EW,padx=(0,10),pady=(4,))

            self.tempeditaxes1.entry05 = tk.StringVar(self.root)
            self.tempeditaxes1.label05 = ttk.Label(self.tempeditaxes1,text="Y-1 Lines")
            self.tempeditaxes1.label05.grid(row=5,column=0,sticky=tk.EW,padx=(30,),pady=(4,))
            self.tempeditaxes1.spinb05 = ttk.Spinbox(self.tempeditaxes1,to=20,textvariable=self.tempeditaxes1.entry05,command=lambda:self.set_temptopdict("entry05"))
            self.tempeditaxes1.spinb05.grid(row=5,column=1,sticky=tk.EW,padx=(0,10),pady=(4,))

            self.tempeditaxes1.entry06 = tk.StringVar(self.root)
            self.tempeditaxes1.label06 = ttk.Label(self.tempeditaxes1,text="Y-2 Lines",state=tk.DISABLED)
            self.tempeditaxes1.label06.grid(row=6,column=0,sticky=tk.EW,padx=(30,),pady=(4,))
            self.tempeditaxes1.spinb06 = ttk.Spinbox(self.tempeditaxes1,to=20,textvariable=self.tempeditaxes1.entry06,command=lambda:self.set_temptopdict("entry06"),state=tk.DISABLED)
            self.tempeditaxes1.spinb06.grid(row=6,column=1,sticky=tk.EW,padx=(0,10),pady=(4,))

            self.tempeditaxes1.entry07 = tk.IntVar(self.root)
            self.tempeditaxes1.check07 = ttk.Checkbutton(self.tempeditaxes1,text="Show Legends",variable=self.tempeditaxes1.entry07)
            self.tempeditaxes1.check07.grid(row=7,column=0,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditaxes1.entry08 = tk.IntVar(self.root)
            self.tempeditaxes1.check08 = ttk.Checkbutton(self.tempeditaxes1,text="Show X Ticks",variable=self.tempeditaxes1.entry08)
            self.tempeditaxes1.check08.grid(row=8,column=0,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditaxes1.entry09 = tk.IntVar(self.root)
            self.tempeditaxes1.check09 = ttk.Checkbutton(self.tempeditaxes1,text="Show Y-1 Ticks",variable=self.tempeditaxes1.entry09)
            self.tempeditaxes1.check09.grid(row=9,column=0,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditaxes1.entry10 = tk.IntVar(self.root)
            self.tempeditaxes1.check10 = ttk.Checkbutton(self.tempeditaxes1,text="Show Y-2 Ticks",variable=self.tempeditaxes1.entry10,state=tk.DISABLED)
            self.tempeditaxes1.check10.grid(row=10,column=0,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditaxes1.entry11 = tk.IntVar(self.root)
            self.tempeditaxes1.check11 = ttk.Checkbutton(self.tempeditaxes1,text="Show Grids",variable=self.tempeditaxes1.entry11)
            self.tempeditaxes1.check11.grid(row=11,column=0,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditaxes1.pack(side=tk.LEFT,expand=1,fill=tk.BOTH)

            self.tempedit.add(self.tempeditaxes,text="Axes",compound=tk.CENTER)

            # Line Properties

            self.tempeditlines = tk.Frame(self.tempedit)

            self.tempeditlines0 = tk.Frame(self.tempeditlines,borderwidth=2,relief=tk.GROOVE)

            self.tempeditlines0.axislabel = ttk.Label(self.tempeditlines0,text="Axis List")
            self.tempeditlines0.axislabel.pack(side=tk.TOP,fill=tk.X)

            self.tempeditlines0.listbox = tk.Listbox(self.tempeditlines0)

            self.tempeditlines0.listbox.pack(side=tk.TOP,expand=1,fill=tk.BOTH)

            self.tempeditlines0.pack(side=tk.LEFT,expand=0,fill=tk.Y)

            self.tempeditlines1 = tk.Frame(self.tempeditlines,borderwidth=2,relief=tk.GROOVE)

            self.tempeditlines1.line1label = ttk.Label(self.tempeditlines1,text="Y-1 Lines")
            self.tempeditlines1.line1label.pack(side=tk.TOP,fill=tk.X)

            self.tempeditlines1.listbox1 = tk.Listbox(self.tempeditlines1)

            self.tempeditlines1.listbox1.pack(side=tk.TOP,expand=1,fill=tk.BOTH)

            self.tempeditlines1.line2label = ttk.Label(self.tempeditlines1,text="Y-2 Lines")
            self.tempeditlines1.line2label.pack(side=tk.TOP,fill=tk.X)

            self.tempeditlines1.listbox2 = tk.Listbox(self.tempeditlines1)

            self.tempeditlines1.listbox2.pack(side=tk.TOP,expand=1,fill=tk.BOTH)

            self.tempeditlines1.pack(side=tk.LEFT,expand=0,fill=tk.Y)

            self.tempeditlines2 = tk.Frame(self.tempeditlines)

            self.tempeditlines2.label = ttk.Label(self.tempeditlines2,text="Line Details")
            self.tempeditlines2.label.grid(row=0,column=0,columnspan=2,sticky=tk.W,padx=(10,),pady=(4,))

            self.tempeditlines2.label0 = ttk.Label(self.tempeditlines2,text="X-axis")
            self.tempeditlines2.label0.grid(row=1,column=0,sticky=tk.E,padx=(10,),pady=(2,))

            self.tempeditlines2.label1 = ttk.Label(self.tempeditlines2,text="Y-axis")
            self.tempeditlines2.label1.grid(row=2,column=0,sticky=tk.E,padx=(10,),pady=(2,))

            self.tempeditlines2.label2 = ttk.Label(self.tempeditlines2,text="Draw Style")
            self.tempeditlines2.label2.grid(row=3,column=0,sticky=tk.E,padx=(10,),pady=(2,))

            self.tempeditlines2.label3 = ttk.Label(self.tempeditlines2,text="Line Style")
            self.tempeditlines2.label3.grid(row=4,column=0,sticky=tk.E,padx=(10,),pady=(2,))

            self.tempeditlines2.label4 = ttk.Label(self.tempeditlines2,text="Line Color")
            self.tempeditlines2.label4.grid(row=5,column=0,sticky=tk.E,padx=(10,),pady=(2,))

            self.tempeditlines2.val0 = tk.StringVar(self.tempeditlines2)
            self.tempeditlines2.val1 = tk.StringVar(self.tempeditlines2)
            self.tempeditlines2.val2 = tk.StringVar(self.tempeditlines2)
            self.tempeditlines2.val3 = tk.StringVar(self.tempeditlines2)
            self.tempeditlines2.val4 = tk.StringVar(self.tempeditlines2)

            self.tempeditlines2.menu0 = ttk.OptionMenu(
                self.tempeditlines2,self.tempeditlines2.val0,"Select Attribute",*self.attrnames)
            self.tempeditlines2.menu0.grid(row=1,column=1,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditlines2.menu1 = ttk.OptionMenu(
                self.tempeditlines2,self.tempeditlines2.val1,"Select Attribute",*self.attrnames)
            self.tempeditlines2.menu1.grid(row=2,column=1,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditlines2.menu2 = ttk.OptionMenu(
                self.tempeditlines2,self.tempeditlines2.val2,"Select Style",*self.drawstyles)
            self.tempeditlines2.menu2.grid(row=3,column=1,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditlines2.menu3 = ttk.OptionMenu(
                self.tempeditlines2,self.tempeditlines2.val3,"Select Style",*self.linestyles)
            self.tempeditlines2.menu3.grid(row=4,column=1,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditlines2.menu4 = ttk.OptionMenu(
                self.tempeditlines2,self.tempeditlines2.val4,"Select Color",*self.linecolors)
            self.tempeditlines2.menu4.grid(row=5,column=1,sticky=tk.EW,padx=(10,),pady=(4,))

            self.tempeditlines2.pack(side=tk.LEFT,expand=1,fill=tk.BOTH)

            self.tempedit.add(self.tempeditlines,text="Lines",compound=tk.CENTER)

            self.tempedit.pack(side=tk.TOP,expand=1,fill=tk.BOTH,padx=(0,1))

            buttonname = "Add Template" if tempid is None else "Edit Template"

            self.temptop.button = ttk.Button(self.temptop,text=buttonname,width=20,command=lambda: self.temptopapply(tempid))
            self.temptop.button.pack(side=tk.TOP,expand=1,anchor=tk.E,padx=(0,1),pady=(1,1))

            self.temptop.button.bind('<Return>',lambda event: self.temptopapply(tempid,event))

            self.temptop.mainloop()

        def set_temptopdict(self):
            pass
            # self.tempeditgeneral0.tempname.insert(0,curtemp.get("name"))
            # naxrows,naxcols = self.curtemp.get("subplots")

            # self.tempeditgeneral1.naxrows.insert(0,naxrows)
            # self.tempeditgeneral1.naxcols.insert(0,naxcols)

            # for index in range(naxrows*naxcols):
            #     self.tempeditaxes0.listbox.insert(tk.END,"Axis {}".format(index))
            #     self.tempeditlines0.listbox.insert(tk.END,"Axis {}".format(index))

            # self.tempeditaxes1.entry00.set(self.curtemp.get("twinx")[0])
            # self.tempeditaxes1.entry01.set(self.curtemp.get("title")[0])
            # self.tempeditaxes1.enrty02.set(self.curtemp.get("xlabel")[0])
            # self.tempeditaxes1.enrty03.set(self.curtemp.get("ylabel")[0])
            # self.tempeditaxes1.enrty04.set(self.curtemp.get("ylabel")[1])
            # self.tempeditaxes1.entry05.set(self.curtemp.get("sublines")[0])
            # self.tempeditaxes1.entry06.set(self.curtemp.get("sublines")[1])
            # self.tempeditaxes1.entry07.set(self.curtemp.get("legends")[0])
            # self.tempeditaxes1.entry08.set(self.curtemp.get("xticks")[0])
            # self.tempeditaxes1.entry09.set(self.curtemp.get("yticks")[0])
            # self.tempeditaxes1.entry10.set(self.curtemp.get("yticks")[1])
            # self.tempeditaxes1.entry11.set(self.curtemp.get("grids")[0])

            # for index in range(curtemp.get("sublines")[0][0]):
            #     self.tempeditlines1.listbox1.insert(tk.END,"Line {}".format(index))

            # for index in range(curtemp.get("sublines")[0][1]):
            #     self.tempeditlines1.listbox2.insert(tk.END,"Line {}".format(index))

            # self.tempeditlines2.val0.set(self.headers[self.curtemp.get("xaxes")[0][0]])
            # self.tempeditlines2.val1.set(self.headers[self.curtemp.get("yaxes")[0][0]])
            # self.tempeditlines2.val2.set(self.drawstyles[self.curtemp.get("drawstyles")[0][0]])
            # self.tempeditlines2.val3.set(self.linestyles[self.curtemp.get("linestyles")[0][0]])
            # self.tempeditlines2.val4.set(self.linecolors[self.curtemp.get("linecolors")[0][0]])

        def set_temptopedits(self,input_):

            if input_=="rows" or input_=="columns":
                numx = self.tempeditgeneral1.naxval0.get()
                numy = self.tempeditgeneral1.naxval1.get()
                numx = int(numx) if numx else 1
                numy = int(numy) if numy else 1
                numa = numx*numy
                if numa>len(self.tempeditaxes0.listbox.get(0,tk.END)):
                    self.tempeditaxes0.listbox.insert(tk.END,"Axis {}".format(numa))
                    self.tempeditlines0.listbox.insert(tk.END,"Axis {}".format(numa))
            elif input_=="entry00":
                if self.tempeditaxes1.entry00.get():
                    self.tempeditaxes1.label04.config(state=tk.NORMAL)
                    self.tempeditaxes1.entry04.config(state=tk.NORMAL)
                    self.tempeditaxes1.label06.config(state=tk.NORMAL)
                    self.tempeditaxes1.spinb06.config(state=tk.NORMAL)
                    self.tempeditaxes1.check10.config(state=tk.NORMAL)
                else:
                    self.tempeditaxes1.label04.config(state=tk.DISABLED)
                    self.tempeditaxes1.entry04.config(state=tk.DISABLED)
                    self.tempeditaxes1.label06.config(state=tk.DISABLED)
                    self.tempeditaxes1.spinb06.config(state=tk.DISABLED)
                    self.tempeditaxes1.check10.config(state=tk.DISABLED)
            elif input_=="entry05":
                num1 = int(self.tempeditaxes1.entry05.get())
                if num1>len(self.tempeditlines1.listbox1.get(0,tk.END)):
                    self.tempeditlines1.listbox1.insert(tk.END,"Line {}".format(num1))
            elif input_=="entry06":
                num2 = int(self.tempeditaxes1.entry06.get())
                if num2>len(self.tempeditlines1.listbox2.get(0,tk.END)):
                    self.tempeditlines1.listbox2.insert(tk.END,"Line {}".format(num2))

            # if x.isdigit() or x=="":
            #     # print(prop)
            #     return True
            # else:
            #     return False

        def set_template(self,tempid=None,event=None):

            if event is not None and event.widget!=self.temptop.button:
                return

            if tempid is not None:
                names = [name for index,name in enumerate(self.curtemp.get("name")) if index!=tempid]
            else:
                names = self.curtemp.get("name")

            name = self.tempeditgeneral0.tempname.get()

            if name in names:
                tk.messagebox.showerror("Error","You have a template with the same name!",parent=self.temptop)
                return
            elif name.strip()=="":
                tk.messagebox.showerror("Error","You have not named the template!",parent=self.temptop)
                return

            if tempid is None:
                tempid = len(self.temps.get("names"))
            else:
                self.tempbox.listbox.delete(tempid)
                self.curtemp.get("name").pop(tempid)
                # self.curtemp.get("naxrows").pop(tempid)
                # self.curtemp.get("naxcols").pop(tempid)
            
            self.tempbox.listbox.insert(tempid,name)

            self.curtemp.get("name").insert(tempid,name)

            try:
                naxrows = int(self.tempeditgeneral1.naxrows.get())
            except ValueError:
                naxrows = 1

            # self.curtemp.get("naxrows").insert(tempid,naxrows)

            try:
                naxcols = int(self.tempeditgeneral1.naxcols.get())
            except ValueError:
                naxcols = 1

            # self.curtemp.get("naxcols").insert(tempid,naxcols)

            self.temptop.destroy()

    return TimeViewClass

def LogView(data=None):

    base = getdata(data)

    class LogViewClass(base):

        lineColors = (
            "black",
            "crimson",
            "blue",
            "sienna",
            )

        color_sandstone = "gold"
        color_limestone = "navajowhite"
        color_dolomite  = "darkkhaki"
        color_clean     = "tan"
        color_shale     = "gray"
        color_waterclay = "lightskyblue"
        color_watercapi = "lightsteelblue"
        color_waterirre = "lightblue"
        color_watermove = "steelblue"
        color_water     = "aqua"
        color_HC        = "green"
        color_oil       = "limegreen"
        color_gas       = "lightgreen"
        color_fluidmove = "seagreen"

        spinerelpos = (0,0.1,0.2,0.3)

        def __init__(self,filepaths=None,**kwargs):

            super().__init__(filepaths=filepaths,**kwargs)

        def set_histogram(self,idframe,idcol,logscale=False):

            self.fig_hist,self.axis_hist = plt.subplots()

            las = self.frames[idframe]

            yaxis = las.running[idcol]

            if logscale:
                yaxis = np.log10(yaxis[np.nonzero(yaxis)[0]])

            try:
                unit = las.units[idcol]
            except IndexError:
                unit = "not-defined"

            try:
                descr = las.details[idcol]
            except IndexError:
                descr = las.headers[idcol]

            if logscale:
                xlabel = "log10(nonzero-{}) [{}]".format(descr,unit)
            else:
                xlabel = "{} [{}]".format(descr,unit)

            self.axis_hist.hist(yaxis,density=True,bins=30)  # density=False would make counts
            self.axis_hist.set_ylabel("Probability")
            self.axis_hist.set_xlabel(xlabel)

        def set_nangraph(self,idframe):

            self.fig_nan,self.axis_nan = plt.subplots()

            las = self.frames[idframe]

            yvals = []
            zvals = []

            depth = las.columns(0)

            for index,column in enumerate(las.running):

                isnan = np.isnan(column)

                L_shift = np.ones(column.shape,dtype=bool)
                R_shift = np.ones(column.shape,dtype=bool)

                L_shift[:-1] = isnan[1:]
                R_shift[1:] = isnan[:-1]

                lower = np.where(np.logical_and(~isnan,R_shift))[0]
                upper = np.where(np.logical_and(~isnan,L_shift))[0]

                zval = np.concatenate((lower,upper),dtype=int).reshape((2,-1)).T.flatten()

                yval = np.full(zval.size,index,dtype=float)
                
                yval[::2] = np.nan

                yvals.append(yval)
                zvals.append(zval)

            qvals = np.unique(np.concatenate(zvals))

            for (yval,zval) in zip(yvals,zvals):
                self.axis_nan.step(np.where(qvals==zval.reshape((-1,1)))[1],yval)

            self.axis_nan.set_xlim((-1,qvals.size))
            self.axis_nan.set_ylim((-1,len(las.running)))

            self.axis_nan.set_xticks(np.arange(qvals.size))
            self.axis_nan.set_xticklabels(depth[qvals],rotation=90)

            self.axis_nan.set_yticks(np.arange(len(las.running)))
            self.axis_nan.set_yticklabels(las.headers)

            self.axis_nan.grid(True,which="both",axis='x')

            self.fig_nan.tight_layout()

        def set_DepthView(self,plot_dictionary):

            self.plot = plot_dictionary

            self.DV_num_axes = len(plot_dictionary)

            zmult = int((self.bottom-self.top)/20.)
            
            self.spinepos = [1+x/zmult for x in self.spinerelpos]

            self.fig = plt.figure()

            self.fig.set_figwidth(2*self.DV_num_axes)
            self.fig.set_figheight(8*zmult)

            self.grids = gridspec.GridSpec(1,self.DV_num_axes)
            self.grids.update(wspace=0)

            self.set_DepthViewAxes()
            self.set_DepthViewLines()

        def set_DepthViewAxes(self):

            self.axes = []

            for index in range(self.DV_num_axes):

                axis = plt.subplot(self.grids[index])
                
                axis.set_xticks([])
                
                axis.grid(True,which="both",axis='y')

                for tic in axis.yaxis.get_major_ticks():
                    if index>0:
                        tic.label1.set_visible(False)
                    tic.tick1line.set_visible(False)

                axis.subax = []

                for _ in range(len(self.plot[index]["lines"])):
                    axis.subax.append(axis.twiny())

                self.axes.append(axis)

        def set_DepthViewLines(self):

            yticks = self.get_yticks()

            for indexI,axdict in enumerate(self.plot):

                for indexJ,line in enumerate(axdict["lines"]):
                
                    depth = self.frames[line[0]].columns(0)
                        
                    xvals = self.frames[line[0]].columns(line[1])

                    indexK = self.frames[line[0]].headers.index(line[1])

                    mnem = self.frames[line[0]].headers[indexK]
                    unit = self.frames[line[0]].units[indexK]

                    linestyle = "-" if indexJ==0 else "--"

                    if axdict["ptype"][indexJ] is None:
                        self.axes[indexI].subax[indexJ].plot(
                            xvals,depth,color=self.lineColors[indexJ],linestyle=linestyle)
                    elif axdict["ptype"][indexJ]=="log":
                        self.axes[indexI].subax[indexJ].semilogx(
                            xvals,depth,color=self.lineColors[indexJ],linestyle=linestyle)

                    xticks = self.get_xticks(xvals,indexI,indexJ)

                    self.axes[indexI].subax[indexJ].set_xlim([xticks.min(),xticks.max()])
                    self.axes[indexI].subax[indexJ].set_xticks(xticks)

                    self.axes[indexI].subax[indexJ].set_ylim([yticks.max(),yticks.min()])
                    self.axes[indexI].subax[indexJ].set_yticks(yticks)

                    self.axes[indexI].subax[indexJ].grid(True,which="both",axis='y')

                    self.axes[indexI].subax[indexJ].yaxis.set_minor_locator(AutoMinorLocator(10))

                    for tic in self.axes[indexI].yaxis.get_minor_ticks():
                        if indexI>0:
                            tic.tick1line.set_visible(False)

                    if indexJ==0:

                        self.axes[indexI].subax[indexJ].grid(True,which="major",axis='x')

                        if axdict["ptype"][indexJ]=="log":

                            self.axes[indexI].subax[indexJ].grid(True,which="minor",axis='x')

                            minorTicks = self.axes[indexI].subax[indexJ].xaxis.get_minor_ticks()

                            for tic in minorTicks:
                                tic.label2.set_visible(False)
                                tic.tick2line.set_visible(False)

                    else:
                        self.axes[indexI].subax[indexJ].spines["top"].set_position(("axes",self.spinepos[indexJ]))
                        self.axes[indexI].subax[indexJ].spines["top"].set_color(self.lineColors[indexJ])
                        self.axes[indexI].subax[indexJ].tick_params(axis='x',color=self.lineColors[indexJ],labelcolor=self.lineColors[indexJ])

                    # box = self.axes[indexI].subax[indexJ].xaxis.set_clip_box(dict(facecolor='none', edgecolor='black'))
                    # box.set_bbox(dict(facecolor='none', edgecolor='black'))

                    if axdict["ptype"][indexJ] is None:
                        self.axes[indexI].subax[indexJ].xaxis.set_major_formatter(ScalarFormatter())
                    elif axdict["ptype"][indexJ]=="log":
                        self.axes[indexI].subax[indexJ].xaxis.set_major_formatter(LogFormatter())

                    self.axes[indexI].subax[indexJ].set_xlabel("{} {}".format(mnem,unit),color=self.lineColors[indexJ])

                    majorTicksX = self.axes[indexI].subax[indexJ].xaxis.get_major_ticks()

                    for tic in majorTicksX:
                        tic.label2.set_visible(False)
                        tic.tick2line.set_visible(False)

                    majorTicksX[0].label2.set_visible(True)
                    majorTicksX[0].tick2line.set_visible(True)

                    majorTicksX[-1].label2.set_visible(True)
                    majorTicksX[-1].tick2line.set_visible(True)

                    plt.setp(self.axes[indexI].subax[indexJ].xaxis.get_majorticklabels()[0],ha="left")
                    plt.setp(self.axes[indexI].subax[indexJ].xaxis.get_majorticklabels()[-1],ha="right")

        def set_DepthViewLine(self,xvals,depth,indexI,indexJ):

            # indexI index of axis in the plot
            # indexJ index of line in the axis

            self.axes[indexI].subax[indexJ].plot(xvals,depth,
                color=self.lineColors[indexJ],linestyle="--")

        def get_yticks(self):

            ymin = np.floor(self.top/20)*20

            ymax = np.ceil(self.bottom/20)*20

            yticks = np.arange(ymin,ymax+5,10)

            return yticks
                    
        def get_xticks(self,xvals,indexI,indexJ,xunits_count_default=11):

            if self.plot[indexI]["xlims"][indexJ] is not None:

                if self.plot[indexI]["ptype"][indexJ] is None:
                    xmin,xmax,xunits_size = self.plot[indexI]["xlims"][indexJ]
                elif self.plot[indexI]["ptype"][indexJ]=="log":
                    xmin,xmax = self.plot[indexI]["xlims"][indexJ]

            else:

                xvals_min = np.nanmin(xvals)
                xvals_max = np.nanmax(xvals)

                xrange_given = xvals_max-xvals_min
                
                xunits_size = xrange_given/(xunits_count_default-1)

                beforeDot,afterDot = format(xunits_size,'f').split('.')

                nondim_xunit_sizes = np.array([1,2,4,5,10])

                if xunits_size>1:
                    xunits_size_temp = xunits_size/10**(len(beforeDot)-1)
                    xunits_size_temp = nondim_xunit_sizes[(np.abs(nondim_xunit_sizes-xunits_size_temp)).argmin()]
                    xunits_size = xunits_size_temp*10**(len(beforeDot)-1)
                else:
                    zeroCountAfterDot = len(afterDot)-len(afterDot.lstrip('0'))
                    xunits_size_temp = xunits_size*10**(zeroCountAfterDot+1)
                    xunits_size_temp = nondim_xunit_sizes[(np.abs(nondim_xunit_sizes-xunits_size_temp)).argmin()]
                    xunits_size = xunits_size_temp/10**(zeroCountAfterDot+1)

                if self.plot[indexI]["ptype"][indexJ] is None:

                    xmin = (np.floor(xvals_min/xunits_size)-1).astype(float)*xunits_size
                    xmax = (np.ceil(xvals_max/xunits_size)+1).astype(float)*xunits_size

                elif self.plot[indexI]["ptype"][indexJ]=="log":

                    xmin = xvals_min if xvals_min>0 else 0.001
                    xmax = xvals_max if xvals_max>0 else 0.1
                
            if self.plot[indexI]["ptype"][indexJ] is None:

                xticks = np.arange(xmin,xmax+xunits_size/2,xunits_size)

            elif self.plot[indexI]["ptype"][indexJ]=="log":

                xmin_power = np.floor(np.log10(xmin))
                xmax_power = np.ceil(np.log10(xmax))

                xticks = 10**np.arange(xmin_power,xmax_power+1/2)

            return xticks

        def set_DepthViewGRcut(self,GRline,indexI,indexJ,perc_cut=40):

            # indexI index of GR containing axis in the plot
            # indexJ index of GR containing line in the axis

            try:
                depth = self.frames[GRline[0]].columns("MD")
            except ValueError:
                depth = self.frames[GRline[0]].columns("DEPT")

            xvals = self.frames[GRline[0]].columns(GRline[1])

            GRmin = np.nanmin(xvals)
            GRmax = np.nanmax(xvals)

            GRcut = (GRmin+(GRmax-GRmin)*perc_cut/100)

            cut_line = GRcut*np.ones(depth.shape)

            cond_clean = cut_line>=xvals

            indexTop = []
            indexBtm = []

            for i,cond in enumerate(cond_clean):
                
                if i>0:
                    old_cond = cond_clean[i-1]
                else:
                    old_cond = False
                    
                try:
                    new_cond = cond_clean[i+1]
                except IndexError:
                    new_cond = False
                    
                if cond and not old_cond:
                    indexTop.append(i)

                if cond and not new_cond:
                    indexBtm.append(i)

            net_pay = 0

            for i,j in zip(indexTop,indexBtm):

                net_pay += depth[j]-depth[i]

            self.axes[indexI].subax[indexJ].fill_betweenx(
                depth,xvals,x2=cut_line,where=cond_clean,color=self.color_clean)

            self.netPayThickness = net_pay
            self.netToGrossRatio = net_pay/self.gross_thickness*100

            return GRcut

        def get_GRcut(self,GRline,depth=("None",None,None),perc_cut=40):

            xvals = self.get_interval(*depth[1:],idframes=GRline[0],curveID=GRline[1])[0]

            GRmin = np.nanmin(xvals)
            GRmax = np.nanmax(xvals)

            GRcut = (GRmin+(GRmax-GRmin)*perc_cut/100)

            return GRcut

        def get_ShaleVolumeGR(self,GRline,GRmin=None,GRmax=None,model=None):

            xvals = self.frames[GRline[0]][GRline[1]]

            if GRmin is None:
                GRmin = np.nanmin(xvals)

            if GRmax is None:
                GRmax = np.nanmax(xvals)

            Ish = (xvals-GRmin)/(GRmax-GRmin)

            if model is None or model=="linear":
                Vsh = Ish

            return Vsh

        def get_ShaleVolumeSP(self,SPline,SPsand,SPshale):

            xvals = self.frames[SPline[0]][SPline[1]]

            Vsh = (xvals-SPsand)/(SPshale-SPsand)

            return Vsh

        def set_DepthViewNeuPorCorr(self,NeuPorLine,indexI,indexJ,Vsh,NeuPorShale):

            # indexI index of Neutron Porosity containing axis in the plot
            # indexJ index of Neutron Porosity containing line in the axis

            try:
                depth = self.frames[NeuPorLine[0]]["MD"]
            except KeyError:
                depth = self.frames[NeuPorLine[0]]["DEPT"]

            xvals = self.frames[NeuPorLine[0]][NeuPorLine[1]]

            NeuPorCorr = xvals-Vsh*NeuPorShale

            self.axes[indexI].subax[indexJ].plot(NeuPorCorr,depth,
                color=self.lineColors[indexJ],linestyle="--")

        def set_DepthViewResistivityCut(self,ResLine,indexI,indexJ,ohmm_cut=10):

            # indexI index of Resistivity containing axis in the plot
            # indexJ index of Resistivity containing line in the axis

            depth = self.frames[ResLine[0]].columns(0)

            xvals = self.frames[ResLine[0]].columns(ResLine[1])

            cut_line = ohmm_cut*np.ones(depth.shape)

            self.axes[indexI].subax[indexJ].fill_betweenx(
                depth,xvals,x2=cut_line,where=ohmm_cut<=xvals,color=self.color_HC)

        def set_DepthViewSaturationCut(self,SwLine,indexI,indexJ,Sw_cut=0.5):

            # indexI index of Resistivity containing axis in the plot
            # indexJ index of Resistivity containing line in the axis

            depth = self.frames[SwLine[0]].columns(0)

            xvals = self.frames[SwLine[0]].columns(SwLine[1])

            cut_line = Sw_cut*np.ones(depth.shape)

            self.axes[indexI].subax[indexJ].fill_betweenx(
                depth,xvals,x2=cut_line,where=Sw_cut>=xvals,color=self.color_HC)

        def set_DepthViewNMRfluid(self,NMRline,indexI,water_clay,water_capi,water_move,HC):

            # indexL index of NMR containing lasio in the pack
            # indexI index of NMR containing axis in the plot

            try:
                depth = self.frames[NMRline]["MD"]
            except KeyError:
                depth = self.frames[NMRline]["DEPT"]

            xvals0 = np.zeros(water_clay.shape)
            xvals1 = water_clay
            xvals2 = water_clay+water_capi
            xvals3 = water_clay+water_capi+water_move
            xvals4 = water_clay+water_capi+water_move+HC

            self.axes[indexI].subax[0].fill_betweenx(
                depth,xvals1,x2=xvals0,where=xvals0<=xvals1,color=self.color_waterclay)

            self.axes[indexI].subax[0].fill_betweenx(
                depth,xvals2,x2=xvals1,where=xvals1<=xvals2,color=self.color_watercapi)

            self.axes[indexI].subax[0].fill_betweenx(
                depth,xvals3,x2=xvals2,where=xvals2<=xvals3,color=self.color_watermove)

            self.axes[indexI].subax[0].fill_betweenx(
                depth,xvals4,x2=xvals3,where=xvals3<=xvals4,color=self.color_HC)

        def set_DepthViewPerfs(self,indexI,indexJ,depths,perfs):

            xtick = self.axes[indexI].subax[indexJ].get_xticks()

            ytick = self.axes[indexI].subax[indexJ].get_yticks()

            perfs = np.array(perfs)

            perfs_just = perfs[perfs>0]

            perfs_just[::10] -= perfs_just[::10]*0.5

            perfs[perfs>0] = perfs_just

            perfs_scaled = xtick.min()+(xtick.max()-xtick.min())/10/(perfs.max()-perfs.min())*perfs

            # pfgun_point = xtick.min()

            # for arg in args:

            #     depths = np.arange(arg[0],arg[1]+1/2,1.)

            #     for index,depth in enumerate(depths):

            #         if index==0:
            #             marker,size = 11,10
            #         elif index==len(depths)-1:
            #             marker,size = 10,10
            #         else:
            #             marker,size = 9,10

            #         self.axes[indexI].subax[indexJ].plot(pfgun_point,depth,
            #             marker=marker,color='orange',markersize=size,markerfacecolor='black')

            self.axes[indexI].subax[indexJ].plot(perfs_scaled,depths)

        def set_DepthViewCasing(self):
            """It creates an axis to include casing set depths"""

            pass

        def set_GammaSpectralCP(self):

            self.fig_gscp,self.axis_gscp = plt.subplots()

        def set_DenNeuCP(self):

            self.fig_dncp,self.axis_dncp = plt.subplots()

        def set_SonDenCP(self):

            self.fig_sdcp,self.axis_sdcp = plt.subplots()

        def set_SonNeuCP(self,
            porLine,
            sonLine,
            a_SND=+0.00,
            a_LMS=+0.00,
            a_DOL=-0.06,
            b_SND=+0.90,
            b_LMS=+0.80,
            b_DOL=+0.84,
            p_SND=+0.02,
            p_LMS=+0.00,
            p_DOL=-0.01,
            DT_FLUID=189,
            DT_SND=55.6,
            DT_LMS=47.5,
            DT_DOL=43.5,
            xmin=None,
            ymin=None,
            xmax=None,
            ymax=None,
            rotate=0):

            self.fig_sncp,self.axis_sncp = plt.subplots()

            self.fig_sncp.set_figwidth(5)
            self.fig_sncp.set_figheight(6)

            c1_SND = 10**((a_LMS-a_SND)/b_LMS)
            c1_LMS = 10**((a_LMS-a_LMS)/b_LMS)
            c1_DOL = 10**((a_LMS-a_DOL)/b_LMS)

            c2_SND = b_SND/b_LMS
            c2_LMS = b_LMS/b_LMS
            c2_DOL = b_DOL/b_LMS

            porSND = np.linspace(0,0.45,46)
            porLMS = np.linspace(0,0.45,46)
            porDOL = np.linspace(0,0.45,46)

            sonicSND = porSND*(DT_FLUID-DT_SND)+DT_SND
            sonicLMS = porLMS*(DT_FLUID-DT_LMS)+DT_LMS
            sonicDOL = porDOL*(DT_FLUID-DT_DOL)+DT_DOL

            porLMS_SND = c1_SND*(porSND)**c2_SND-p_SND
            porLMS_LMS = c1_LMS*(porLMS)**c2_LMS-p_LMS
            porLMS_DOL = c1_DOL*(porDOL)**c2_DOL-p_DOL

            xaxis_max = 0.5
            yaxis_max = 110

            for depth in self.depths:

                xaxis = self.get_interval(*depth[1:],idframe=porLine[0],curveID=porLine[1])
                yaxis = self.get_interval(*depth[1:],idframe=sonLine[0],curveID=sonLine[1])

                xaxis_max = max((xaxis_max,xaxis[0].max()))
                yaxis_max = max((yaxis_max,yaxis[0].max()))

                self.axis_sncp.scatter(xaxis,yaxis,s=1,label=depth[0])

            self.axis_sncp.legend(scatterpoints=10)

            self.axis_sncp.plot(porLMS_SND,sonicSND,color='blue',linewidth=0.3)
            self.axis_sncp.plot(porLMS_LMS,sonicLMS,color='blue',linewidth=0.3)
            self.axis_sncp.plot(porLMS_DOL,sonicDOL,color='blue',linewidth=0.3)

            self.axis_sncp.scatter(porLMS_SND[::5],sonicSND[::5],marker=(2,0,45),color="blue")
            self.axis_sncp.scatter(porLMS_LMS[::5],sonicLMS[::5],marker=(2,0,45),color="blue")
            self.axis_sncp.scatter(porLMS_DOL[::5],sonicDOL[::5],marker=(2,0,45),color="blue")

            self.axis_sncp.text(porLMS_SND[27],sonicSND[26],'Sandstone',rotation=rotate)
            self.axis_sncp.text(porLMS_LMS[18],sonicLMS[17],'Calcite (limestone)',rotation=rotate)
            self.axis_sncp.text(porLMS_DOL[19],sonicDOL[18],'Dolomite',rotation=rotate)

            self.axis_sncp.set_xlabel("Apparent Limestone Neutron Porosity")
            self.axis_sncp.set_ylabel("Sonic Transit Time $\\Delta$t [$\\mu$s/ft]")

            xaxis_min = -0.05 if xmin is None else xmin
            yaxis_min = +40.0 if ymin is None else ymin

            xaxis_max = xaxis_max if xmax is None else xmax
            yaxis_max = yaxis_max if ymax is None else ymax

            self.axis_sncp.set_xlim([xaxis_min,xaxis_max])
            self.axis_sncp.set_ylim([yaxis_min,yaxis_max])

            self.axis_sncp.xaxis.set_minor_locator(AutoMinorLocator(10))
            self.axis_sncp.yaxis.set_minor_locator(AutoMinorLocator(10))

            self.axis_sncp.grid(True,which="both",axis='both')

            self.fig_sncp.tight_layout()

        def set_DenPheCP(self):

            # density photoelectric cross section cross plot

            self.fig_dpcp,self.axis_dpcp = plt.subplots()

        def set_MNplot(self):

            self.fig_mncp,self.axis_mncp = plt.subplots()

        def set_MIDplot(self):

            self.fig_midp,self.axis_midp = plt.subplots()

        def set_rhomaaUmaa(self):

            self.fig_rhoU,self.axis_rhoU = plt.subplots()

        def set_PickettCP(
            self,
            resLine,
            phiLine,
            returnSwFlag=False,
            showDiffSwFlag=True,
            m=2,
            n=2,
            a=0.62,
            Rw=0.1,
            xmin=None,
            xmax=None,
            ymin=None,
            ymax=None,
            GRconds=None,
            ):

            if returnSwFlag:

                xvalsR = self.frames[resLine[0]].columns(resLine[1])
                xvalsP = self.frames[phiLine[0]].columns(phiLine[1])

                Sw_calculated = ((a*Rw)/(xvalsR*xvalsP**m))**(1/n)

                Sw_calculated[Sw_calculated>1] = 1

                return Sw_calculated

            else:

                self.fig_pcp,self.axis_pcp = plt.subplots()

                xaxis_min = 1
                xaxis_max = 100

                yaxis_min = 0.1
                yaxis_max = 1

                for depth in self.depths:

                    xaxis = self.get_interval(*depth[1:],idframes=resLine[0],curveID=resLine[1])[0]
                    yaxis = self.get_interval(*depth[1:],idframes=phiLine[0],curveID=phiLine[1])[0]

                    xaxis_min = min((xaxis_min,xaxis.min()))
                    xaxis_max = max((xaxis_max,xaxis.max()))

                    yaxis_min = min((yaxis_min,yaxis.min()))
                    yaxis_max = max((yaxis_max,yaxis.max()))

                    if GRconds is not None:
                        self.axis_pcp.scatter(xaxis[GRconds],yaxis[GRconds],s=1,label="{} clean".format(depth[0]))
                        self.axis_pcp.scatter(xaxis[~GRconds],yaxis[~GRconds],s=1,label="{} shaly".format(depth[0]))
                    else:
                        self.axis_pcp.scatter(xaxis,yaxis,s=1,label=depth[0])

                self.axis_pcp.legend(scatterpoints=10)

                indexR = self.frames[resLine[0]].headers.index(resLine[1])
                indexP = self.frames[phiLine[0]].headers.index(phiLine[1])

                mnemR = self.frames[resLine[0]].headers[indexR]
                unitR = self.frames[resLine[0]].units[indexR]

                mnemP = self.frames[phiLine[0]].headers[indexP]
                unitP = self.frames[phiLine[0]].units[indexP]

                xaxis_min = xmin if xmin is not None else xaxis_min
                xaxis_max = xmax if xmax is not None else xaxis_max

                yaxis_min = ymin if ymin is not None else yaxis_min
                yaxis_max = ymax if ymax is not None else yaxis_max

                resexpmin = np.floor(np.log10(xaxis_min))
                resexpmax = np.ceil(np.log10(xaxis_max))

                if showDiffSwFlag:

                    resSw = np.logspace(resexpmin,resexpmax,100)

                    Sw75,Sw50,Sw25 = 0.75,0.50,0.25

                    philine_atSw100 = (a*Rw/resSw)**(1/m)

                    philine_atSw075 = philine_atSw100*Sw75**(-n/m)
                    philine_atSw050 = philine_atSw100*Sw50**(-n/m)
                    philine_atSw025 = philine_atSw100*Sw25**(-n/m)

                    self.axis_pcp.plot(resSw,philine_atSw100,c="black",linewidth=1)#,label="100% Sw")
                    self.axis_pcp.plot(resSw,philine_atSw075,c="blue",linewidth=1)#,label="75% Sw")
                    self.axis_pcp.plot(resSw,philine_atSw050,c="blue",linewidth=1)#,label="50% Sw")
                    self.axis_pcp.plot(resSw,philine_atSw025,c="blue",linewidth=1)#,label="25% Sw")

                phiexpmin = np.floor(np.log10(yaxis_min))
                phiexpmax = np.ceil(np.log10(yaxis_max))

                xticks = 10**np.arange(resexpmin,resexpmax+1/2)
                yticks = 10**np.arange(phiexpmin,phiexpmax+1/2)

                self.axis_pcp.set_xscale('log')
                self.axis_pcp.set_yscale('log')

                self.axis_pcp.set_xlim([xticks.min(),xticks.max()])
                self.axis_pcp.set_xticks(xticks)

                self.axis_pcp.set_ylim([yticks.min(),yticks.max()])
                self.axis_pcp.set_yticks(yticks)

                self.axis_pcp.xaxis.set_major_formatter(LogFormatter())
                self.axis_pcp.yaxis.set_major_formatter(LogFormatter())

                for tic in self.axis_pcp.xaxis.get_minor_ticks():
                    tic.label1.set_visible(False)
                    tic.tick1line.set_visible(False)

                for tic in self.axis_pcp.yaxis.get_minor_ticks():
                    tic.label1.set_visible(False)
                    tic.tick1line.set_visible(False)

                self.axis_pcp.set_xlabel("{} {}".format(mnemR,unitR))
                self.axis_pcp.set_ylabel("{} {}".format(mnemP,unitP))

                self.axis_pcp.grid(True,which="both",axis='both')

        def set_HingleCP(self):

            self.fig_hcp,self.axis_hcp = plt.subplots()

    return LogViewClass

def PerfView(data=None):

    base = getdata(data)

    class PerfViewClass(base):
        
        pass

    return PerfViewClass

def View3D(data=None):

    base = getdata(data)

    class View3DClass(base):

        def __init__(self,window,**kwargs):

            super().__init__(**kwargs)

            self.dirname = os.path.dirname(__file__)

            self.root = window

        def set_plot(self):

            self.pane_EW = ttk.PanedWindow(self.root,orient=tk.HORIZONTAL)

            self.frame_side = ttk.Frame(self.root)

            self.pane_EW.add(self.frame_side,weight=1)

            self.frame_plot = ttk.Frame(self.root)

            self.pane_EW.add(self.frame_plot,weight=1)

            self.pane_EW.pack(side=tk.LEFT,expand=1,fill=tk.BOTH)

            self.frame_plot.columnconfigure(0,weight=1)
            self.frame_plot.columnconfigure(1,weight=0)

            self.frame_plot.rowconfigure(0,weight=1)
            self.frame_plot.rowconfigure(1,weight=0)

            self.figure = plt.Figure()
            self.canvas = FigureCanvasTkAgg(self.figure,self.frame_plot)

            self.plotbox = self.canvas.get_tk_widget()
            self.plotbox.grid(row=0,column=0,sticky=tk.NSEW)        

            self.plotbar = VerticalNavigationToolbar2Tk(self.canvas,self.frame_plot)
            self.plotbar.update()
            self.plotbar.grid(row=0,column=1,sticky=tk.N)

            self.itembox = AutocompleteEntryListbox(self.frame_side,height=250,padding=0)

            self.itembox.content = self.itemnames.tolist()
            self.itembox.config(completevalues=self.itembox.content,allow_other_values=True)

            self.itembox.listbox.bind('<<ListboxSelect>>',lambda event: self.set_object(event))

            self.itembox.pack(expand=1,fill=tk.BOTH)

        def set_object(self,event):

            pass

    return View3DClass

def TableView(data=None):

    base = getdata(data)

    class TableViewClass(base):

        def __init__(self,**kwargs):

            super().__init__(**kwargs)

            self.dirname = os.path.dirname(__file__)

        def draw(self,func=None):

            self.scrollbar = tk.Scrollbar(self.root)

            self.columns = ["#"+str(idx) for idx,_ in enumerate(self.headers,start=1)]

            self.tree = ttk.Treeview(self.root,columns=self.columns,show="headings",selectmode="browse",yscrollcommand=self.scrollbar.set)

            self.sortReverseFlag = [False for column in self.columns]

            for idx,(column,header) in enumerate(zip(self.columns,self.headers)):
                self.tree.column(column,anchor=tk.W,stretch=tk.NO)
                self.tree.heading(column,text=header,anchor=tk.W)

            self.tree.column(self.columns[-1],stretch=tk.YES)

            self.tree.pack(side=tk.LEFT,expand=1,fill=tk.BOTH)

            self.scrollbar.pack(side=tk.LEFT,fill=tk.Y)

            self.scrollbar.config(command=self.tree.yview)

            # self.frame = tk.Frame(self.root,width=50)
            # self.frame.configure(background="white")
            # self.frame.pack(side=tk.LEFT,fill=tk.Y)

            self.tree.bind("<KeyPress-i>",self.addItem)

            # self.button_Add = tk.Button(self.frame,text="Add Item",width=50,command=self.addItem)
            # self.button_Add.pack(side=tk.TOP,ipadx=5,padx=10,pady=(5,1))

            self.tree.bind("<KeyPress-e>",self.editItem)
            self.tree.bind("<Double-1>",self.editItem)

            self.tree.bind("<Delete>",self.deleteItem)

            self.tree.bind("<KeyPress-j>",self.moveDown)
            self.tree.bind("<KeyPress-k>",self.moveUp)

            self.tree.bind("<Button-1>",self.sort_column)

            self.tree.bind("<Control-KeyPress-s>",lambda event: self.saveChanges(func,event))

            # self.button_Save = tk.Button(self.frame,text="Save Changes",width=50,command=lambda: self.saveChanges(func))
            # self.button_Save.pack(side=tk.TOP,ipadx=5,padx=10,pady=(10,1))

            self.root.protocol('WM_DELETE_WINDOW',lambda: self.close_no_save(func))

            self.counter = self.running[0].size

            self.iids = np.arange(self.counter)

            self.added = []
            self.edited = []
            self.deleted = []

            self.refill()

        def refill(self):

            self.tree.delete(*self.tree.get_children())

            rows = np.array(self.running).T.tolist()

            for iid,row in zip(self.iids,rows):
                self.tree.insert(parent="",index="end",iid=iid,values=row)

        def addItem(self,event):

            if hasattr(self,"topAddItem"):
                if self.topAddItem.winfo_exists():
                    return

            self.topAddItem = tk.Toplevel()

            self.topAddItem.resizable(0,0)

            for index,header in enumerate(self.headers):
                label = "label_"+str(index)
                entry = "entry_"+str(index)
                pady = (30,5) if index==0 else (5,5)
                setattr(self.topAddItem,label,tk.Label(self.topAddItem,text=header,font="Helvetica 11",width=20,anchor=tk.E))
                setattr(self.topAddItem,entry,tk.Entry(self.topAddItem,width=30,font="Helvetica 11"))
                getattr(self.topAddItem,label).grid(row=index,column=0,ipady=5,padx=(10,5),pady=pady)
                getattr(self.topAddItem,entry).grid(row=index,column=1,ipady=5,padx=(5,10),pady=pady)

            self.topAddItem.entry_0.focus()

            self.topAddItem.button = tk.Button(self.topAddItem,text="Add Item",command=self.addItemEnterClicked)
            self.topAddItem.button.grid(row=index+1,column=0,columnspan=2,ipady=5,padx=15,pady=(15,30),sticky=tk.EW)

            self.topAddItem.button.bind('<Return>',self.addItemEnterClicked)

            self.topAddItem.mainloop()

        def addItemEnterClicked(self,event=None):

            if event is not None and event.widget!=self.topAddItem.button:
                return

            values = []

            for idx,header in enumerate(self.headers):
                entry = "entry_"+str(idx)
                value = getattr(self.topAddItem,entry).get()
                values.append(value)

            self.added.append(self.counter)

            self.set_rows(values)

            self.iids = np.append(self.iids,self.counter)

            self.tree.insert(parent="",index="end",iid=self.counter,values=values)

            self.counter += 1

            self.topAddItem.destroy()

        def editItem(self,event):

            region = self.tree.identify('region',event.x,event.y)

            if region=="separator":
                self.autowidth(event)
                return

            if not(region=="cell" or event.char=="e"):
                return

            if hasattr(self,"topEditItem"):
                if self.topEditItem.winfo_exists():
                    return

            if not self.tree.selection():
                return
            else:
                item = self.tree.selection()[0]

            values = self.tree.item(item)['values']

            self.topEditItem = tk.Toplevel()

            self.topEditItem.resizable(0,0)

            for idx,(header,explicit) in enumerate(zip(self.headers,self.headers)):
                label = "label_"+str(idx)
                entry = "entry_"+str(idx)
                pady = (30,5) if idx==0 else (5,5)
                setattr(self.topEditItem,label,tk.Label(self.topEditItem,text=explicit,font="Helvetica 11",width=20,anchor=tk.E))
                setattr(self.topEditItem,entry,tk.Entry(self.topEditItem,width=30,font="Helvetica 11"))
                getattr(self.topEditItem,label).grid(row=idx,column=0,ipady=5,padx=(10,5),pady=pady)
                getattr(self.topEditItem,entry).grid(row=idx,column=1,ipady=5,padx=(5,10),pady=pady)
                getattr(self.topEditItem,entry).insert(0,values[idx])

            self.topEditItem.entry_0.focus()

            self.topEditItem.button = tk.Button(self.topEditItem,text="Save Item Edit",command=lambda: self.editItemEnterClicked(item))
            self.topEditItem.button.grid(row=idx+1,column=0,columnspan=2,ipady=5,padx=15,pady=(15,30),sticky=tk.EW)

            self.topEditItem.button.bind('<Return>',lambda event: self.editItemEnterClicked(item,event))

            self.topEditItem.mainloop()

        def editItemEnterClicked(self,item,event=None):

            if event is not None and event.widget!=self.topEditItem.button:
                return

            values = []

            for idx,header in enumerate(self.headers):
                entry = "entry_"+str(idx)
                value = getattr(self.topEditItem,entry).get()
                values.append(value)

            self.edited.append([int(item),self.tree.item(item)["values"]])

            self.set_rows(values,np.argmax(self.iids==int(item)))

            self.tree.item(item,values=values)

            self.topEditItem.destroy()

        def deleteItem(self,event):

            if not self.tree.selection():
                return
            else:
                item = self.tree.selection()[0]

            self.deleted.append([int(item),self.tree.item(item)["values"]])

            self.del_rows(np.argmax(self.iids==int(item)),inplace=True)

            self.iids = np.delete(self.iids,np.argmax(self.iids==int(item)))

            self.tree.delete(item)

        def autowidth(self,event):

            column = self.tree.identify('column',event.x,event.y)

            index = self.columns.index(column)

            if index==len(self.columns)-1:
                return

            header_char_count = len(self.headers[index])

            vcharcount = np.vectorize(lambda x: len(x))

            if self.running[index].size != 0:
                column_char_count = vcharcount(self.running[index].astype(str)).max()
            else:
                column_char_count = 0

            char_count = max(header_char_count,column_char_count)

            width = tkfont.Font(family="Consolas", size=12).measure("A"*char_count)

            column_width_old = self.tree.column(column,"width")

            self.tree.column(column,width=width)

            column_width_new = self.tree.column(column,"width")

            column_width_last_old = self.tree.column(self.columns[-1],"width")

            column_width_last_new = column_width_last_old+column_width_old-column_width_new

            self.tree.column(self.columns[-1],width=column_width_last_new)

        def moveUp(self,event):
     
            if not self.tree.selection():
                return
            else:
                item = self.tree.selection()[0]

            self.tree.move(item,self.tree.parent(item),self.tree.index(item)-1)

        def moveDown(self,event):

            if not self.tree.selection():
                return
            else:
                item = self.tree.selection()[0]

            self.tree.move(item,self.tree.parent(item),self.tree.index(item)+1)

        def sort_column(self,event):

            region = self.tree.identify('region',event.x,event.y)

            if region!="heading":
                return

            column = self.tree.identify('column',event.x,event.y)

            header_index = self.columns.index(column)

            reverseFlag = self.sortReverseFlag[header_index]

            N = self.running[0].size

            argsort = np.argsort(self.running[header_index])

            if reverseFlag:
                argsort = np.flip(argsort)

            for index,column in enumerate(self.running):
                self.running[index] = column[argsort]

            self.iids = self.iids[argsort]
            # indices = np.arange(N)

            # sort_indices = indices[np.argsort(argsort)]

            self.refill()

            # for item,sort_index in zip(self.iids,sort_indices):
            #     self.tree.move(item,self.tree.parent(item),sort_index)

            self.sortReverseFlag[header_index] = not reverseFlag

        def saveChanges(self,func=None,event=None):

            self.added = []
            self.edited = []
            self.deleted = []

            if func is not None:
                func()

        def close_no_save(self,func=None):

            try:
                for deleted in self.deleted:
                    self.set_rows(deleted[1])
            except:
                print("Could not bring back deleted rows ...")

            try:
                for edited in self.edited:
                    self.set_rows(edited[1],np.argmax(self.iids==edited[0]))
            except:
                print("Could not bring back editions ...")

            added = [np.argmax(self.iids==add) for add in self.added]

            try:
                self.del_rows(added,inplace=True)
            except:
                print("Could not remove additions ...")

            try:
                if func is not None:
                    func()
            except:
                print("Could not run the called function ...")

            self.root.destroy()

    return TableViewClass

def TreeView(data=None):

    base = getdata(data)

    class TreeViewClass(base):

        def __init__(self,dirpath):

            self.dirpath = dirpath

        def draw(self,window,func=None):

            self.root = window

            self.scrollbar = ttk.Scrollbar(self.root)

            self.tree = ttk.Treeview(self.root,show="headings tree",selectmode="browse",yscrollcommand=self.scrollbar.set)

            self.tree.pack(side=tk.LEFT,expand=1,fill=tk.BOTH)

            self.scrollbar.pack(side=tk.LEFT,fill=tk.Y)

            self.scrollbar.config(command=self.tree.yview)

            self.tree.bind("<Button-1>",lambda event: self.set_path(func,event))

            self.refill()

        def refill(self):

            self.tree.heading("#0",text="")

            self.tree.delete(*self.tree.get_children())

            iterator = os.walk(self.dirpath)

            parents_name = []
            parents_link = []

            counter  = 0

            while True:

                try:
                    root,dirs,frames = next(iterator)
                except StopIteration:
                    break

                if counter==0:
                    dirname = os.path.split(root)[1]
                    self.tree.heading("#0",text=dirname,anchor=tk.W)
                    parents_name.append(root)
                    parents_link.append("")
                
                parent = parents_link[parents_name.index(root)]

                for directory in dirs:
                    link = self.tree.insert(parent,'end',iid=counter,text=directory)
                    counter += 1

                    parents_name.append(os.path.join(root,directory))
                    parents_link.append(link)

                for file in frames:            
                    self.tree.insert(parent,'end',iid=counter,text=file)
                    counter += 1

        def set_path(self,func=None,event=None):

            if event is not None:
                region = self.tree.identify("region",event.x,event.y)
            else:
                return

            if region!="tree":
                return

            item = self.tree.identify("row",event.x,event.y)

            path = self.tree.item(item)['text']

            while True:

                item = self.tree.parent(item)

                if item:
                    path = os.path.join(self.tree.item(item)['text'],path)
                else:
                    path = os.path.join(self.dirpath,path)
                    break

            if func is not None:
                func(path)
            else:
                print(path)

    return TreeView

# Supporting Plot Functions

def ternary(axis,p1,p2,p3,number):

    index = np.arange(1,number)

    xs1 = p1[0]+index*(p2[0]-p1[0])/number
    xs2 = p2[0]+index*(p3[0]-p2[0])/number
    xs3 = p3[0]+index*(p1[0]-p3[0])/number

    ys1 = p1[1]+index*(p2[1]-p1[1])/number
    ys2 = p2[1]+index*(p3[1]-p2[1])/number
    ys3 = p3[1]+index*(p1[1]-p3[1])/number

    axis.plot([p1[0],p2[0]],[p1[1],p2[1]],'k',linewidth=0.5)
    axis.plot([p2[0],p3[0]],[p2[1],p3[1]],'k',linewidth=0.5)
    axis.plot([p3[0],p1[0]],[p3[1],p1[1]],'k',linewidth=0.5)

    for i in index:
        axis.plot([xs1[i-1],xs2[number-1-i]],[ys1[i-1],ys2[number-1-i]],'k',linewidth=0.5)
        axis.plot([xs2[i-1],xs3[number-1-i]],[ys2[i-1],ys3[number-1-i]],'k',linewidth=0.5)
        axis.plot([xs3[i-1],xs1[number-1-i]],[ys3[i-1],ys1[number-1-i]],'k',linewidth=0.5)

    return axis

# Supporting Tkinter Widgets

class VerticalNavigationToolbar2Tk(NavigationToolbar2Tk):

    def __init__(self,canvas,window):

        super().__init__(canvas,window,pack_toolbar=False)

        self.message = tk.StringVar(master=window)
        self._message_label = tk.Label(master=window,textvariable=self.message)
        self._message_label.grid(row=1,column=0,columnspan=2,sticky=tk.W)

    # override _Button() to re-pack the toolbar button in vertical direction
    def _Button(self,text,image_file,toggle,command):
        b = super()._Button(text,image_file,toggle,command)
        b.pack(side=tk.TOP) # re-pack button in vertical direction
        return b

    # override _Spacer() to create vertical separator
    def _Spacer(self):
        s = tk.Frame(self,width=26,relief=tk.RIDGE,bg="DarkGray",padx=2)
        s.pack(side=tk.TOP,pady=5) # pack in vertical direction
        return s

if __name__ == "__main__":

    pass
