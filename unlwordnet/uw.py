# !/usr/bin/env python
# -*- coding: utf-8 -*-

class UniversalWord(object):
    headword = None
    constraints = None
    gloss = None
    example = None
    pos = None
    wordnet_id = None

    def __repr__(self):
        return "%s %s" % (self.headword, self.constraints)