from tkinter import *
import os
import threading
import time
import recorder

def main():
    root = App()
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

        Button(self.right_frame, text="기록 시작", padx=10, pady=10, command=self.execute_startBtnCmd).pack()

    def onSelect(self, event):
        w = event.widget
        value = w.get(w.curselection()[0])
        gall_id = value.split(" │ ")[0]
        with open("./posts/"+gall_id, "r", encoding="utf8") as f:
            f.readline()
            self.textarea.delete("1.0", END)
            self.textarea.insert(END, f.readline())

    def fill_listbox_withPosts(self):
        filenames = os.listdir("./posts")
        for filename in reversed(filenames):
            with open("./posts/"+filename, "r", encoding="utf8") as f:
                self.listbox.insert(END, filename + " │ " + f.readline())

    def execute_startBtnCmd(self):
        if(self.isArchiving != True):
            self.isArchiving = True
            threading.Thread(target=self.loop_saveArchive).start()
        else:
            self.isArchiving = False

    def loop_saveArchive(self):
        while(self.isArchiving == True):
            recorder.save_pageArchive()
            self.update()
            SAVE_INTERVAL = 30
            time.sleep(SAVE_INTERVAL)


if __name__ == "__main__":
    main()