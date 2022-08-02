from tkinter import *
import os

class Gui:
    def __init__(self):
        root = Tk()
        root.title("DCArchiver")
        listbox = Listbox(root, selectmode="extended", width=50, height=20)
        listbox.bind('<<ListboxSelect>>', self.onSelect)
        listbox.pack(side="left", padx=10, pady=10)

        right_frame = Frame(root)
        right_frame.pack()

        self.textarea = Text(right_frame, width=30, height=10)
        self.textarea.pack(side="top", padx=10, pady=10)

        # >>> 시작 버튼
        start_btn = Button(right_frame, text="기록 시작", padx=10, pady=10)
        start_btn.pack()

        filenames = os.listdir("./posts")
        for filename in reversed(filenames):
            with open("./posts/"+filename, "r", encoding="utf8") as f:
                listbox.insert(END, filename + " │ " + f.readline())
        root.mainloop()

    def onSelect(self, event):
        # Note here that Tkinter passes an event object to onselect()
        w = event.widget
        value = w.get(w.curselection()[0])

        gall_id = value.split(" │ ")[0]
        with open("./posts/"+gall_id, "r", encoding="utf8") as f:
            f.readline()
            self.textarea.delete("1.0", END)
            self.textarea.insert(END, f.readline())

    def startOrStop_archive(self):
        pass

Gui()