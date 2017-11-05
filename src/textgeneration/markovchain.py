#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import random
import re
import string

import haikubotti.src.textgeneration.hypenator as hp


# TODO: implement markov chain as a ngram model in ARPA format with back-off
# current method is ineffective with large corpora

def get_words(text):
    text = re.sub("-", " ", text)
    exclude = string.punctuation + '0123456789' +"\.-"+ "\"" +"”“”–" #string.punctuation
    exclude = exclude.decode("utf-8")
    regex = re.compile('[%s]' % re.escape(exclude))
    text = text.lower()
    text = regex.sub(' ', text)
    tokens = text.split()
    return tokens

class MarkovChain:
    def __init__(self, n, corpus="", language='finnish'):
        self.n = n
        self.map = {}
        self.map[""] = [""]
        self.words = []
        self.hype = hp.Hypenator(language)
        self.learn(corpus)

    def learn(self, content):
        if len(content)>0:
            t_content = get_words(content)
            map = self.map
            self.words = list(set(self.words + t_content))
            n= self.n
            for i in range(0, len(t_content)):
                word = t_content[i]  # huom
                for j in range(0, n + 1):
                    key = " ".join(t_content[i + 1: i + 1 + j])
                    if key in map:
                        map[key].append(word)
                    else:
                        map[key] = [word]
        else:
            print("No content in corpus")

    def text(self, nwords, last_word=""):
        state = last_word
        if state == "":
            state = random.choice(self.words)
        text = [state]
        for i in range(1, nwords):
            if (state not in self.map.keys()):
                state = random.choice(self.map.keys())  # huom
            word = random.choice(self.map[state])
            text = [word] + text
            state = " ".join(text[0:self.n])
        return text

    # check a long sequence of tokenized words for n ones that matches the Kalevala restrictions
    def kalevala(self, nlines=4, last_word=""):
        tn = 100
        lines = []
        iterations = 0
        while len(lines) < nlines and iterations < 4:
            text = self.text(tn, last_word)
            a = 0
            b = 1
            while b < tn and a < tn:
                syl = self.hype.count_syl(text[a:b])
                if syl < 8:
                    b = b + 1
                elif syl > 8:
                    a = a + 1
                else:
                    """8 syllables in sequence
					 check if at least two of the words have same first letter """
                    first_letters = [list(w)[0] for w in text[a:b]]
                    set_first_letters = set(first_letters)
                    uniq = len(set_first_letters)
                    words = len(first_letters)
                    if uniq <= 2 and words > uniq:
                        lines.append(" ".join(text[a:b]))
                        a = b
                        b = b + 1
                        if len(lines) == nlines:
                            break
                    else:
                        a = a + 1
            iterations = iterations + 1
        if iterations == 4 and len(lines) != 4:
            print "not enough lines found"
        poem = "\n".join(lines)
        print poem
        return poem

    def haiku(self, last_word=""):
        # 5-7-5
        tn = 15
        poem = ['none found']
        iterations = 0
        while iterations < 10:
            text = self.text(tn, last_word)
            a = 0
            b = 1
            while b < tn and a < tn:
                syl = self.hype.count_syl(text[a:b])
                if syl < 17:
                    b = b + 1
                elif syl > 17:
                    a = a + 1
                else:
                    c = a + 1
                    d = b - 1
                    while self.hype.count_syl(text[a:c]) < 5:
                        c = c + 1
                    while self.hype.count_syl(text[d:b]) < 5:
                        d = d - 1
                    if self.hype.count_syl(text[a:c]) == 5 and self.hype.count_syl(
                            text[c:d]) == 7 and self.hype.count_syl(text[d:b]) == 5:
                        poem = [text[a:c], text[c:d], text[d:b]]
                        poem = [" ".join(l) for l in poem]
                        break
                    else:
                        a = a + 1
            iterations = iterations + 1
        joined_poem = "\n".join(poem)
        return joined_poem
