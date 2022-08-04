from tkinter import *
import os
import asyncio

def main():
    root = App()
    root.mainloop()

class App(Tk):
    def __init__(self) -> Tk:
        super().__init__()
        self.title("dcArchiver")

        self.listbox = Listbox(self, selectmode="extended", width=50, height=20)
        self.listbox.bind('<<ListboxSelect>>', self.onSelect)
        self.listbox.pack(side="left", padx=10, pady=10)
        self.fill_listbox_withPosts(self.listbox)

        self.right_frame = Frame(self)
        self.right_frame.pack()

        self.textarea = Text(self.right_frame, width=30, height=10)
        self.textarea.pack(side="top", padx=10, pady=10)

        Button(self.right_frame, text="기록 시작", padx=10, pady=10).pack()

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

    async def start_archive(self):
        while True:
            print("test")
            await asyncio.sleep(1)



if __name__ == "__main__":
    main()