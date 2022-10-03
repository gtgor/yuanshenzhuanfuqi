import threading
import time
from PIL import Image
import pyautogui
import tkinter

from pynput.keyboard import Listener

tk = tkinter.Tk()
global 强化1坐标
global 强化2坐标
global 详细坐标
global 快捷放入坐标
global 强化次数
global 监听线程结束
global 回车次数
global 输入记录
global 位置记录
global 强化间隔时间

强化间隔时间=0.1
位置记录=[]
输入记录 = ""
强化1坐标=False
强化2坐标=False
详细坐标=False
快捷放入坐标=False
强化次数=1
回车次数=0
读秒=tkinter.StringVar()
读秒.set("倒计时")

__版本__=1.0

def 购买提示():
    tk=tkinter.Tk()

    tk.mainloop()

def 修改强化次数(次数):
    global 强化次数
    强化次数=次数

def 修改强化间隔时间(间隔时间):
    global 强化间隔时间
    强化间隔时间=间隔时间

def 给惠惠打赏按钮():
    im = Image.open('打赏.png')
    im.show()



def 获取鼠标位置():
    x,y=pyautogui.position()
    return [x,y]

def 强化命令(详细x,详细y,强化2x,强化2y,快捷放入x,快捷放入y,强化1x ,强化1y):
    for i in range(int(强化次数)):
        pyautogui.click(快捷放入x,快捷放入y)
        pyautogui.click(强化1x,强化1y)
        time.sleep(强化间隔时间)
        pyautogui.click(详细x,详细y)
        time.sleep(强化间隔时间)
        pyautogui.click(强化2x,强化2y)


def _按键监听():
    def 判断是否启动函数(key):
        global 回车次数
        global 输入记录
        global 位置记录
        输入记录=输入记录+str(key).replace("'","")
        if "enter" in str(key):
            鼠标位置=获取鼠标位置()
            if 回车次数>=4:
                位置记录.remove(位置记录[0])
            位置记录.append(鼠标位置)
            回车次数+=1
        if "huihui" in 输入记录:
            输入记录="'"
            print("""惠惠输入成功""")
            try:
                强化命令(位置记录[0][0],位置记录[0][1],位置记录[1][0],位置记录[1][1],位置记录[2][0],位置记录[2][1],位置记录[3][0],位置记录[3][1])
            except Exception as Erroe:
                if Erroe=="list index out of range":
                    pass
        print(输入记录)
        print(回车次数)
        print(位置记录)
    with Listener(判断是否启动函数) as listener:
        listener.join()

def 按键监听():
    监听线程=threading.Thread(group=None, args=(), kwargs={}, daemon=None, target=_按键监听)
    监听线程.start()

if __name__ == '__main__':
    """-----------------------init----------------------------"""
    按键监听()
    """-----------------------windows config------------------"""
    tk.geometry("420x200")
    tk.title("惠惠自动强化器")
    tk.resizable(False, False)
    tk.iconbitmap(bitmap="图标.ico")
    tk.attributes("-topmost",1)
    """-------------------------label-------------------------"""
    tkinter.Scale(tk, from_ =40, to =1,resolution =1,length =150,sliderlength= 20,label ='次数' ,command=修改强化次数).place(x=320,y=10)
    tkinter.Scale(tk, from_ =0.3, to =0.1,resolution =0.01,length =150,sliderlength= 20,label ='间隔时间' ,command=修改强化间隔时间).place(x=10,y=10)

    """------------------------menu---------------------------"""
    任务栏=tkinter.Menu(tk)
    任务栏.add_cascade(label="打赏惠惠~(不是打惠惠)",command=给惠惠打赏按钮)
    tk.config(menu=任务栏)
    tk.mainloop()