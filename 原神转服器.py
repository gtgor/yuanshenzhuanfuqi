# -*- coding: utf-8 -*-


import os
import shutil
import subprocess
import threading
import time
import tkinter
import webbrowser
import winreg
from tkinter.ttk import Separator

import filedialogs
import pyautogui
import requests
import win32com.client
from PIL import Image
from pynput.keyboard import Listener

字体大小 = 10


def 配置信息(文件名, data=False):
    """
    检查是否传入data，
    如果传入，则修改文件内容
    否则返回文件内容
    """
    if data == False:  # 如果没有传入data
        try:
            文件内容 = open("data/配置信息/" + 文件名, encoding="utf-8").read()
        except:
            文件内容 = open("data/配置信息/" + 文件名, encoding="gbk").read()
        return 文件内容
    # 如果传入了data
    try:
        文件 = open("data/配置信息/" + 文件名, "w", encoding="utf-8")
    except:
        文件 = open("data/配置信息/" + 文件名, "w", encoding="gbk")
    文件.write(data)
    文件.close()


def 获取背景图片():
    try:
        背景图片 = tkinter.PhotoImage(file="data/资源/自定义背景图片.png")
    except:
        背景图片 = tkinter.PhotoImage(file="data/资源/背景.png")
    return 背景图片


def 记录登录次数():
    requests.get("http://8.142.28.115:11451/记录")  # 向服务器记录一次登录次数，服务器每天都会记录启动次数


def 检查国际服依赖包是否下载():
    依赖包是否下载 = True
    try:
        官转国大小 = 获取文件大小("data/依赖包/官转国.zip")
        国转官大小 = 获取文件大小("data/依赖包/国转官.zip")
    except:
        官转国大小 = 0
        国转官大小 = 0
    if 官转国大小 < 300:
        依赖包是否下载 = False
    if 国转官大小 < 300:
        依赖包是否下载 = False
    return 依赖包是否下载


def 提示(title, data):
    错误提示 = tkinter.Tk()
    错误提示.title(title)
    错误提示.iconbitmap("data/资源/图标.ico")
    tkinter.Label(错误提示, font=字体大小, text=data, anchor="w", justify="left").pack()
    错误提示.resizable(False, False)
    错误提示.mainloop()


def 获取目录下的文件(rootdir):
    import os
    _files = []
    # 列出文件夹下所有的目录与文件
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        # 构造路径
        path = os.path.join(rootdir, list[i])
        # 判断路径是否为文件目录或者文件
        # 如果是目录则继续递归
        if os.path.isdir(path):
            _files.extend(获取目录下的文件(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files


def 获取桌面路径():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]


def 获取兑换码(是否保存到桌面=True):
    data = requests.get("http://8.142.28.115/原神兑换码").text
    if "404 Not Found" in data:
        return False
    if 是否保存到桌面:
        a = open(获取桌面路径() + "\\原神兑换码.txt", "w+")
        a.write(data)
        a.close()
        提示("系统提示", "兑换码获取成功，请前往桌面查看")
        return data
    else:
        return "获取成功"


def 获取路径():
    config = "data/配置信息/原神路径"
    try:
        data = open(config, encoding="utf-8").read()
    except:
        try:
            data = open(config, encoding="ANSI").read()
        except:
            data = open(config, encoding="gbk").read()
    return data


def 保存路径(path):
    # 对用户输入的路径进行修改
    path = path.replace("：", ":")
    path = path.replace("/", r'\惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠')
    path = path.replace("惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠惠", "")
    a = open("data/配置信息/原神路径", "w")
    a.write(path)
    a.close()
    当前路径.set(open("data/配置信息/原神路径", "r").read())


def 获取文件大小(文件):
    stat_info = os.stat(文件)
    size = stat_info.st_size
    return size / 1024 / 1024


def 官转国():
    try:
        os.rename(获取路径() + "\YuanShen_Data", 获取路径() + "\GenshinImpact_Data")  # 先改名
        os.remove(获取路径() + "\YuanShen.exe")  # 删除其他原神服主程序
    except Exception as err:
        print("转国际服错误:" + str(err))
        return False
    shutil.unpack_archive("data/依赖包/官转国.zip", extract_dir=获取路径(), format=None)  # 再解压


def 国转官():
    try:
        os.rename(获取路径() + "\GenshinImpact_Data", 获取路径() + "\YuanShen_Data")  # 先改名
        os.remove(获取路径() + "\GenshinImpact.exe")  # 删除其他原神服主程序
    except Exception as err:
        pass
    shutil.unpack_archive("data/依赖包/国转官.zip", extract_dir=获取路径(), format=None)  # 再解压


def 官转b():
    try:
        os.rename(获取路径() + "\GenshinImpact_Data", 获取路径() + "\YuanShen_Data")  # 先改名
    except Exception as err:
        pass
    shutil.unpack_archive("data/依赖包/官转b.zip", extract_dir=获取路径(), format=None)  # 再解压
    try:
        os.remove(获取路径() + "\YuanShen_Data\Plugins\metakeeper.dll")  # 删除metakeeper.dll
    except Exception as err:
        pass


def b转官():
    shutil.unpack_archive("data/依赖包/b转官.zip", extract_dir=获取路径(), format=None)  # 先解压
    try:
        os.remove(获取路径() + "\YuanShen_Data\Plugins\PCGameSDK.dll")  # 删除PCgamesdk
    except Exception as err:
        pass


def 启动(服="官服"):
    if 是否需要破解帧率启动.get() == "1":
        破解帧率启动()
    else:
        普通启动()


def 普通启动():
    if 获取当前服() == "官服":
        文件名 = "YuanShen"
    if 获取当前服() == 'b服':
        文件名 = "YuanShen"
    if 获取当前服() == "国际服":
        文件名 = "GenshinImpact"
    path = 获取路径()
    命令一 = "cd {}".format(系统路径转换(path))
    总命令 = "{}:&".format(path[:1]) + 命令一 + "&.\{}".format(文件名)
    print(总命令)
    # subprocess.call(总命令, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    threading.Thread(group=None, args=([总命令]),
                     kwargs={"shell": True, "stdin": subprocess.PIPE, "stdout": subprocess.PIPE,
                             "stderr": subprocess.PIPE}, daemon=None,
                     target=subprocess.call).start()  # 创建线程，防止游戏启动时转服器卡死


def 破解帧率启动():
    if 获取当前服() == "官服":
        原神文件名 = "YuanShen.exe"
    if 获取当前服() == "b服":
        原神文件名 = "YuanShen.exe"
    if 获取当前服() == "国际服":
        原神文件名 = "GenshinImpact.exe"
    fps_config = open("data/帧率破解器/fps_config.ini", "w", encoding="GBK")
    fps_config.write(r"""[Setting]
Path={}\{}
FPS=200""".format(获取路径(), 原神文件名))
    fps_config.close()
    命令一 = "cd {}".format(系统路径转换(os.getcwd() + "\data\帧率破解器"))
    总命令 = "{}:&".format(os.getcwd()[:1]) + 命令一 + "&.\{}".format("帧率破解器")
    print(总命令)
    # threading.Thread(group=None, args=([总命令]), kwargs={}, daemon=None, target=os.system).start()  # 创建线程，防止游戏启动时转服器卡死
    threading.Thread(group=None, args=([总命令]),
                     kwargs={"shell": True, "stdin": subprocess.PIPE, "stdout": subprocess.PIPE,
                             "stderr": subprocess.PIPE}, daemon=None,
                     target=subprocess.call).start()  # 创建线程，防止游戏启动时转服器卡死


def 刷新当前服显示框的字体颜色():
    """
    刷新当前服字体颜色
    如果未选择服，字体为红色
    如果已选择服，字体为绿色
    """
    try:  # 加上try是为了防止调用此函数时，当前服显示框没有初始化
        if 当前服显示信息.get() == "未选择路径":
            当前服显示框.config(fg="red")
        else:
            当前服显示框.config(fg="green")
        当前服显示框.update()
    except:
        pass


def 获取当前服(是否返回未选择=True):
    try:
        config = open(获取路径() + "\config.ini", "r").read()
    except:
        if 是否返回未选择:
            return "未选择路径"
    if "channel=1" in config:
        if "sub_channel=1" in config:
            return "官服"
    if "channel=1" in config:
        if "sub_channel=2" in config:
            return "官服"
    if "channel=14" in config:
        if "sub_channel=0" in config:
            return "b服"
    if "channel=1" in config:
        if "sub_channel=0" in config:
            return "国际服"


def 检查原神data名是国服还是国际服():
    file_list = os.listdir(获取路径())  # 获取原神路径中的所以文件名
    if "YuanShen_Data" in file_list:
        return "国服"
    if "GenshinImpact_Data" in file_list:
        return "国际服"


def 检测配置是否正常():  # 如果正常就返回True,不正常就返回False
    路径 = 获取路径()
    config = open(路径 + "\config.ini", "r").read()
    if """[General]
channel=""" in config:
        return True
    else:
        return False


def 判断依赖包是否下载():
    依赖包是否下载 = True
    try:
        官转国大小 = 获取文件大小("data/依赖包/官转国.zip")
        国转官大小 = 获取文件大小("data/依赖包/国转官.zip")
        print("官转国大小=" + str(官转国大小))
        print("国转官大小=" + str(国转官大小))
    except:
        官转国大小 = 0
        国转官大小 = 0
    if 官转国大小 < 270:
        依赖包是否下载 = False
        time.sleep(3)
    if 国转官大小 < 260:
        依赖包是否下载 = False
    return 依赖包是否下载


def 关闭原神主程序():
    subprocess.call("taskkill /f /t /im YuanShen.exe")
    subprocess.call("taskkill /f /t /im GenshinImpact.exe")


def 官服启动():
    关闭原神主程序()
    当前服 = str(获取当前服())
    print(当前服 + " ----- 官服")
    if 当前服 == "官服":
        pass
    if 当前服 == "b服":
        b转官()
    if 当前服 == "国际服":
        国转官()
    if 当前服 == "None":
        b转官()
    当前服显示信息.set(获取当前服())
    刷新当前服显示框的字体颜色()
    启动("官服")


def b服启动():
    关闭原神主程序()
    当前服 = str(获取当前服())
    print(当前服 + " ----- b服")
    if 当前服 == "官服":
        官转b()
    if 当前服 == "b服":
        pass
    if 当前服 == "国际服":
        国转官()
        官转b()
    if 当前服 == "None":
        官转b()
    当前服显示信息.set(获取当前服())
    刷新当前服显示框的字体颜色()
    启动("b服")


def 国际服启动():
    关闭原神主程序()
    依赖包是否下载 = 判断依赖包是否下载()
    当前服 = str(获取当前服())
    print(当前服 + " ----- 国际服")
    print("依赖包是否下载=" + str(依赖包是否下载))
    if 依赖包是否下载:
        if 当前服 == "官服":
            官转国()
        if 当前服 == "b服":
            b转官()
            time.sleep(1)
            官转国()
        if 当前服 == "国际服":
            pass
        当前服显示信息.set(获取当前服())
        刷新当前服显示框的字体颜色()
        启动("国际服")
    else:
        提示("系统提示", "依赖包没有下载，请前往q群下载")


def 从桌面快捷方式选择原神路径():
    def 获取快捷方式指向的路径(路径):  # 调用api
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(路径)
        return shortcut.Targetpath

    for 文件 in 获取目录下的文件(获取桌面路径()):
        print(文件)
        if r"\原神.lnk" in 文件:
            启动器路径 = 获取快捷方式指向的路径(文件)
            启动器配置文件路径 = 启动器路径.replace(r"\launcher.exe", r"\config.ini")
            配置信息 = open(启动器配置文件路径, "r").read()
            # print(配置信息)
            索引头 = 配置信息.index("game_install_path=") + 18
            配置信息 = 配置信息[索引头:]
            索引尾 = 配置信息.index("\n")
            原神路径 = 配置信息[:索引尾]
            # print(原神路径)
            保存路径(原神路径)
            当前服显示信息.set(获取当前服(True))
            刷新当前服显示框的字体颜色()


def 手动选择原神路径():
    路径 = filedialogs.open_folder_dialog('选择"Genshin Impact Game"路径', 'gbk')
    print(路径)
    if "genshin impact game" in 路径[-19:].lower():
        保存路径(路径)
        当前路径.set(open("data/配置信息/原神路径", "r").read())
        当前服显示信息.set(获取当前服())
        刷新当前服显示框的字体颜色()
        提示("可爱の惠惠の提示", "路径保存成功")
    else:
        提示("可爱の惠惠の提示", "请选择'Genshin Impact Game'文件夹哟~")


def 系统路径转换(data):
    return data.replace(" ", '" "')


def 搜索(path, name):
    for root, dirs, files in os.walk(path):  # path 为根目录
        if name in dirs or name in files:
            flag = 1  # 判断是否找到文件
            root = str(root)
            dirs = str(dirs)
            return os.path.join(root)
    return -1


def 将依赖包放进data文件夹():
    def 查找qq群下载的依赖包():
        """获取腾讯文件下所以文件名，找到依赖包就返回依赖包的路径（以列表的方式）"""
        file = 获取目录下的文件(r"C:\Users\{}\Documents\Tencent Files".format(os.getlogin()))
        依赖包路径 = []
        for i in file:
            if "\官转国.zip" in i or "\国转官.zip" in i:
                依赖包路径.append(i)
        return 依赖包路径

    try:
        依赖包 = 查找qq群下载的依赖包()
        依赖包[1]
        for i in 依赖包:
            if "国转官" in i:
                shutil.copy(i, "data/依赖包/国转官.zip")
            if "官转国" in i:
                shutil.copy(i, "data/依赖包/官转国.zip")
        提示("系统提示", "获取成功")
    except:
        提示("系统提示", "获取失败，请前往qq群文件下载依赖包")


def 添加账号(文件名, 备注, 账号信息库位置="data/账号库/账号信息.csv"):
    subprocess.call(
        r'reg export "HKEY_CURRENT_USER\Software\miHoYo\原神" data\账号库\{}.reg'.format(文件名))  # 通过cmd命令行导出原神的注册表文件
    文件默认编码格式 = open(账号信息库位置).encoding
    try:
        账号数据库 = open(账号信息库位置, "a+", encoding="UTF-8")
    except:
        账号数据库 = open(账号信息库位置, "a+", encoding="GBK")
    账号数据库.write("\n{},{},{}".format(文件名, 获取当前服(True), 备注))


def 获取所有保存的账号(账号信息库位置="data/账号库/账号信息.csv"):  # 此函数会返回一个列表，里面包含所有账号信息

    try:
        账号数据库 = open(账号信息库位置, "r", encoding="UTF-8").read()
    except:
        账号数据库 = open(账号信息库位置, "r", encoding="GBK").read()
    所有账号列表 = []
    for 每行信息 in 账号数据库.split("\n"):  # 此循环用于创建列表
        所有账号列表.append(每行信息)
    return 所有账号列表[1:]  # 删除行头


def 修改注册表信息(账号名):
    subprocess.call(r'reg import "data/账号库/{}.reg"'.format(账号名))


def 切换账号命令(下标):  # 传入下标，对应着账号信息库的顺序
    账号信息 = 获取所有保存的账号()
    print("账号信息:" + str(账号信息))
    当前要启动的账号.set(账号信息[下标].split(",")[0])
    修改注册表信息(账号信息[下标].split(",")[0])
    if 账号信息[下标].split(",")[1] == "官服":
        官服启动()
    if 账号信息[下标].split(",")[1] == "b服":
        b服启动()
    if 账号信息[下标].split(",")[1] == "国际服":
        国际服启动()


def 给惠惠打赏按钮():
    im = Image.open('data/资源/打赏.png')
    im.show()


def 调整图片尺寸():
    def 更改图片尺寸(file_in, file_out, width, height):
        image = Image.open(file_in)
        resized_image = image.resize((width, height), Image.ANTIALIAS)
        resized_image.save(file_out)

    y_屏幕 = tk.winfo_screenheight()
    x_屏幕 = tk.winfo_screenwidth()
    x_图片 = 获取背景图片().width()
    y_图片 = 获取背景图片().height()
    print("""
屏幕x={}
屏幕y={}
图片x={}
图片y={}
    """.format(x_屏幕, y_屏幕, x_图片, y_图片))
    if x_图片 > x_屏幕:
        x_缩小比例 = x_屏幕 / x_图片
    else:
        x_缩小比例 = 1
    if y_图片 > y_屏幕:
        y_缩小比例 = y_屏幕 / y_图片
    else:
        y_缩小比例 = 1
    """先确定下一个最终缩小比例，如果x和y都要缩小，则改变此值"""
    最终缩小比例 = 1
    if x_缩小比例 < 1:
        最终缩小比例 = x_缩小比例
    if y_缩小比例 < 1:
        最终缩小比例 = y_缩小比例
    """如果x和y都需要缩小，则判断谁缩的更小"""
    if x_缩小比例 < 1 and y_缩小比例 < 1:
        if x_缩小比例 > y_缩小比例:
            最终缩小比例 = y_缩小比例
        else:
            最终缩小比例 = x_缩小比例
    更改图片尺寸("data/资源/背景.png", "data/资源/背景.png", int(x_图片 * 最终缩小比例), int(y_图片 * 最终缩小比例))


def 生成背景(类型):
    if 类型 == "全部":
        url = "https://iw233.cn/api.php?sort=random"
    if 类型 == "银发":
        url = "https://iw233.cn/api.php?sort=yin"
    if 类型 == "兽耳":
        url = "https://iw233.cn/api.php?sort=cat"
    if 类型 == "星空":
        url = "https://iw233.cn/api.php?sort=xing"
    if 类型 == "色图":
        url = "http://8.142.28.115:13131/色图"
    print(url)
    data = requests.get(url).content
    a = open("data/资源/背景.png", "wb")
    print(data)
    a.write(data)
    a.close()
    Image.open("data/资源/背景.png").save("data/资源/背景.png")
    调整图片尺寸()


def 刷新背景():
    背景图片.config(file="data/资源/背景.png")
    tk.geometry("{}x{}".format(背景图片.width(), 背景图片.height()))  # 图片多大，窗口就多大
    tk.update()


def 随机背景(类型):
    生成背景(类型)
    刷新背景()


def 更改图片保存的文件夹():
    配置信息("背景图片的保存位置", filedialogs.open_folder_dialog(encoding="GBK"))
    提示("系统提示", "背景图片保存路径已更改为:'{}'".format(配置信息("背景图片的保存位置")))


def 保存背景():
    def 获取没有使用的图片名():
        for i in range(99999):
            try:
                open("{}/{}.png".format(获取桌面路径(), i))
            except:
                return i

    if 配置信息("背景图片的保存位置") == "":
        更改图片保存的文件夹()

    print("保存背景   data/资源/背景.png  -->  {}\{}.png".format(配置信息("背景图片的保存位置"), 获取没有使用的图片名()))
    shutil.copy("data/资源/背景.png", 配置信息("背景图片的保存位置") + "\{}.png".format(获取没有使用的图片名()))
    提示("系统提示", "背景已保存至" + 配置信息("背景图片的保存位置"))


def 更换背景():
    from tkinter import filedialog
    file_path = filedialog.askopenfilenames(title='请选择一个文件', filetypes=[('图片', '.png'), ('图片', '.jpg')])[0]
    print(file_path)
    Image.open(file_path).save("data/资源/自定义背景图片.png")
    背景图片.config(file="data/资源/自定义背景图片.png")
    tk.geometry("{}x{}".format(背景图片.width(), 背景图片.height()))  # 图片多大，窗口就多大
    tk.update()


def 帮助命令():
    提示("可爱の惠惠の帮助", """如果程序转服识别，请联系惠惠远程""")


def 关注惠惠bilibili():
    webbrowser.open("https://space.bilibili.com/400684381?spm_id_from=333.1007.0.0")


def 检查更新(是否提示已是最新版本=False):
    更新提示 = requests.get("http://8.142.28.115/新版本更新内容").text
    最新版本 = requests.get("http://8.142.28.115/4版本").text
    当前版本 = open("data/配置信息/当前转服器版本").read()
    print(float(当前版本), float(最新版本))
    if float(当前版本) < float(最新版本):
        更新窗口 = tkinter.Tk()
        更新窗口.title("是否更新新版本")
        更新窗口.iconbitmap("data/资源/图标.ico")
        tkinter.Label(更新窗口, text=更新提示, font=字体大小, anchor="w", justify="left").pack()
        更新窗口.resizable(False, False)

        def 下载新版本():
            webbrowser.open("http://8.142.28.115/原神转服器安装包.exe")

        更新按钮 = tkinter.Button(更新窗口, text="更新", justify='left', command=下载新版本).pack()
        更新窗口.mainloop()
    else:
        if 是否提示已是最新版本:
            提示("系统提示", "目前已是最新版本，无需更新")


def 联系惠惠():
    提示("惠惠QQ", "惠惠QQ1621320515")


def 贡献榜():
    提示("贡献榜  感谢大家对惠惠的支持，希望惠惠可以帮到越来越多的人", requests.get("http://8.142.28.115/贡献榜").text)


def 管理账号窗口():
    root = tkinter.Tk()

    # 按扭调用的函数
    def 添加账号按钮命令():
        账号名 = 账号名输入框.get()
        备注 = 备注输入框.get()
        账号重复 = False
        if 账号名 != "":
            if 备注 != "":
                for i in 获取所有保存的账号():
                    if 账号名 == i.split(',')[0]:
                        账号重复 = True
                        提示信息["text"] = "账号重复"
                if 账号重复 == False:
                    添加账号(账号名, 备注)
                    提示信息["text"] = 账号名 + "添加成功"
            else:
                提示信息["text"] = "备注不能为空"
        else:
            提示信息["text"] = "账号不能为空"
        切换账号按钮.config(menu=菜单())

    def 删除按钮命令():
        账号名 = 账号名输入框.get()
        try:
            os.remove(r"data/账号库/{}.reg".format(账号名))  # 删除保存的账号注册表（reg文件）
        except:
            提示信息["text"] = "账号不存在"
        if 账号名 == "":
            提示信息["text"] = "请输入账号"  # 防止整个文件给你薅了
            return False  # 不往下执行，用返回函数来卡住函数
        """
        读取整个文件的每一行，将含有用户输入的那行删了
        """
        账号库 = open(r"data/账号库/账号信息.csv", encoding="utf-8")
        账号库data = 账号库.read()
        for 每行信息 in 账号库data.split("\n"):
            print(每行信息)
            if "{},".format(账号名) in 每行信息:  # 加个逗号，防止关键字错误
                账号库data = 账号库data.replace("\n" + 每行信息, "")
                账号库 = open(r"data/账号库/账号信息.csv", "w", encoding="utf-8")
                账号库.write(账号库data)
                提示信息["text"] = "删除成功"
        账号库.close()
        切换账号按钮.config(menu=菜单())

    账号名显示 = tkinter.Label(root, text='账号名：')
    账号名显示.grid(row=0, sticky=tkinter.W)
    账号名输入框 = tkinter.Entry(root)
    账号名输入框.grid(row=0, column=1, sticky=tkinter.E)

    备注显示 = tkinter.Label(root, text='备注信息：')
    备注显示.grid(row=1, sticky=tkinter.W)
    备注输入框 = tkinter.Entry(root)
    备注输入框.grid(row=1, column=1, sticky=tkinter.E)

    提示信息 = tkinter.Label(root, text='')
    提示信息.grid(row=3)

    添加账号按钮 = tkinter.Button(root, text='保存账号缓存', command=添加账号按钮命令)
    添加账号按钮.grid(row=2, column=1, sticky=tkinter.E)

    删除按钮 = tkinter.Button(root, text='删除账号缓存', command=删除按钮命令)
    删除按钮.grid(row=2, column=0, sticky=tkinter.E)

    root.mainloop()


def 惠惠自动化工具():
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
    global 自动过剧情是否开启

    自动过剧情是否开启 = False
    强化间隔时间 = 0.1
    位置记录 = []
    输入记录 = ""
    强化1坐标 = False
    强化2坐标 = False
    详细坐标 = False
    快捷放入坐标 = False
    强化次数 = 1
    回车次数 = 0
    读秒 = tkinter.StringVar()
    读秒.set("倒计时")

    def 修改强化次数(次数):
        global 强化次数
        强化次数 = 次数

    def 修改强化间隔时间(间隔时间):
        global 强化间隔时间
        强化间隔时间 = 间隔时间

    def 给惠惠打赏按钮():
        im = Image.open('打赏.png')
        im.show()

    def 获取鼠标位置():
        x, y = pyautogui.position()
        return [x, y]

    def 强化命令(详细x, 详细y, 强化2x, 强化2y, 快捷放入x, 快捷放入y, 强化1x, 强化1y):
        for i in range(int(强化次数)):
            pyautogui.click(快捷放入x, 快捷放入y)
            pyautogui.click(强化1x, 强化1y)
            time.sleep(强化间隔时间)
            pyautogui.click(详细x, 详细y)
            time.sleep(强化间隔时间)
            pyautogui.click(强化2x, 强化2y)

    def 自动过剧情():
        global 自动过剧情是否开启
        while True:
            pyautogui.click(int(pyautogui.size()[0] * 0.9), (pyautogui.size()[1] * 0.6))
            pyautogui.click(int(pyautogui.size()[0] * 0.9), (pyautogui.size()[1] * 0.65))
            pyautogui.click(int(pyautogui.size()[0] * 0.9), (pyautogui.size()[1] * 0.7))
            pyautogui.click(int(pyautogui.size()[0] * 0.9), (pyautogui.size()[1] * 0.75))
            pyautogui.click(int(pyautogui.size()[0] * 0.9), (pyautogui.size()[1] * 0.8))
            pyautogui.click(int(pyautogui.size()[0] * 0.9), (pyautogui.size()[1] * 0.85))
            pyautogui.click(int(pyautogui.size()[0] * 0.9), (pyautogui.size()[1] * 0.))
            if 自动过剧情是否开启 == False:
                break

    def _按键监听():
        def 判断是否启动函数(key):
            global 回车次数
            global 输入记录
            global 位置记录
            global 自动过剧情是否开启
            输入记录 = 输入记录 + str(key).replace("'", "")
            if "enter" in str(key):
                鼠标位置 = 获取鼠标位置()
                if 回车次数 >= 4:
                    位置记录.remove(位置记录[0])
                位置记录.append(鼠标位置)
                回车次数 += 1
            if "huihui" in 输入记录:
                输入记录 = "'"
                print("""惠惠输入成功""")
                try:
                    强化命令(位置记录[0][0], 位置记录[0][1], 位置记录[1][0], 位置记录[1][1], 位置记录[2][0], 位置记录[2][1], 位置记录[3][0], 位置记录[3][1])
                except Exception as Erroe:
                    if Erroe == "list index out of range":
                        pass
            if "Key.f10" in str(key):
                if 自动过剧情是否开启 == False:
                    自动过剧情是否开启 = True
                    threading.Thread(group=None, args=(), kwargs={}, daemon=None, target=自动过剧情).start()
                else:
                    自动过剧情是否开启 = False
                print("自动过剧情是否开启=" + str(自动过剧情是否开启))

            print(输入记录)
            print(回车次数)
            print(位置记录)

        with Listener(判断是否启动函数) as listener:
            listener.join()

    if __name__ == '__main__':
        """-----------------------init----------------------------"""
        监听线程 = threading.Thread(group=None, args=(), kwargs={}, daemon=None, target=_按键监听)
        监听线程.setDaemon(True)  # 设置成守护线程，免得窗口没了，线程还在跑
        监听线程.start()
        """-----------------------windows config------------------"""
        tk.geometry("420x400")
        tk.title("惠惠自动化工具")
        tk.resizable(False, False)
        try:
            tk.iconbitmap(bitmap="data/图标.ico")
        except:
            tk.iconbitmap(bitmap="data/资源/图标.ico")
        tk.attributes("-topmost", 1)
        """-------------------------label-------------------------"""
        tkinter.Label(tk, text="自动化工具配置，使用方法见主页帮助").place(x=0, y=0)
        tkinter.Scale(tk, from_=40, to=1, resolution=1, length=150, sliderlength=20, label='次数', command=修改强化次数).place(
            x=320, y=40)
        tkinter.Scale(tk, from_=0.3, to=0.1, resolution=0.01, length=150, sliderlength=20, label='间隔时间',
                      command=修改强化间隔时间).place(x=10, y=40)
        tkinter.ttk.Separator(tk, orient=tkinter.HORIZONTAL).place(x=20, y=200, width=380)
        tkinter.Label(tk, text="自动过剧情开关：F10").place(x=0, y=250)

        """------------------------menu---------------------------"""
        任务栏 = tkinter.Menu(tk)
        tk.config(menu=任务栏)


def 输出基本信息():
    print("-" * 20)
    print("桌面路径=" + 获取桌面路径())
    print("原神路径=" + 配置信息("原神路径"))
    print("背景图片的保存位置=" + 配置信息("背景图片的保存位置"))
    print("默认启动方式=" + 配置信息("默认启动方式"))
    print("-" * 20)


def 菜单():
    def 任务栏_main():
        任务栏 = tkinter.Menu(tk, tearoff=False)

        def 任务栏_工具箱():
            工具箱 = tkinter.Menu(tk, tearoff=False)
            工具箱.add_cascade(label="惠惠自动化工具", command=惠惠自动化工具)
            工具箱.add_cascade(label="破解帧率启动", command=破解帧率启动)
            任务栏.add_cascade(label="工具箱", menu=工具箱)

        def 任务栏_帮助():
            帮助 = tkinter.Menu(tk, tearoff=False)
            帮助.add_cascade(label="惠惠原神转服器", command=lambda: 提示(帮助, open("data/说明文档/原神转服器.md", encoding="utf-8").read()))
            帮助.add_cascade(label="惠惠自动化工具",
                           command=lambda: 提示(帮助, open("data/说明文档/惠惠自动化工具.md", encoding="utf-8").read()))
            帮助.add_cascade(label="破解帧率启动器", command=lambda: 提示(帮助, open("data/说明文档/帧率破解器.md", encoding="utf-8").read()))
            帮助.add_separator()  # 添加一条线，好看
            帮助.add_cascade(label="联系惠惠", command=联系惠惠)
            任务栏.add_cascade(label="帮助", menu=帮助)

        def 任务栏_获取兑换码():
            if 获取兑换码(False) == "获取成功":
                任务栏.add_cascade(label="获取兑换码", command=lambda: 获取兑换码(True))

        def 任务栏_功能():
            功能 = tkinter.Menu(tk, tearoff=False)
            功能.add_cascade(label="检查更新", command=lambda: 检查更新(True))
            功能.add_cascade(label="从群文件获取依赖", command=将依赖包放进data文件夹)
            任务栏.add_cascade(label="功能", menu=功能)

        def 任务栏_支持惠惠():
            支持惠惠 = tkinter.Menu(tk, tearoff=False)
            支持惠惠.add_cascade(label="给惠惠打赏", command=给惠惠打赏按钮)
            支持惠惠.add_cascade(label="关注惠惠biliblil", command=关注惠惠bilibili)
            任务栏.add_cascade(label="支持惠惠", menu=支持惠惠)

        任务栏_支持惠惠()
        任务栏.add_cascade(label="贡献榜", command=贡献榜)
        任务栏_功能()
        任务栏_工具箱()
        任务栏_帮助()
        任务栏_获取兑换码()
        return 任务栏

    def 启动菜单_main():
        启动菜单 = tkinter.Menu(启动按钮, tearoff=False)
        启动菜单.add_cascade(label="官服启动", command=官服启动)
        启动菜单.add_cascade(label="b服启动", command=b服启动)
        启动菜单.add_cascade(label="国际服启动", command=国际服启动)
        启动菜单.add_separator()  # 添加一条线，好看
        启动菜单.add_checkbutton(label="是否破解帧率启动", variable=是否需要破解帧率启动,
                             command=lambda: 配置信息("data/配置信息/默认启动方式", 是否需要破解帧率启动.get()))
        return 启动菜单

    def 选择路径菜单_main():
        选择路径菜单 = tkinter.Menu(选择路径按钮, tearoff=False)
        选择路径菜单.add_cascade(label="从桌面快捷方式选择原神路径", command=从桌面快捷方式选择原神路径)
        选择路径菜单.add_cascade(label="手动选择路径", command=手动选择原神路径)
        return 选择路径菜单

    def 切换账号菜单_main():
        切换账号菜单 = tkinter.Menu(切换账号按钮, tearoff=False)
        切换账号菜单.add_cascade(label="管理账号", command=管理账号窗口)
        切换账号菜单.add_separator()  # 添加一条线，好看
        try:
            最终命令 = """"""
            命令 = "切换账号菜单.add_cascade(label=获取所有保存的账号()[菜单下标],command=lambda :切换账号命令(菜单下标))"  # 之所以要这样写是因为，假如直接使用，那么所以选项都是一样的
            for i in range(1000):
                最终命令 = 最终命令 + 命令.replace("菜单下标", str(i)) + "\n"
            exec(最终命令)
        except:
            pass
        return 切换账号菜单

    """以下是菜单"""
    tk.config(menu=任务栏_main())
    选择路径按钮.config(menu=选择路径菜单_main())
    切换账号按钮.config(menu=切换账号菜单_main())
    启动按钮.config(menu=启动菜单_main())


def 背景的右键菜单(鼠标的点击位置):
    界面 = tkinter.Menu(tk, tearoff=False)
    界面.add_cascade(label="自定义背景", command=更换背景)
    界面.add_separator()  # 添加一条线，好看
    界面.add_cascade(label="随机背景", command=lambda: 随机背景("全部"))
    界面.add_cascade(label="随机背景(银发)", command=lambda: 随机背景("银发"))
    界面.add_cascade(label="随机背景(兽耳)", command=lambda: 随机背景("兽耳"))
    界面.add_cascade(label="随机背景(星空)", command=lambda: 随机背景("星空"))
    界面.add_cascade(label="随机背景(色图)", command=lambda: 随机背景("色图"))
    界面.add_separator()  # 添加一条线，好看
    界面.add_cascade(label="保存背景图片", command=保存背景)
    界面.add_separator()  # 添加一条线，好看
    界面.add_cascade(label="更改背景保存位置", command=更改图片保存的文件夹)
    界面.post(鼠标的点击位置.x_root, 鼠标的点击位置.y_root)


if __name__ == '__main__':
    """---------------------------------  初始化  ------------------------------------------"""
    threading.Thread(group=None, args=(), kwargs={}, daemon=None, target=检查更新).start()
    threading.Thread(group=None, args=(), kwargs={}, daemon=None, target=记录登录次数).start()  # 记录登录次数的线程
    tk = tkinter.Tk()
    当前服显示信息 = tkinter.Variable()
    当前服显示信息.set(获取当前服(True))
    # 刷新当前服显示框的字体颜色()    #当前服为初始化，所以放在初始化后，启动窗口前的，自己找
    是否需要破解帧率启动 = tkinter.StringVar()
    是否需要破解帧率启动.set(配置信息("默认启动方式"))  # 0是未选中，1是选中
    当前路径 = tkinter.Variable()
    当前路径.set(获取路径())
    当前要启动的账号 = tkinter.Variable()
    当前要启动的账号.set("当前账号:默认")
    """---------------------------------  背景设置  ---------------------------------------------"""
    背景图片 = 获取背景图片()
    背景 = tkinter.Label(tk, image=背景图片, cursor="hand2")
    背景.bind("<Button-3>", 背景的右键菜单)
    背景.bind("<Button-1>", 背景的右键菜单)
    背景.pack()
    """---------------------------------  控件设置  ---------------------------------------------"""
    当前账号框 = tkinter.Label(tk, font=字体大小, background="#FFFF6F", textvariable=当前要启动的账号, anchor="w")
    当前路径显示 = tkinter.Label(tk, font=字体大小, background="#FFFF6F", textvariable=当前路径, anchor="w")
    当前服显示框 = tkinter.Label(tk, font=字体大小, background="#FFFF6F", textvariable=当前服显示信息, anchor="w")
    启动按钮 = tkinter.Menubutton(tk, text='启动', font=字体大小)
    切换账号按钮 = tkinter.Menubutton(tk, text='账号', font=字体大小)
    选择路径按钮 = tkinter.Menubutton(tk, text="选择路径", font=字体大小, background="#FF8040")
    """---------------------------------  布局设置  ---------------------------------------------"""
    高度 = 0.03
    当前账号框.place(relx=0, rely=0, relwidth=0.1, relheight=高度)
    当前服显示框.place(relx=0.1, rely=0, relwidth=0.1, relheight=高度)
    当前路径显示.place(relx=0.2, rely=0, relwidth=0.8, relheight=高度)
    选择路径按钮.place(relx=0.8, rely=0, relwidth=0.2, relheight=高度)
    """--------------------------------     主要控件     -------------------------------------------"""
    启动按钮.place(relx=0.3, rely=0.8, relwidth=0.05, relheight=0.07)
    切换账号按钮.place(relx=0.5, rely=0.8, relwidth=0.05, relheight=0.07)
    """----------------------------------  菜单   ---------------------------------------------"""
    菜单()  # 将任务栏菜单放在一个函数
    """---------------------------------  窗口配置  ----------------------------------------"""
    tk.title("原神转服器  bilibili:是惠惠不是惠惠")
    tk.geometry("{}x{}".format(背景图片.width(), 背景图片.height()))  # 图片多大，窗口就多大
    # tk.resizable(False, False)
    tk.iconbitmap("data/资源/图标.ico")
    路径 = 获取路径()
    刷新当前服显示框的字体颜色()
    输出基本信息()
    """---------------------------------  窗口启动  ---------------------------------------------"""
    tk.mainloop()