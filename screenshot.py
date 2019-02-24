# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 15:22:15 2019

@author: zengh
"""
from win32api import GetSystemMetrics, keybd_event
import win32con
import tkinter
#import tkinter.filedialog
import os
#import pyscreenshot as  ImageGrab
from PIL import ImageGrab, Image
from time import sleep
from  change2text import Change2Text
root = tkinter.Tk()
root.title("Screenshot to Text")
""" 指定窗口的大小  form =widthxheight+x+y. """
root.geometry('500x400+400+300')
  

#不允许改变窗口大小 
root.resizable(False,False)
filename = "result.jpg"
change2Text = Change2Text(filename)
"""Bug ！！！部分区域不能截图，显示缩放100%"""
class Screenshot:
    def __init__(self, png, ratio):
        #变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.ratio = ratio
        self.sel = False
        #屏幕尺寸
        self.screenWidth = GetSystemMetrics (0) #1920 #root.winfo_screenwidth() 尺寸错误
        self.screenHeight = GetSystemMetrics (1) #1080 #root.winfo_screenheight()
        #显示全屏截图，在全屏截图上进行区域截图
        
        
        #创建顶级组件容器
        self.top = tkinter.Toplevel(root, width=self.screenWidth, height=self.screenHeight)
        #不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top,bg='white', width=self.screenWidth, height=self.screenHeight)
        
        #显示全屏截图，在全屏截图上进行区域截图
       
        self.image = tkinter.PhotoImage(file=png) # 100缩放
        self.canvas.create_image(self.screenWidth//2, self.screenHeight//2, image=self.image)
        self.canvas.pack()
 
        #鼠标左键按下的位置
        def onLeftButtonDown(event):
            # pdb.set_trace()
            self.X.set(event.x)
            self.Y.set(event.y)
            #开始截图
            self.sel =True
        self.canvas.bind('<Button-1>', onLeftButtonDown)
 
        #鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            # pdb.set_trace()
            global lastDraw, r, c
            try:
                #删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(lastDraw)
                self.canvas.delete(r)
                self.canvas.delete(c)
            except Exception as e:
                print(e)
            if not self.sel:
                #没有点击左键时绘制十字线
                r = self.canvas.create_line(0, event.y, self.screenWidth, event.y, fill='white')
                c = self.canvas.create_line(event.x, 0, self.screenHeight, event.x, fill='white')
               # print(event.x, event.y, self.screenWidth, self.screenHeight)
            else:
                lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='orange')
               # print(event.x, event.y, self.screenWidth, self.screenWidth)
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)
        #获取鼠标左键抬起的位置，保存区域截图
        def onLeftButtonUp(event):
            self.sel =False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                print(e)
            sleep(0.1)
            #考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic =ImageGrab.grab((left*self.ratio+1, top*self.ratio+1, right*self.ratio, bottom*self.ratio))
            #关闭顶级容器
            self.top.destroy()
            if pic:
                pic.save('./result.jpg')
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)
#开始截图
def buttonCaptureClick():
    #最小化主窗口
    root.state('icon')
    filename = 'temp.gif'
    keybd_event(win32con.VK_SNAPSHOT, 0)
    sleep(1)
    im = ImageGrab.grabclipboard()
    sleep(4)
    if im is not None:
        ratio = im.size[0]/GetSystemMetrics(0)
        im = im.resize((GetSystemMetrics(0) , GetSystemMetrics(1)), Image.ANTIALIAS)
        im.save(filename)
        im.close()
        """显示全屏幕截图"""
        w =Screenshot(filename, ratio)
        buttonCapture.wait_window(w.top)
    
        """ 调用通用OCR接口，显示文字到文本框"""
        textResult = change2Text.doOCR()
        if textResult is not None:
            text.delete(1.0, tkinter.END)
            text.insert(1.0, textResult)
            
    """截图结束，恢复主窗口，并删除临时的全屏幕截图文件"""
    root.state('normal')
    os.remove(filename)
 
    
    
"""pack, place, grid 布局"""
buttonCapture = tkinter.Button(root, text='截图', width="90", height="2", command=buttonCaptureClick)
buttonCapture.pack(side = "top")

text  = tkinter.Text(root, highlightthickness=2)
text.pack(expand=1, fill="both")

""" 启动消息主循环 """
try:
    root.mainloop()
except:
    root.destroy()

