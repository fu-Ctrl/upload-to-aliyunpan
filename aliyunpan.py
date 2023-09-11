# -*- encoding: utf-8 -*-
# @Time       :  11:44
# @Author     : yuxian
# @Email      : 1503889663@qq.com
# @File       : aliyunpan.py
# @SoftWare   : PyCharm
import json
import os
import tkinter as tk
import requests
from tkinter import messagebox, font
from pynput.mouse import Controller
from tkinter import ttk


class ChoiceAliPath:
    which_data = ''
    path = []
    storage_path = 'config/information.txt'
    file_extensions = [
        ".txt", ".csv", ".xlsx", ".doc", ".pdf", ".jpg", ".png", ".gif", ".mp3", ".mp4",
        ".avi", ".mov", ".html", ".css", ".js", ".py", ".java", ".cpp", ".h", ".xml",
        ".json", ".yaml", ".ini", ".log", ".zip", ".rar", ".tar", ".gz", ".exe", ".dll",
        ".sh", ".bat", ".php", ".html", ".htm", ".md", ".sql", ".rb", ".java", ".c",
        ".class", ".dll", ".jar", ".ppt", ".pptx", ".xls", ".ppt", ".pptx", ".odt",
        ".odp", ".ods", ".tex", ".svg", ".eps", ".bmp", ".tif", ".tiff", ".psd", ".ico",
        ".pptm", ".potx", ".key", ".numbers", ".pages", ".tar.gz", ".tgz", ".bz2", ".7z",
        ".dmg", ".iso", ".img", ".apk", ".ipa", ".woff", ".woff2", ".ttf", ".eot", ".otf",
        ".yaml", ".yml", ".json", ".toml", ".cfg", ".conf", ".config", ".txt", ".md",
        ".rst", ".csv", ".tsv", ".html", ".xml", ".xslt", ".xsd", ".yml", ".yaml",
        ".json", ".jsonl", ".ini", ".cfg", ".conf", ".config", ".log", ".bak", ".old",
        ".tmp", ".swp", ".db", ".dbf", ".sqlite", ".sqlite3", ".dat", ".db2", ".db3",
        ".rdf", ".ttl", ".nt", ".n3", ".csv", ".tsv", ".xls", ".xlsx", ".ods", ".odt",
        ".docx", ".dotx", ".dotm", ".log", ".xml", ".pdf", ".pptx", ".xlsx", ".xlsm",
        ".docx", ".dotx", ".dotm", ".jpeg", ".webp", ".tiff", ".jfif", ".avif", ".bmp",
        ".ico", ".raw", ".ps", ".eps", ".svgz", ".ai", ".avi", ".flv", ".mkv", ".wmv",
        ".mov", ".mpeg", ".mpg", ".webm", ".wav", ".flac", ".m4a", ".ogg", ".aac", ".wma",
        ".3gp", ".webm", ".mp3", ".m4v", ".mp4", ".ogg", ".wmv", ".mkv", ".mov", ".vob",
        ".flv", ".avi", ".swf", ".exe", ".msi", ".bat", ".sh", ".cmd", ".com", ".jar",
        ".pyc", ".class", ".obj", ".dll", ".lib", ".a", ".so", ".dylib", ".h", ".hpp",
        ".c", ".cpp", ".cs", ".java", ".js", ".php", ".html", ".htm", ".css", ".scss",
        ".less", ".sass", ".jsx", ".tsx", ".vue", ".ts", ".rb", ".pl", ".perl", ".cgi",
        ".pm", ".sql", ".mysql", ".sqlite", ".pgsql", ".mssql", ".db2", ".oracle", ".postgres",
        ".sqlitedb", ".bak", ".gho", ".iso", ".img", ".vhd", ".vmdk", ".bak", ".log",
        ".old", ".tmp", ".swp", ".db", ".dbf", ".sqlite", ".sqlite3", ".dat", ".db2",
        ".db3", ".rdf", ".ttl", ".nt", ".n3", ".csv", ".tsv", ".xls", ".xlsx", ".ods",
        ".odt", ".docx", ".dotx", ".dotm", ".log", ".xml", ".pdf", ".pptx", ".xlsx",
        ".xlsm", ".docx", ".dotx", ".dotm", ".jpeg", ".webp", ".tiff", ".jfif", ".avif",
        ".bmp", ".ico", ".raw", ".ps", ".eps", ".svgz", ".ai", ".avi", ".flv", ".mkv",
        ".wmv", ".mov", ".mpeg", ".mpg", ".webm", ".wav", ".flac", ".m4a", ".ogg", ".aac",
        ".wma", ".3gp", ".webm", ".mp3", ".m4v", ".mp4", ".ogg", ".wmv", ".mkv", ".mov",
        ".vob", ".flv", ".avi", ".swf", ".exe", ".msi", ".bat", ".sh", ".cmd", ".com",
        ".jar", ".pyc", ".class", ".obj", ".dll", ".lib", ".a", ".so", ".dylib", ".h",
        ".hpp", ".c", ".cpp", ".cs", ".java", ".js", ".php", ".html", ".htm", ".css",
        ".scss", ".less", ".sass", ".jsx", ".tsx", ".vue", ".ts", ".rb", ".pl", ".perl",
        ".cgi", ".pm", ".sql", ".mysql", ".sqlite", ".pgsql", ".mssql", ".db2", ".oracle",
        ".postgres", ".sqlitedb", ".bak", ".gho", ".iso", ".img", ".vhd", ".vmdk", ".ASF",
        ".whl", ".ipynb", ".temp"
    ]

    def __init__(self, root=tk.Tk()):
        # 用于存储数据
        self.data = []
        self.activate_num_list = []
        self.level = 1

        # 1 确认选择退出  2 取反
        self.normal_exit = None

        # 当前高亮的颜色
        self.activate = 0

        root.attributes('-alpha', 0.85)
        root.overrideredirect(True)  # 删除标题栏
        root.attributes("-topmost", 1)
        mouse = Controller()
        x, y = mouse.position
        self.root = root
        # self.root.title("My App")
        self.root.geometry(f"400x210+{x + 410}+{y}")

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        self.file_menu1 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="帮助", menu=self.file_menu1)
        self.file_menu1.add_command(label="说明", command=self.explain_function)

        self.file_menu2 = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="操作", menu=self.file_menu2)
        self.file_menu2.add_command(label="确认选择", command=self.agree)
        self.file_menu2.add_command(label="退出选择", command=self.exit1)

        # 创建主框架
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(expand=True, fill="both")

        # 创建列表框
        MyFont = font.Font(family="./github.ttf", size=12, weight="bold")
        self.listbox = tk.Listbox(self.main_frame, bg='white', activestyle="none", selectmode=tk.SINGLE,
                                  selectborderwidth=0, selectbackground='white',
                                  selectforeground='skyblue', font=MyFont)
        self.listbox.pack(expand=True, fill="both")

        self.load_data()
        self.update_listbox()

        # 列表元素点击事件
        self.listbox.bind("<Button-1>", self.get_choice)
        self.listbox.bind("<Double-1>", self.on_listbox_Double)
        self.listbox.bind("<Button-3>", self.on_listbox_right_click)
        self.listbox.bind("<Up>", self.Key_UP)
        self.listbox.bind("<Down>", self.Key_down)
        self.listbox.bind("<Return>", self.agree)



    def load_data(self):
        try:
            response = requests.get("http://127.0.0.1:57801/MP4")
            if response.status_code == 200:
                self.data.append([i for i in response.json()['data'] if "." + i['name'].split('.')[-1].split('.')[0].lower() not in self.file_extensions])
        except Exception as e:
            messagebox.showerror("错误", str(e))
        self.listbox.select_set(self.activate)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.data[self.level - 1]:
            self.listbox.insert(tk.END, item['name'])
        self.listbox.select_set(self.activate)

    def on_listbox_Double(self, event):
        index = self.listbox.nearest(event.y)
        selected_item = self.data[self.level - 1][index]
        resp = self.load_next_data(selected_item)

        self.activate = 0
        self.update_listbox()

        if resp != '没有内容':
            self.activate_num_list.append(index)
        # elif self.level == 1:
        #     self.activate_num_list.append(index)

    def load_next_data(self, selected_item):
        try:
            response = requests.get(f"http://127.0.0.1:57801/MP4list?id={selected_item['id']}")
            if response.status_code == 200:
                if not response.json()['data']:
                    return 0
                response1 = []
                for i in response.json()['data']:
                    if "." + i['name'].split('.')[-1].split('.')[0].lower() not in self.file_extensions:
                        response1.append(i)
                if len(response1) == 0:
                    return "没有内容"
                self.data.append(response1)
                self.level += 1
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def on_listbox_right_click(self, event):
        if self.level == 1:
            return 0
        self.level -= 1
        self.data = self.data[:-1]

        self.activate = self.activate_num_list[-1]
        self.update_listbox()
        self.activate_num_list = self.activate_num_list[:-1]

    def get_choice(self, event):
        index = self.listbox.nearest(event.y)
        self.listbox.select_set(index)
        self.activate = index

    def Key_UP(self, event):
        if self.activate == 0:
            return 0
        self.activate -= 1
        self.listbox.selection_clear(0, tk.END)
        self.listbox.select_set(self.activate)

    def Key_down(self, event):
        if self.activate == len(self.data[self.level - 1]) - 1:
            return 0
        self.activate += 1
        self.listbox.selection_clear(0, tk.END)
        self.listbox.select_set(self.activate)

    def explain_function(self):
        messagebox.showinfo("提示", "功能如下:\n1. 按钮 ↑ 上移\n2. 按钮 ↓ 下移\n3. 鼠标左键单击 选中\n4. 按钮 Enter 确认当前选项\n5. 鼠标左键双击 进入下一级\n6. 鼠标右键单击 返回上一级")

    def agree(self, event=None):
        self.which_data = self.data[self.level - 1][self.activate]

        self.activate_num_list.append(self.activate)
        path = [item[self.activate_num_list[index]]['name'] for index,item in enumerate(self.data)]
        self.path = path
        self.root.quit()
        self.normal_exit = 1

    def exit1(self):
        self.normal_exit = 2
        self.root.quit()

    def run(self):
        self.root.mainloop()
        if self.normal_exit not in [None, 2]: # 确认了选择
            dir_,file = self.storage_path.split('/')
            if not os.path.exists(dir_):
                os.mkdir(dir_)
            with open(self.storage_path,'w',encoding='utf-8') as  fp:
                fp.write(json.dumps({'path': '/'.join(self.path), "info": self.which_data}))
                fp.flush()
                fp.close()
            print(json.dumps({'path': '/'.join(self.path), "info": self.which_data}))

if __name__ == "__main__":
    # 开发调试代码
    # root = tk.Tk()
    # app = MyApp(root)
    # app.run()
    #  工作代码
    ChoiceAliPath().run()
    # main()
