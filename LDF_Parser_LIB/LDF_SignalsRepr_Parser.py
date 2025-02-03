#######################################################################
# Name: simple.py
# Purpose: Simple language based on example from pyPEG
# Author: Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# Copyright: (c) 2009-2015 Igor R. Dejanovic <igor DOT dejanovic AT gmail DOT com>
# License: MIT License
#
# This example demonstrates grammar definition using python constructs.
# It is taken and adapted from pyPEG project (see http://www.fdik.org/pyPEG/).
#######################################################################

from __future__ import unicode_literals

import copy 
#import os
from arpeggio import *
from arpeggio import RegExMatch as _

# Grammar
#def simpleLanguage():   return SignalRepr_Block
def SignalRepr_Block():      return Kwd("Signal_representation"), "{", OneOrMore(SignalRepr_Record), "}"
def SignalRepr_Record():     return SignalRepr_Encoder, ":", SignalRepr_EncodedSignal, ZeroOrMore(",",SignalRepr_EncodedSignal), ";"

def SignalRepr_Encoder():       return SignalRepr_symbol
def SignalRepr_EncodedSignal(): return SignalRepr_symbol

def SignalRepr_symbol():    return _(r"\w+")

# Lexer Comments
def comment():          return [_("//.*"), _("/\*.*\*/")] # C comments style

def SignalReprPrint(my_Signals):
    for x in range(len(my_Signals)):
        print (
            "Signal_Encoder: " + my_Signals[x].Encoder
            )
        for y in range(len(my_Signals[x].EncodedSignals)):
            print (
                "\t\t,Signals: " + my_Signals[x].EncodedSignals[y]
                )
    return

class LDF_SignalRepr_Class:
    def __init__(self):
        self.Encoder =""
        self.EncodedSignals = []        
    
class LDF_SignalReprVisitor_Class(PTNodeVisitor):
    PTNodeVisitor.LDF_SignalReprs = []
                
    def visit_SignalRepr_Record(self, node, children):
        if self.debug:
            print (">>> DBG visit_SignalRepr_Record")
            for x in range(len(children)):        
                print (">>> DBG visit_SignalRepr_Record (" + str(x) + ") : " + str(children[x]))
        
        SignalRepr = LDF_SignalRepr_Class()
        SignalRepr.Encoder = children[0]
        EncodedSignals = []
        for x in range(1,len(children)):
            EncodedSignals.append(children[x])
        SignalRepr.EncodedSignals = copy.deepcopy(EncodedSignals)
        
        PTNodeVisitor.LDF_SignalReprs.append(SignalRepr) 
        
        return PTNodeVisitor.LDF_SignalReprs
    