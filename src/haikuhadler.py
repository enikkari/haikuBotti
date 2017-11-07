#!/usr/bin/env python
# -*- coding: utf-8 -*-

from textgeneration.markovchain import MarkovChain
import os
import random

class HaikuHandler:

    def __init__(self, corporafolder, n, language='finnish'):
        self.markovchains_list = list()

        for corpus_file_name in os.listdir(corporafolder):
            full_corpus_file_name = os.path.join(corporafolder, corpus_file_name)
            print("create markov chain on " + full_corpus_file_name)
            content = self.get_text(full_corpus_file_name)
            mc = MarkovChain(n, content)
            self.markovchains_list.append(mc)

    def get_text(self, filename):
        with open(filename, 'r+') as f:
            text = f.read()
        return text

    def get_haiku(self, inspirational_word = ""):
        markov_chain = self.choose_chain(inspirational_word)
        return markov_chain.haiku(inspirational_word)

    def choose_chain(self, inspirational_word):
        word = inspirational_word.lower()
        filtered_chains = [markovchain
                           for markovchain in self.markovchains_list
                           if word in markovchain.words]
        if word != "" and len(filtered_chains) > 0:
            return random.choice(filtered_chains)
        else:
            print("word " + word + " not in any of the corpora")
            return random.choice(self.markovchains_list)


if __name__ == '__main__':
    print os.getcwd()
    h = HaikuHandler("../corpora/", 2)
    print("")
    print(h.get_haiku("orressa"))
    print("")
    print(h.get_haiku("äiti"))


