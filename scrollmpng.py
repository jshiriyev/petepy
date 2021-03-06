import io

import logging

import os

import tkinter as tk

from matplotlib import gridspec
from matplotlib import pyplot
from matplotlib import transforms

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import LogFormatter
from matplotlib.ticker import LogFormatterExponent
from matplotlib.ticker import LogFormatterMathtext
from matplotlib.ticker import NullLocator
from matplotlib.ticker import ScalarFormatter

import numpy as np

from PIL import ImageTk, Image

if __name__ == "__main__":
    import setup

from textio import LogASCII

"""
1. DepthView should be a frame that can be added to any parent frame.
2. Axis and line numbers should not be predefined.
3. Adding axis should not affect previous axes.
4. Adding line should not affect previous lines.
5. DepthView should be added to graphics and inherit from the textio.
6. Depth axis must be unique!
7. x-axis grids must be the same for the axis on top of each other.
8. get_xticks() should be working perfectly for both normal and logarithmic scale
9. set_lines() should be working smoothly
10. set_listbox() should be adding {idfile: mnemonic} to the listbox
"""

class DepthView(LogASCII):

	def __init__(self,root,**kwargs):
		"""It initializes the DepthView with listbox and figure canvas."""

		super().__init__(**kwargs)

		self.root = root

		self.root.title("RockPy")

		icopath = os.path.join(os.path.dirname(__file__),"rockpy.ico")

		self.root.iconbitmap(icopath)

		# The main frame for the listbox

		self.framelist = tk.Frame(root,width=31*8)
		self.framelist.pack(side=tk.LEFT,fill=tk.Y,expand=0)

		self.listbox = tk.Listbox(self.framelist,width=31)
		self.listbox.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

		# The main frame for the plot canvas

		self.framefigs = tk.Frame(root)
		self.framefigs.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

		self.canvas = tk.Canvas(self.framefigs)

		self.canvas.grid(row=0,column=0,sticky=tk.NSEW)

		self.hscroll = tk.Scrollbar(self.framefigs,orient=tk.HORIZONTAL)
		self.vscroll = tk.Scrollbar(self.framefigs,orient=tk.VERTICAL)

		self.hscroll.grid(row=1,column=0,sticky=tk.EW)
		self.vscroll.grid(row=0,column=1,sticky=tk.NS)

		self.framefigs.rowconfigure(0,weight=1)
		self.framefigs.columnconfigure(0,weight=1)

		self.canvas.config(xscrollcommand=self.hscroll.set)
		self.canvas.config(yscrollcommand=self.vscroll.set)

		self.hscroll.config(command=self.canvas.xview)
		self.vscroll.config(command=self.canvas.yview)

		self.canvas.bind_all("<MouseWheel>",self._on_mousewheel)

		# The colors to be used for lines

		# self.colors = ("black","crimson","blue","sienna")
		self.colors = pyplot.rcParams['axes.prop_cycle'].by_key()['color']
		# self.colors.insert(0,"#000000")

	def set_listbox(self):

		pass

	def set_axes(self,numaxes=1,subaxes=None,depth=None,inchdepth=15.,width=3.,height=128.,dpi=100.):
		"""Creates the figure and axes and their sub-axes and stores them in the self.axes."""

		# numaxes 	: integer
		# 			 Number of axes in the figure

		# subaxes 	: list or tuple of integers
		# 			 Number of subaxes in each axis

		# depth 	: float
		# 			 Depth of log in meters; every inch will represent inchdepth meter of formation
		# 			 Default value for inchdepth is 15 meters.

		# inchdepth	: float
		# 			 The depth (meters) to be shown in every inch of the figure

		# width 	: float
		# 			 Width of each axis in inches

		# height 	: float
		# 			 Height of figure in inches

		# dpi 		: integer
		# 			 Resolution of the figure, dots per inches

		self.figure = pyplot.figure(dpi=dpi)

		self.figure.set_figwidth(width*numaxes)

		if depth is None:
			self.figure.set_figheight(height)
		else:
			self.figure.set_figheight(depth/inchdepth)

		self.fgspec = gridspec.GridSpec(1,numaxes)

		self.axes = []

		if subaxes is None:
			subaxes = (1,)*numaxes
		elif not hasattr(subaxes,"__len__"):
			logging.warning(f"Expected subaxes is a list or tuple with the length equal to numaxes; input is {type(subaxes)}")
		elif len(subaxes)!=numaxes:
			logging.warning(f"The length of subaxes should be equal to numaxes; {len(subaxes)} not equal to {numaxes=}")

		for idaxis in range(numaxes):
			self.add_axis(idaxis,subaxes[idaxis])

	def add_axis(self,idaxis,numsubaxes=1):
		"""Adds main-axis and its subaxes to the list of self.axes."""

		subaxes = []

		subaxis_main = pyplot.subplot(self.fgspec[idaxis])

		xlims = (0,1)

		ylims = (0,1)

		subaxis_main.set_xticks(np.linspace(*xlims,11))
		subaxis_main.set_yticks(ylims)

		subaxis_main.set_ylim(ylims[::-1])

		subaxis_main.yaxis.set_minor_locator(AutoMinorLocator(25))

		subaxis_main.grid(True,which="both",axis='y')

		subaxis_main.grid(True,which="major",axis='x')

		pyplot.setp(subaxis_main.get_xticklabels(),visible=False)
		pyplot.setp(subaxis_main.get_xticklines(),visible=False)

		# pyplot.setp(subaxis_main.xaxis.get_minorticklabels(),visible=False)
		# pyplot.setp(subaxis_main.xaxis.get_minorticklines(),visible=False)

		pyplot.setp(subaxis_main.yaxis.get_minorticklines(),visible=False)
		# subaxis_main.tick_params(axis='y',which='major',length=0)

		if idaxis>0:
			pyplot.setp(subaxis_main.get_yticklabels(),visible=False)

		subaxes.append(subaxis_main)

		self.axes.append(subaxes)

		self.set_subaxes(idaxis,numsubaxes)

	def set_subaxes(self,idaxis,numsubaxes):
		"""Creates subaxes and stores them in self.axes."""

		numsubaxes_current = len(self.axes[idaxis])-1

		if numsubaxes_current>=numsubaxes:
			return

		roofpos = 1+0.4*numsubaxes/self.figure.get_figheight()

		self.axes[idaxis][0].spines["top"].set_position(("axes",roofpos))

		for idline in range(numsubaxes_current,numsubaxes):
			self.add_subaxis(idaxis,idline)

	def add_subaxis(self,idaxis,idline):
		"""Adds subaxis to the self.axes."""

		axsub = self.axes[idaxis][0].twiny()

		axsub.set_xticks((0.,1.))
		axsub.set_ylim(self.axes[0][0].get_ylim())

		spinepos = 1+0.4*idline/self.figure.get_figheight()

		axsub.spines["top"].set_position(("axes",spinepos))
		axsub.spines["top"].set_color(self.colors[idline])

		axsub.spines["left"].set_visible(False)
		axsub.spines["right"].set_visible(False)
		axsub.spines["bottom"].set_visible(False)

		axsub.tick_params(axis='x',labelcolor=self.colors[idline])

		# self.axes[idaxis][0].yaxis.set_minor_locator(AutoMinorLocator(25))

		# self.axes[idaxis][0].grid(True,which="both",axis='y')

		pyplot.setp(self.axes[idaxis][0].get_xticklabels(),visible=False)
		pyplot.setp(self.axes[idaxis][0].get_xticklines(),visible=False)

		axsub.LineExistFlag = False

		self.set_xaxis(axsub)

		self.axes[idaxis].append(axsub)

	def set_depth(self,depth=None):
		"""It will check the depths of axis and set depth which include all depths."""

		for axis in self.axes:
			for axsub in axis:
				axsub.set_ylim(self.axes[0][0].get_ylim())

			# axis[0].yaxis.set_minor_locator(AutoMinorLocator(25))
			# axis[0].grid(True,which="both",axis='y')

	def set_xaxis(self,axis):

		pyplot.setp(axis.xaxis.get_majorticklabels()[1:-1],visible=False)

		pyplot.setp(axis.xaxis.get_majorticklabels()[0],ha="left")
		pyplot.setp(axis.xaxis.get_majorticklabels()[-1],ha="right")

		if not axis.LineExistFlag:

			loffset = transforms.ScaledTranslation(5/72,-5/72,self.figure.dpi_scale_trans)
			
			ltrans = axis.xaxis.get_majorticklabels()[0].get_transform()

			axis.xaxis.get_majorticklabels()[0].set_transform(ltrans+loffset)

			roffset = transforms.ScaledTranslation(-5/72,-5/72,self.figure.dpi_scale_trans)

			rtrans = axis.xaxis.get_majorticklabels()[-1].get_transform()

			axis.xaxis.get_majorticklabels()[-1].set_transform(rtrans+roffset)

		else:

			roffset = transforms.ScaledTranslation(-10/72,0,self.figure.dpi_scale_trans)

			rtrans = axis.xaxis.get_majorticklabels()[-1].get_transform()

			axis.xaxis.get_majorticklabels()[-1].set_transform(rtrans+roffset)

		pyplot.setp(axis.xaxis.get_majorticklines()[2:-1],visible=False)

		pyplot.setp(axis.xaxis.get_majorticklines()[1],markersize=25)
		pyplot.setp(axis.xaxis.get_majorticklines()[-1],markersize=25)

		# axis.xaxis.get_majorticklines()[0].set_markersize(100)

	def set_lines(self,idaxis,idline,xvals,yvals):

		axis = self.axes[idaxis][idline+1]

		axis.plot(xvals,yvals,color=self.colors[idline])

		axis.LineExistFlag = True

		yticks = self.get_yticks(yvals)
		xticks = self.get_xticks(xvals)

		# figheight_temp = (yticks.max()-yticks.min())/128

		# if figheight_temp>self.figure.get_figheight():
		# 	self.figure.set_figheight(figheight_temp)

		# figheight = max(self.figure.get_figheight(),figheight_temp)

		axis.set_ylim((yticks.max(),yticks.min()))
		axis.set_yticks(yticks)

		axis.set_xlim((xticks.min(),xticks.max()))
		axis.set_xticks(xticks)

		self.set_xaxis(axis)

		# axis.grid(True,which="both",axis='y')

		# axis.yaxis.set_minor_locator(AutoMinorLocator(10))

		# if idline==0:
			# axis.grid(True,which="major",axis='x')

		# axis.xaxis.set_major_formatter(ScalarFormatter())
		# # axis.xaxis.set_major_formatter(LogFormatter())

	def set_image(self):
		"""Creates the image of figure in memory and displays it on canvas."""

		self.fgspec.tight_layout(self.figure,rect=[0,0,1.0,0.995])
		self.fgspec.update(wspace=0)

		buff = io.BytesIO()

		self.figure.savefig(buff,format='png')

		buff.seek(0)

		self.image = ImageTk.PhotoImage(Image.open(buff))

		self.canvas.create_image(0,0,anchor=tk.NW,image=self.image)

		self.canvas.config(scrollregion=self.canvas.bbox('all'))

	def get_xticks(self,xvals,xmin=None,xmax=None,xscale="normal",xdelta=None,xdelta_count=11):

		xvals_min = np.nanmin(xvals)

		if xvals_min is np.nan:
			xvals_min = 0.

		xvals_max = np.nanmax(xvals)

		if xvals_max is np.nan:
			xvals_max= 1.

		xrange_given = xvals_max-xvals_min

		if xdelta is None:
			xdelta = xrange_given/(xdelta_count-1)

		beforeDot,afterDot = format(xdelta,'f').split('.')

		nondim_xunit_sizes = np.array([1,2,4,5,10])

		if xdelta>1:

		    xdelta_temp = xdelta/10**(len(beforeDot)-1)
		    xdelta_temp = nondim_xunit_sizes[(np.abs(nondim_xunit_sizes-xdelta_temp)).argmin()]

		    xdelta = xdelta_temp*10**(len(beforeDot)-1)

		else:

		    zeroCountAfterDot = len(afterDot)-len(afterDot.lstrip('0'))

		    xdelta_temp = xdelta*10**(zeroCountAfterDot+1)
		    xdelta_temp = nondim_xunit_sizes[(np.abs(nondim_xunit_sizes-xdelta_temp)).argmin()]

		    xdelta = xdelta_temp/10**(zeroCountAfterDot+1)

		if xscale=="normal":

			if xmin is None:
				xmin = (np.floor(xvals_min/xdelta)-1).astype(float)*xdelta

			if xmax is None:
				xmax = (np.ceil(xvals_max/xdelta)+1).astype(float)*xdelta

			xticks = np.arange(xmin,xmax+xdelta/2,xdelta)

		elif xscale=="log":

			if xmin is None:
				xmin = xvals_min if xvals_min>0 else 0.001

			if xmax is None:
				xmax = xvals_max if xvals_max>0 else 0.1

			xmin_power = np.floor(np.log10(xmin))
			xmax_power = np.ceil(np.log10(xmax))

			xticks = 10**np.arange(xmin_power,xmax_power+1/2)

		return xticks

	def get_yticks(self,yvals=None,top=None,bottom=None,endmultiple=5.,ydelta=25.):

		if yvals is None:
			yvals = np.array([0,1])

		if top is None:
			top = np.nanmin(yvals)

		if bottom is None:
			bottom = np.nanmax(yvals)

		if top>bottom:
			top,bottom = bottom,top

		ymin = np.floor(top/endmultiple)*endmultiple

		ymax = np.ceil(bottom/endmultiple)*endmultiple

		yticks = np.arange(ymin,ymax+ydelta/2,ydelta)

		return yticks

	def _on_mousewheel(self,event):
		"""Lets the scroll work everywhere on the window."""

		self.canvas.yview_scroll(int(-1*(event.delta/120)),"units")

if __name__ == "__main__":

	root = tk.Tk()

	las = DepthView(root)

	Y = np.arange(5000)*0.1
	X = np.random.random(5000)/5

	las.set_axes(2)
	las.set_subaxes(0,3)
	las.set_subaxes(1,3)
	# las.set_subaxes(2,3)
	las.set_lines(0,0,xvals=X,yvals=Y)
	# las.set_lines(1,0,xvals=X,yvals=Y)
	# las.set_lines(1,1,xvals=np.random.random(500),yvals=Y)

	las.set_image()

	# root.geometry("750x270")

	tk.mainloop()