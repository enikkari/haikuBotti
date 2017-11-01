#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# Hypenation for finnish words
# makes mistakes in compound words
# Rules were derived from the finnish hypenation wikipedia article :)

vowel = {'a', 'e', 'i', 'o', 'u', 'y', 'å'.decode('utf-8'), 'ä'.decode('utf-8'), 'ö'.decode('utf-8')}

diphthong = {'ai', 'ei', 'oi', 'ui', 'yi', 'äi'.decode('utf-8'), 'öi'.decode('utf-8'), 'au', 'eu', 'iu', 'ou',
             'äy'.decode('utf-8'), 'öy'.decode('utf-8'), 'iy', 'ey', 'ie', 'uo', 'yö'.decode('utf-8')}

punct = {'.', ',', ':', ';', '?', '!', '/', '\'', '/"', '-', '(', ')', '[', ']', '{', '}'}


class Hypenator:
    def __init__(self, language):
        print "init hype"
        self.hype = self.fin_hype

    def fin_hype(self, word):
        w = list(word.lower())
        hype = []
        syl = [w[0]]
        for i in range(1, len(w)):
            prw = syl[-1]
            nw = w[i]
            if nw in punct:
                hype.append("".join(syl))
            # hyphenate between two vowels if they don't form a long vowel or diftong
            elif prw in vowel and nw in vowel and prw != nw and (prw + nw) not in diphthong:
                hype.append("".join(syl))
                syl = [nw]
            # hyphenate before consonant that is followed by a vowel
            elif prw not in vowel and nw in vowel and i > 2:
                if len(syl) > 1:
                    hype.append("".join(syl[0:-1]))
                syl = [prw, nw]
            else:
                syl.append(nw)
        hype.append("".join(syl))
        return hype

    def count_syl(self, t_text):
        return sum([len(self.hype(w)) for w in t_text])
