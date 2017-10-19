#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
import random
from Tkinter import *

import src.textgeneration.markovchain as mc

class App(Frame):
    def __init__(self, master):
        frame = Frame(master)
        frame.grid()

        Label(master, text="Inspirational word (in finnish): ").grid(row=1)
        self.inspw = Entry(master)
        self.inspw.grid(row=2)

        self.n = 2

        # TODO: separate ui and corpus generation
        # TODO: link to resources
        all_files = os.listdir('corpora')  # find corpuses  # creativePoems.app/Contents/Resources
        corpus_names = ["".join(["corpora/", f]) for f in all_files if f.endswith('.txt')]
        text_corpora =[]
        for file_name in corpus_names:
            corpus_file = open(file_name)
            corpus_text = corpus_file.read()
            text_corpora.append(corpus_text)
        self.mcs = [mc.MarkovChain(self.n, crps) for crps in text_corpora]

        self.mcK = random.choice(self.mcs)

        self.kalevala_button = Button(frame,
                                      text="kalevala",
                                      command=self.klvl)
        self.kalevala_button.grid(row=0, column=0)

        self.haiku_button = Button(frame,
                                   text="haiku",
                                   command=self.hk)
        self.haiku_button.grid(row=0, column=1)

        self.button = Button(frame,
                             text="text(10)",
                             command=self.txt).grid(row=0, column=2)

        self.msg = StringVar()
        self.msg.set(':)')
        Message(master, textvariable=self.msg).grid(row=3)

        self.cmsg = StringVar()
        self.ncorpuses = len(self.mcs)
        self.cmsg.set(str(self.ncorpuses) + ' corpora in system')
        Message(master, textvariable=self.cmsg).grid(row=5)

        self.T = Text(root, height=4, width=30)
        self.T.grid(row=4, column=0)
        self.T.insert(END, 'Poem will appear here'.decode('utf-8'))

    def choose_corpus(self):
        word = self.inspw.get().lower()
        if word != "":
            filtered = [mc for mc in self.mcs if word in mc.words]
            self.cmsg.set("word in " + str(len(filtered)) + "/" + str(self.ncorpuses) + " corpora")
            if len(filtered) > 0:
                self.msg.set(":)")
                self.mcK = random.choice(filtered)
            else:
                self.msg.set("Not inspired! D:")

    def klvl(self):
        self.choose_corpus()
        self.T.delete(1.0, END)
        self.T.insert(END, self.mcK.kalevala(last_word=self.inspw.get().lower()))

    def hk(self):
        self.choose_corpus()
        self.T.delete(1.0, END)
        self.T.insert(END, self.mcK.haiku(self.inspw.get().lower()))

    def txt(self):
        self.choose_corpus()
        self.T.delete(1.0, END)
        self.T.insert(END, self.mcK.text(10, self.inspw.get().lower()))


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
