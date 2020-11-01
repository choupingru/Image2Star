import cv2
import numpy as np
import sys
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import *

class MyApp(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.geometry('700x650')
		container = tk.Frame(self)
		container.pack(side="top", fill='both', expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		frame = StartPage(container, self)
		self.frames[StartPage] = frame
		frame.grid(row=0, column=0, sticky='nsew')
		self.show_frame(StartPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		f = Figure(figsize=(5,3), dpi=70)
		a = f.add_subplot(111)
		a.plot([],[])
		a.axis('off')
		self.canvas_org = FigureCanvasTkAgg(f, self)
		self.canvas_org.show()
		self.canvas_org.get_tk_widget().grid(row=0, column=0, rowspan=12, columnspan=2)
		
		f1 = Figure(figsize=(5,3), dpi=70)
		a1 = f.add_subplot(111)
		a1.plot([],[])
		a1.axis('off')
		self.canvas_canny = FigureCanvasTkAgg(f1, self)
		self.canvas_canny.show()
		self.canvas_canny.get_tk_widget().grid(row=12, column=0, rowspan=12, columnspan=2)
		

		f2 = Figure(figsize=(5,3), dpi=70)
		a2 = f.add_subplot(111)
		a2.plot([],[])
		a2.axis('off')
		self.canvas_result = FigureCanvasTkAgg(f2, self)
		self.canvas_result.show()
		self.canvas_result.get_tk_widget().grid(row=24, column=0, rowspan=12, columnspan=2)
		

		file_label = tk.Label(self, text="File Name:")
		file_label.grid(row=0, column=2, sticky=SW)
		
		self.file_name = tk.Text(self, height=1, highlightbackground='black', width=10)
		self.file_name.grid(row=1, column=2)

		load_image = tk.Button(self, text="Load", command=self.loadImage)
		load_image.grid(row=1, column=3)

		result_label = tk.Label(self, text='Result Name:')
		result_label.grid(row=2, column=2, sticky=SW)

		self.result_name = tk.Text(self, height=1, highlightbackground='black', width=10)
		self.result_name.grid(row=3, column=2)

		save_image = tk.Button(self, text="Save", command=self.saveImage)
		save_image.grid(row=3, column=3)

		canny_threshold_label = tk.Label(self, text='Canny Threshold :')
		canny_threshold_label.grid(row=4, column=2, sticky=SW)

		self.canny_threshold_low = tk.Text(self, height=1, highlightbackground='black', width=10)
		self.canny_threshold_low.grid(row=5, column=2)

		self.canny_threshold_high = tk.Text(self, height=1, highlightbackground='black', width=10)
		self.canny_threshold_high.grid(row=5, column=3)

		plot_canny = tk.Button(self, text="Edge Detection", command=self.cannyImage)
		plot_canny.grid(row=5, column=4)

		starButton = tk.Button(self, text="Star!", command=self.starImage, borderwidth=3, height=5)
		starButton.grid(row=6, column=2, rowspan=2, columnspan=3, sticky='nesw')

	def loadImage(self):
		image_name = self.file_name.get('1.0', 'end-1c')
		f = Figure(figsize=(5,3), dpi=70)
		a = f.add_subplot(111)
		image = cv2.imread('./source/'+image_name+'.jpg')
		image = np.array(image)
		a.imshow(image)
		a.axis('off')
		self.canvas_org = FigureCanvasTkAgg(f, self)
		self.canvas_org.show()
		self.canvas_org.get_tk_widget().grid(row=0, column=0, rowspan=12, columnspan=2, sticky=N)
	
	def cannyImage(self):
		low = self.canny_threshold_low.get('1.0', 'end-1c')
		high = self.canny_threshold_high.get('1.0', 'end-1c')

		try:
			low = int(low)
		except:
			low = 200
		try:
			high = int(high)
		except:
			high = 350

		image_name = self.file_name.get('1.0', 'end-1c')
		f = Figure(figsize=(5,3), dpi=70)
		a = f.add_subplot(111)
		image = cv2.imread('./source/'+image_name+'.jpg', 0)
		self.edge = np.array(cv2.Canny(image, low, high))
		a.imshow(self.edge, cmap='gray')
		a.axis('off')
		self.canvas_canny = FigureCanvasTkAgg(f, self)
		self.canvas_canny.show()
		self.canvas_canny.get_tk_widget().grid(row=12, column=0, rowspan=12, columnspan=2, sticky=N)	

	def starImage(self):
		xs, ys = [], []
		height, width = self.edge.shape
		for idx1, row in enumerate(self.edge):
			for idx2, ele in enumerate(row):
				if ele != 0:
					xs.append(idx2)
					ys.append(height - idx1)
		
		self.star = Figure(figsize=(5,3), dpi=70)
		a = self.star.add_subplot(111)
		a.scatter(xs, ys, marker='*', s=0.15)
		a.axis('off')

		self.canvas_result = FigureCanvasTkAgg(self.star, self)
		self.canvas_result.show()
		self.canvas_result.get_tk_widget().grid(row=24, column=0, rowspan=12, columnspan=2, sticky=N)	

	def saveImage(self):
		target = self.result_name.get('1.0', 'end-1c')
		self.star.savefig('./target/'+target+'.jpg')
		
if __name__ == '__main__':
	
	app = MyApp()
	app.mainloop()
