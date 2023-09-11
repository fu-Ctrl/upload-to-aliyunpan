# -*- encoding: utf-8 -*-
# @Time       :  11:42
# @Author     : yuxian
# @Email      : 1503889663@qq.com
# @File       : UpLoad.py
# @SoftWare   : PyCharm
import json
import os
import subprocess
import tkinter as tk
from tkinter import font
from tkinterdnd2 import DND_FILES, TkinterDnD
from pynput.mouse import Controller
import requests


class FileDragAndDropApp:
    storage_path = 'config/information.txt'
    item = {}

    def __init__(self, root):
        # 上一次上传的路径
        if not os.path.exists(self.storage_path):
            self.last_choice_path = "上一次选择的云盘路径:\t\t\t\t\t\n/"
        else:
            fp = open(self.storage_path, 'r', encoding='utf-8')
            self.item = json.load(fp)
            if len(self.item['path']) > 30:
                str1 = self.item['path'].split('/')[:-1]
                str1.insert(int(len(str1) / 2), "\n")
                self.item["path"] = "/".join(str1).split('\n')[0][:-1] + "/\n" + ".../" + self.item['path'].split('/')[
                    -1]
            self.last_choice_path = "上一次选择的云盘路径:\t\t\t\t\t\n/" + self.item['path']
            fp.close()

        self.root = root
        # self.root.title("文件拖拽示例")
        root.attributes('-alpha', 0.85)
        root.attributes("-topmost", 2)
        root.overrideredirect(True)  # 删除标题栏
        mouse = Controller()
        x = root.winfo_screenwidth()  # 获取电脑屏幕的宽，
        y = root.winfo_screenheight()
        mouse_x, mouse_y = mouse.position
        if mouse_x < x * 0.1 and mouse_y < y * 0.1:
            x = int(x / 2)
            y = int(y / 2)
        if x - mouse_x < 400 or mouse_y - y < 200:
            x = int(x / 2)
            y = int(y / 2)
        self.root.geometry(f"400x210+{x}+{y}")
        # 创建一个显示上一次 上传路径

        self.label1_string = tk.StringVar()

        self.label1_string.set(self.last_choice_path)

        self.file_path_label1 = tk.Label(root, textvariable=self.label1_string, padx=10, pady=10)
        # 创建一个标签来显示文件路径
        MyFont = font.Font(family="./github.ttf", size=14, weight="bold")
        self.file_path_label2 = tk.Label(root, text="上传到阿里云盘", padx=400, pady=200, bg='lightblue', font=MyFont)
        self.file_path_label1.pack()
        self.file_path_label2.pack()

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        self.file_menu1 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="选择", menu=self.file_menu1)
        self.file_menu1.add_command(label="选则您要上传的路径", command=self.get_choice_path)

        self.file_menu2 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="操作", menu=self.file_menu2)
        self.file_menu2.add_command(label="退出上传", command=root.quit)

        # 在标签上启用拖放功能
        self.file_path_label2.drop_target_register(DND_FILES)
        self.file_path_label2.dnd_bind('<<Drop>>', self.handle_drop)

    def handle_drop(self, event):
        # 获取拖放的文件或文件夹路径
        file_path = event.data
        print(file_path)
        self.file_path_label2.config(text=f'本地文件/文件夹路径: \t\t\n\n{file_path}')
        self.root.wm_attributes('-topmost', 0)
        requests.post('http://127.0.0.1:57801/upload', data=json.dumps({"info": self.item['info'], "path": file_path}))
        self.root.quit()

    def get_choice_path(self):
        result = subprocess.run(['python aliyunpan.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # # 输出标准输出和标准错误
        # print("标准输出:", result.stdout)
        # print("标准错误:", result.stderr)
        #
        # # 获取返回值
        # return_code = result.returncode
        # print("返回值:", return_code)
        if result.returncode == 0 and result.stdout:
            self.item = json.loads(result.stdout)
            if len(self.item['path']) > 30:
                str1 = self.item['path'].split('/')[:-1]
                str1.insert(int(len(str1) / 2), "\n")
                self.item["path"] = "/".join(str1).split('\n')[0][:-1] + "/\n" + ".../" + self.item['path'].split('/')[
                    -1]
            self.label1_string.set("当前选择的云盘路径:\t\t\t\t\t\t\n/" + self.item["path"])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = FileDragAndDropApp(root)
    app.run()
