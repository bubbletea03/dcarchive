from tkinter import *
import os
import threading
import time
import recorder
import sys

def main():
    if not os.path.exists(os.getcwd()+"/posts"): # 디렉토리 없으면 자동생성
        os.makedirs(os.getcwd()+"/posts")
    if not os.path.exists(os.getcwd()+"/screenshots"):
        os.makedirs(os.getcwd()+"/screenshots")

    root = App()
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    root.mainloop()

class App(Tk):

    isArchiving = False

    def __init__(self) -> Tk:
        super().__init__()
        self.title("dcArchiver")

        self.listbox = Listbox(self, selectmode="extended", width=50, height=20)
        self.listbox.bind('<<ListboxSelect>>', self.onSelect)
        self.listbox.pack(side="left", padx=10, pady=10)
        self.fill_listbox_withPosts()

        self.right_frame = Frame(self)
        self.right_frame.pack()

        self.textarea = Text(self.right_frame, width=30, height=10)
        self.textarea.pack(side="top", padx=10, pady=10)

        self.start_btn = Button(self.right_frame, text="기록 시작", padx=10, pady=10, command=self.execute_startBtnCmd)
        self.start_btn.pack()

    def onSelect(self, event):
        w = event.widget
        value = w.get(w.curselection()[0])
        gall_id = value.split(" │ ")[0]
        with open(os.getcwd()+"/posts/"+gall_id, "r", encoding="utf8") as f:
            f.readline()
            self.textarea.delete("1.0", END)
            self.textarea.insert(END, f.readline())

    def fill_listbox_withPosts(self):
        self.listbox.delete(0, END)
        filenames = os.listdir(os.getcwd()+"/posts")
        for filename in reversed(filenames):
            with open(os.getcwd()+"/posts/"+filename, "r", encoding="utf8") as f:
                self.listbox.insert(END, filename + " │ " + f.readline())

    def execute_startBtnCmd(self):
        if(self.isArchiving != True):
            self.isArchiving = True
            self.start_btn.config(text="중지")
            threading.Thread(target=self.loop_saveArchive).start()
            threading.Thread(target=self.loop_fillListbox).start()
        else:
            self.isArchiving = False
            self.start_btn.config(text="기록 시작")

    def loop_saveArchive(self):
        while(self.isArchiving == True):
            recorder.save_pageArchive()

    def loop_fillListbox(self):
        while(self.isArchiving == True):
            self.fill_listbox_withPosts()
            time.sleep(5)


if __name__ == "__main__":
    main()