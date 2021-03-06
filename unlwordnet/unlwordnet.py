# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os

from uw import UniversalWord

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp/unl.db')

class UNLWordNet():

    def __init__(self, db=db_path):
        self.db = db
        self.con = sqlite3.connect(self.db)

    def get(self, headword):
        c = self.con.cursor()
        r = []
        for row in c.execute('SELECT * FROM UNLWordNet21 WHERE headword=?', (headword,)):
            uw = UniversalWord()
            uw.headword = row[1]
            uw.example = row[4]
            uw.gloss = row[3]
            uw.pos = row[6]
            uw.wordnet_id = row[8]
            uw.constraints = row[2]
            r.append(uw)
        return r


if __name__ == '__main__':
    import sys
    unl = UNLWordNet()
    r = unl.get(sys.argv[1])
    for row in r:
        print(row)
