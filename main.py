from tkinter import *
import os
import threading
import time
from turtle import width
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

        self.left_frame = Frame(self)
        self.left_frame.pack(side="left")

        self.listbox = Listbox(self.left_frame, selectmode="extended", width=50, height=20)
        self.listbox.bind('<<ListboxSelect>>', self.onSelect)
        self.listbox.pack(side="top", padx=10, pady=10)
        self.fill_listbox_withPosts()

        self.start_btn = Button(self.left_frame, text="기록 시작", padx=10, pady=10, command=self.execute_startBtnCmd)
        self.start_btn.pack(side="bottom")

        self.right_frame = Frame(self)
        self.right_frame.pack(side="right")

        self.imageLabel = Label(self.right_frame)
        self.imageLabel.pack()


    def onSelect(self, event):
        w = event.widget
        value = w.get(w.curselection()[0])
        gall_id = value.split(" │ ")[0]
        with open(os.getcwd()+"/posts/"+gall_id, "r", encoding="utf8") as f:
            f.readline()
        self.photoImage = PhotoImage(file=os.getcwd()+"/screenshots/"+gall_id+".png")
        self.imageLabel.config(image=self.photoImage)

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