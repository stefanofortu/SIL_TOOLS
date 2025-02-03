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

#import os
from arpeggio import *
from arpeggio import RegExMatch as _

# Grammar
#def simpleLanguage():   return Signals_Block
def Signals_Block():      return Kwd("Signals"), "{", OneOrMore(Signals_Record), "}"
def Signals_Record():     return Signals_Name, ":", Signals_BitLen, ",", Signals_InitVal, ",", Signals_PubNode, OneOrMore(",",Signals_SubNode), ";"

def Signals_Name():     return Signals_symbol
def Signals_BitLen():   return Signals_int_number
def Signals_InitVal():  return Signals_int_number
def Signals_PubNode():  return Signals_symbol
def Signals_SubNode():  return Signals_symbol

#def Signals_GenericExpression(): return _(r'([^,;\n])+')
#def Signals_symbol():            return _(r"\w+")

def Signals_symbol():    return _(r"\w+")
def Signals_int_number(): return [Signals_hex_number, Signals_dec_number]
def Signals_dec_number():  return _(r'\d+')
def Signals_hex_number(): return _(r'0x[0-9A-Fa-f]+')

# Lexer Comments
def comment():          return [_("//.*"), _("/\*.*\*/")] # C comments style

def SignalsPrint(my_Signals):
    for x in range(len(my_Signals)):
        subs=""
        for y in range(len(my_Signals[x].Subscribers)):
            subs = subs + my_Signals[x].Subscribers[y] + ", "
        print (
            "Signal_Name: " + my_Signals[x].Name +
            ", BitLen: " + ("%d" % my_Signals[x].BitLen) +
            ", InitVal: " + ("0x%02X" % my_Signals[x].InitVal) +
            ", Pub: " + my_Signals[x].Publisher +
            ", Sub: " + subs
            )
    return

class LDF_Signal_Class:
    def __init__(self):
        self.Name =""
        self.BitLen = 0
        self.InitVal = 0
        self.Publisher = ""
        self.Subscribers = []        
    
class LDF_SignalsVisitor_Class(PTNodeVisitor):
    PTNodeVisitor.LDF_Signals = []
    
    def visit_Signals_dec_number(self, node, children):
        if self.debug:
            print (">>> DEC_NUMBER : " + node.value)
        return int((node.value),10)
    def visit_Signals_hex_number(self, node, children):
        if self.debug:
            print (">>> HEX_NUMBER : " + node.value) 
        return int((node.value),16)
    
    def visit_Signals_Record(self, node, children):
        if self.debug:
            for x in range(len(children)):        
                print (">>> DBG visit_Signals_Record (" + str(x) + ") : " + str(children[x]))
        Signal = LDF_Signal_Class()

        Signal.Name = children[0]
        Signal.BitLen = children[1]
        Signal.InitVal = children[2]
        Signal.Publisher = children[3]
        for x in range(4,len(children)):
            Signal.Subscribers.append(children[x])

        PTNodeVisitor.LDF_Signals.append(Signal)
        return PTNodeVisitor.LDF_Signals
    

