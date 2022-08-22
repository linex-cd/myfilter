import tkinter as tk
import os.path

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk

import cv2
import numpy as np


app = None
frame1 = None
frame2 = None

filename = None
canvas_src = None
canvas_dest = None
img = None
canvas_img = None
result = None
photo1 = None
photo2 = None

#对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例 
def resize(w, h, w_box, h_box, pil_image):  

	f1 = 1.0*w_box/w
	f2 = 1.0*h_box/h  
	factor = min([f1, f2])  

	width = int(w*factor)  
	height = int(h*factor)
	
	return pil_image.resize((width, height), Image.ANTIALIAS) 

#打开
def button_open_click():
	global app
	global filename
	global canvas_src
	global canvas_dest
	global photo1

	filename = askopenfilename() 
	
	#未选择文件则不执行操作
	if filename == '':
		return 
	if filename[-4:] != '.jpg' and filename[-4:] != '.png':
		showinfo('打开','不是图片文件')
		return 
	photo1 = Image.open(filename)
	photo1 = resize(photo1.width, photo1.height, w_box=500, h_box=500, pil_image=photo1)
	photo1 = ImageTk.PhotoImage(photo1) 
	
	#删除已有的画布，并重建画布
	if canvas_src is not None:
		canvas_src.pack_forget()
	
	if canvas_dest is not None:
		canvas_dest.pack_forget()
		
	canvas_src = tk.Canvas(window, width=photo1.width(), height=photo1.height(),background='#333')
	canvas_src.place(x = 50, y = 100)
	canvas_src.create_image(photo1.width(), photo1.height(), image = photo1, anchor=tk.SE)
	
	
	app.update()
	
#保存
def button_save_click():
	global result
	
	if result is None:
		showinfo('保存','还没有滤镜效果')
		return 
	cv2.imwrite("result.jpg", result)
	showinfo('保存','文件保存在当前目录下的result.jpg')
	
##############################################

#黑白
def fun_gray():
	global app
	global filename
	global img
	global canvas_img
	global result
	global canvas_src
	global canvas_dest
	global photo1
	global photo2
	
	#未选择文件则不执行操作
	if filename == None:
		showinfo('滤镜','还没有打开图片')
		return 
	
	img = cv2.imdecode(np.fromfile(filename,dtype=np.uint8),-1)


	####
	result = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	canvas_img = Image.fromarray(result)
	
	####
	
	photo2 = resize(canvas_img.width, canvas_img.height, w_box=500, h_box=500, pil_image=canvas_img)
	photo2 = ImageTk.PhotoImage(image = photo2)
	
	#删除已有的画布，并重建画布
	if canvas_dest is not None:
		canvas_dest.pack_forget()
	canvas_dest = tk.Canvas(window, width=photo2.width(), height=photo2.height(), background='#333')
	canvas_dest.place(x = 650, y = 100)
	canvas_dest.create_image(photo2.width(), photo2.height(), image = photo2, anchor=tk.SE)
	
	
	app.update()

#素描
def fun_pencil():
	global app
	global filename
	global img
	global canvas_img
	global result
	global canvas_src
	global canvas_dest
	global photo1
	global photo2
	
	#未选择文件则不执行操作
	if filename == None:
		showinfo('滤镜','还没有打开图片')
		return 
	
	img = cv2.imdecode(np.fromfile(filename,dtype=np.uint8),-1)

	####

	#高斯滤波降噪
	gaussian = cv2.GaussianBlur(img, (5,5), 0)
	 
	#Canny算子
	canny = cv2.Canny(gaussian, 50, 150)

	#阈值化处理
	ret, result = cv2.threshold(canny, 100, 255, cv2.THRESH_BINARY_INV)
	
	####
	
	canvas_img = Image.fromarray(result)
	
	photo2 = resize(canvas_img.width, canvas_img.height, w_box=500, h_box=500, pil_image=canvas_img)
	photo2 = ImageTk.PhotoImage(image = photo2)
	
	#删除已有的画布，并重建画布
	if canvas_dest is not None:
		canvas_dest.pack_forget()
	canvas_dest = tk.Canvas(window, width=photo2.width(), height=photo2.height(), background='#333')
	canvas_dest.place(x = 650, y = 100)
	canvas_dest.create_image(photo2.width(), photo2.height(), image = photo2, anchor=tk.SE)
	
	
	app.update()


#胶片
def fun_film():
	global app
	global filename
	global img
	global canvas_img
	global result
	global canvas_src
	global canvas_dest
	global photo1
	global photo2
	
	#未选择文件则不执行操作
	if filename == None:
		showinfo('滤镜','还没有打开图片')
		return 
	
	img = cv2.imdecode(np.fromfile(filename,dtype=np.uint8),-1)


	####
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	result = cv2.applyColorMap(img_gray, cv2.COLORMAP_BONE  )
	
	####
	
	
	canvas_img = Image.fromarray(result)
	
	photo2 = resize(canvas_img.width, canvas_img.height, w_box=500, h_box=500, pil_image=canvas_img)
	photo2 = ImageTk.PhotoImage(image = photo2)
	
	#删除已有的画布，并重建画布
	if canvas_dest is not None:
		canvas_dest.pack_forget()
	canvas_dest = tk.Canvas(window, width=photo2.width(), height=photo2.height(), background='#333')
	canvas_dest.place(x = 650, y = 100)
	canvas_dest.create_image(photo2.width(), photo2.height(), image = photo2, anchor=tk.SE)
	
	
	app.update()


#怀旧
def fun_oldtimes():
	global app
	global filename
	global img
	global canvas_img
	global result
	global canvas_src
	global canvas_dest
	global photo1
	global photo2
	
	#未选择文件则不执行操作
	if filename == None:
		showinfo('滤镜','还没有打开图片')
		return 
	
	img = cv2.imdecode(np.fromfile(filename,dtype=np.uint8),-1)


	####
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	result = cv2.applyColorMap(img_gray, cv2.COLORMAP_OCEAN )
	
	####
	
	
	canvas_img = Image.fromarray(result)
	
	photo2 = resize(canvas_img.width, canvas_img.height, w_box=500, h_box=500, pil_image=canvas_img)
	photo2 = ImageTk.PhotoImage(image = photo2)
	
	#删除已有的画布，并重建画布
	if canvas_dest is not None:
		canvas_dest.pack_forget()
	canvas_dest = tk.Canvas(window, width=photo2.width(), height=photo2.height(), background='#333')
	canvas_dest.place(x = 650, y = 100)
	canvas_dest.create_image(photo2.width(), photo2.height(), image = photo2, anchor=tk.SE)
	
	
	app.update()
		
##############################################

def build_gui():
	global app
	
	global canvas_src
	global canvas_dest
	
	window = tk.Tk()
	
	window.resizable(width=False, height=False)
	
	title = '我的滤镜'
	window.title(title)
	
	window_h = 650
	window_w = 1200
	window.geometry('%dx%d' % (window_w, window_h ))
	

	
	b1=tk.Button(window, text='选择图片', width=8, height=2, command = button_open_click)
	b1.place(x = 100, y = 20)
	
	b2=tk.Button(window, text='保存结果', width=8,height=2,command = button_save_click)
	b2.place(x = 200, y = 20)
	
	
	
	b2=tk.Button(window, text='黑白', width=8, height=2, command = fun_gray)
	b2.place(x = 710, y = 20)
	
	b2=tk.Button(window, text='素描', width=8, height=2, command = fun_pencil)
	b2.place(x = 810, y = 20)
	
	b1=tk.Button(window, text='胶片', width=8, height=2, command = fun_film)
	b1.place(x = 910, y = 20)
	
	b2=tk.Button(window, text='怀旧', width=8, height=2, command = fun_oldtimes)
	b2.place(x = 1010, y = 20)
	
	
	app = window
	
	return window

if __name__ == '__main__':
	window = build_gui()
	window.mainloop()

