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
#def simpleLanguage():   return Frames_Block
def Frames_Block():     return Kwd("Frames"), "{", OneOrMore(Frames_Frame), "}"
def Frames_Frame():     return FrameName,":", FrameID, ",", FrameNode, ",", FrameByteLen, "{", OneOrMore(Frames_Signal), "}"
def Frames_Signal():    return SignalName, ",", SignalOffSet, ";"

def MasterName():       return Frames_symbol
def SlaveName():        return Frames_symbol
#def extra_field():      return _(r'([^,;\n])+')
#def Frames_symbol():           return _(r"\w+")

def FrameName():    return Frames_symbol         
def FrameNode():    return Frames_symbol
def FrameID():      return Frames_int_number
def FrameByteLen(): return Frames_int_number #Frame_dec_number()
def SignalName():   return Frames_symbol  
def SignalOffSet(): return Frames_int_number #Frame_dec_number()

def Frames_symbol():    return _(r"\w+")
def Frames_int_number(): return [Frames_hex_number, Frames_dec_number]
def Frames_dec_number():  return _(r'\d+')
def Frames_hex_number(): return _(r'0x[0-9A-Fa-f]+')

# Lexer Comments
def comment():          return [_("//.*"), _("/\*.*\*/")] # C comments style


def FramesPrint(myFrames):
    for x in range(len(myFrames)):
        print (
            "Frame_Name: " + myFrames[x].Name +
            ", Node: " + myFrames[x].Node +
            ", ID: " + ("0x%02x" % (myFrames[x].ID)) +
            ", LEN: " + ("%02d" % (myFrames[x].LEN))
            )
        for y in range(len(myFrames[x].FrameSignals)):
            print (
                "Frame_Signal: " + str( (myFrames[x].FrameSignals[y]).Signal) +
                ", Offset: " + ("%02d" %  (myFrames[x].FrameSignals[y]).BitOffset)
                )         
    return

class LDF_FrameSignal_Class:
    def __init__(self):
        self.Signal =""
        self.BitOffset = 0

class LDF_Frame_Class:
    def __init__(self):
        self.Name =""
        self.Node =""
        self.ID = 0
        self.LEN = 0
        self.FrameSignals =[]



class LDF_FramesVisitor_Class(PTNodeVisitor):
    PTNodeVisitor.LDF_Frames = []
    PTNodeVisitor.LDF_FramesSignal = []
       
    def visit_Frames_dec_number(self, node, children):
        if self.debug:
            print (">>> DEC_NUMBER : " + node.value)
        return int((node.value),10)
    def visit_Frames_hex_number(self, node, children):
        if self.debug:
            print (">>> HEX_NUMBER : " + node.value) 
        return int((node.value),16)

    def visit_Frames_Signal(self, node, children):
        if self.debug:
            for x in range(len(children)):        
                print (">>> DBG visit_Frames_Signal Count(" + str(x) + ") : " + str(children[x]))
        
        Signal = LDF_FrameSignal_Class()
        Signal.Signal = children[0]
        Signal.BitOffset = children[1]
        PTNodeVisitor.LDF_FramesSignal.append(Signal)

        return PTNodeVisitor.LDF_Frames
                
    def visit_Frames_Frame(self, node, children):
        if self.debug:
            for x in range(len(children)):        
                print (">>> DBG visit_Frames_Frame Count(" + str(x) + ") : " + str(children[x]))
                
        Frame = LDF_Frame_Class()
        Frame.Name  = children[0]
        Frame.ID    = children[1]
        Frame.Node  = children[2]
        Frame.LEN   = children[3]
        Frame.FrameSignals = PTNodeVisitor.LDF_FramesSignal
        PTNodeVisitor.LDF_FramesSignal = []
        
        PTNodeVisitor.LDF_Frames.append(Frame)

        return PTNodeVisitor.LDF_Frames
    


