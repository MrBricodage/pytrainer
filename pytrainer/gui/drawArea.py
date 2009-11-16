# -*- coding: iso-8859-1 -*-

#Copyright (C) Fiz Vazquez vud1@sindominio.net

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import matplotlib
matplotlib.use('GTK')
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvasGTK
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
#from matplotlib.numerix import *
import matplotlib.pyplot as plt
#from pylab import *
import logging

class DrawArea:
	def __init__(self, vbox = None, window = None):
		logging.debug('>>')
		#self.figure = Figure(figsize=(6,4), dpi=72)
		#self.axis = self.figure.add_subplot(111)
		self.vbox = vbox
		self.window = window
		#self.canvas = FigureCanvasGTK(self.figure) # a gtk.DrawingArea
		#self.drawDefault()
		logging.debug('<<')

	def stadistics(self,type,xvalues,yvalues,xlabel,ylabel,title,color,zones=None):
		logging.debug('>>')	
		if len(xvalues[0]) < 1:
			#self.drawDefault()
			return False
		#logging.debug('xvalues: '+str(xvalues))
		#logging.debug('yvalues: '+str(yvalues))
		logging.debug("Type: "+type+" | title: "+str(title)+" | col: "+str(color)+" | xlabel: "+str(xlabel)+" | ylabel: "+str(ylabel))
		if type == "bars":
			self.drawBars(xvalues,yvalues,xlabel,ylabel,title,color)
		elif type == "plot":
			self.drawPlot(xvalues,yvalues,xlabel,ylabel,title,color,zones)
		elif type == "pie":
			self.drawPie(xvalues,yvalues,xlabel,ylabel,title,color,zones)
		logging.debug('<<')

	def drawBars(self,xvalues,yvalues,xlabel,ylabel,title,color):
		logging.debug('>>')		
		
		# ToDo: check why vertical container is shared
		for child in self.vbox.get_children():
			if self.vbox.get_children()[0] != child:
				logging.debug('Removing child: '+str(child))
				self.vbox.remove(child)
		
		figure = Figure(figsize=(6,4), dpi=72)
		#canvas = FigureCanvasGTK(figure) # a gtk.DrawingArea
		
		xmod = 0.4
		if len(xvalues) > 1:
			width = 0.40
		else:
			width = 0.80
		i=0
		
		for value in xvalues:
			if i<1:
				axis = figure.add_subplot(111)
				axis.set_xlim(-width,len(xvalues[i]))
				axis.set_xlabel(xlabel[i])
				axis.set_ylabel(ylabel[i])
				axis.set_title(title[i])	
				j=0
				for x in xvalues[i]:
					xvalues[i][j]=x-xmod
					j+=1
				axis.bar(xvalues[i], yvalues[i], width, color=color[i])
					
				axis.grid(True)
				for tl in axis.get_yticklabels():
    					tl.set_color('%s' %color[i])
			if i>=1:
				ax2 = axis.twinx()
				ax2.bar(xvalues[i], yvalues[i], width, color=color[i])
				for tl in ax2.get_yticklabels():
    					tl.set_color('%s' %color[i])
			axis.set_xlabel(xlabel[i])
			i+=1
		
		if (len(xvalues)>1):
			axis.set_title("%s vs %s" %(ylabel[0],ylabel[1]))
		else:
			axis.set_title("%s" %(ylabel[0]))

		
		canvas = FigureCanvasGTK(figure) # a gtk.DrawingArea
		canvas.show()
		self.vbox.pack_start(canvas, True, True)
		toolbar = NavigationToolbar(canvas, self.window)
		self.vbox.pack_start(toolbar, False, False)

		for child in self.vbox.get_children():
			logging.debug('Child available: '+str(child))

		logging.debug('<<')

	def drawPlot(self,xvalues,yvalues,xlabel,ylabel,title,color,zones=None):
		logging.debug('>>')  

		logging.debug('xlabel: '+str(xlabel)+' | ylabel: '+str(ylabel)+' | title: '+str(title))
		vboxChildren = self.vbox.get_children()
		logging.debug('Vbox has %d children %s' % (len(vboxChildren), str(vboxChildren) ))
		# ToDo: check why vertical container is shared
		for child in vboxChildren:
			#Remove all FigureCanvasGTK and NavigationToolbar2GTKAgg to stop double ups of graphs
			if isinstance(child, matplotlib.backends.backend_gtkagg.FigureCanvasGTK) or isinstance(child, matplotlib.backends.backend_gtkagg.NavigationToolbar2GTKAgg):
				logging.debug('Removing child: '+str(child))
				self.vbox.remove(child)

		figure = Figure()
		figure.clf()
		i = 0
		for value in xvalues:
			if i<1:
				axis = figure.add_subplot(111)
				axis.plot(xvalues[i],yvalues[i], color=color[i])
					
				axis.grid(True)
				for tl in axis.get_yticklabels():
    					tl.set_color('%s' %color[i])
			if i>=1:
				ax2 = axis.twinx()
				ax2.plot(xvalues[i], yvalues[i], color=color[i])
				for tl in ax2.get_yticklabels():
    					tl.set_color('%s' %color[i])
			axis.set_xlabel(xlabel[i])
			i+=1
		
		if (len(xvalues)>1):
			axis.set_title("%s vs %s" %(ylabel[0],ylabel[1]))
		else:
			axis.set_title("%s" %(ylabel[0]))

		canvas = FigureCanvasGTK(figure) # a gtk.DrawingArea
		canvas.show()
		self.vbox.pack_start(canvas, True, True)
		toolbar = NavigationToolbar(canvas, self.window)
		self.vbox.pack_start(toolbar, False, False)
		
		for child in self.vbox.get_children():
			logging.debug('Child available: '+str(child))

		if title[0] == 'Stage Profile':
			figure.savefig('/tmp/stage.png', dpi=75)
		if title[0] == 'Heart Rate':
			figure.savefig('/tmp/hr.png', dpi=75)
		logging.debug('<<')
	
	def drawPie(self,xvalues,yvalues,xlabel,ylabel,title,color,zones=None):
		logging.debug('>>')

		# ToDo: check why vertical container is shared
		for child in self.vbox.get_children():
			if self.vbox.get_children()[0] != child:
				logging.debug('Removing child: '+str(child))
				self.vbox.remove(child)

		figure = Figure(figsize=(6,4), dpi=72)
		axis = figure.add_subplot(111)

		labels = ["rest"]
		colors = ["#ffffff"]
		frac0 = 0
		frac1 = 0
		frac2 = 0
		frac3 = 0
		frac4 = 0
		frac5 = 0
		for zone in zones:
			labels.append(zone[3])
			colors.append(zone[2])
	
		for value in yvalues[0]:
			if value < zones[4][0]:
				frac0+=1
			elif value > zones[4][0] and value < zones[4][1]:
				frac1+=1
			elif value > zones[3][0] and value < zones[3][1]:
				frac2+=1
			elif value > zones[2][0] and value < zones[2][1]:
				frac3+=1
			elif value > zones[1][0] and value < zones[1][1]:
				frac4+=1
			elif value > zones[0][0] and value < zones[0][1]:
				frac5+=1
			
		fracs = [frac0,frac1,frac2,frac3,frac4, frac5]
		explode=(0, 0, 0, 0,0,0)
		axis.pie(fracs, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)

		canvas = FigureCanvasGTK(figure) # a gtk.DrawingArea
		canvas.show()

		for child in self.vbox.get_children():
			logging.debug('Child available: '+str(child))

		self.vbox.pack_start(canvas, True, True)
		logging.debug('<<')

	def drawDefault(self):
		logging.debug('>>')
		self.axis=self.figure.add_subplot(111)
		self.axis.set_xlabel('Yepper')
		self.axis.set_ylabel('Flabber')
		self.axis.set_title('An Empty Graph')
		self.axis.grid(True)
		self.canvas.destroy()
		self.canvas = FigureCanvasGTK(self.figure) # a gtk.DrawingArea
		self.canvas.show()
		self.vbox.pack_start(self.canvas, True, True)
		logging.debug('<<')

	def fill_over(self, ax, x, y, val, color, over=True):
		"""
		Plot filled x,y for all y over val
		if over = False, fill all areas < val
		"""
		logging.debug('>>')
		ybase = asarray(y)-val
		crossings = nonzero(less(ybase[:-1] * ybase[1:],0))

		if ybase[0]>=0:
			fillon = over
		else:
			fillon = not over
		indLast = 0
		for ind in crossings:
			if fillon:
				thisX = x[indLast:ind+1]
				thisY = y[indLast:ind+1]
				thisY[0] = val
				thisY[-1] = val
				ax.fill(thisX, thisY, color)
			fillon = not fillon
        	indLast = ind
		logging.debug('<<')

