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
import copy
from arpeggio import *
from arpeggio import RegExMatch as _

# Grammar
#def simpleLanguage():   return Schedule_Block
#def ScheduleBlockDef():    return Kwd("Schedule_tables"), ScheduleBlock
def Schedule_Block():       return Kwd("Schedule_tables"), "{", OneOrMore(Schedule_EntryBlock), "}"
def Schedule_EntryBlock():  return Schedule_EntryName, "{", OneOrMore([SintaxException1, Schedule_Record]), "}"
def Schedule_Record():      return Schedule_RecordName, "delay", Schedule_RecordDelay, "ms", ";"

def SintaxException1():  return  Schedule_EntryName, "{", Schedule_symbol,",", Schedule_int_number, "}", "delay", Schedule_float_number, "ms", ";"

def extra_field():      return _(r'([^,;\n])+')


def Schedule_EntryName():   return Schedule_symbol        
def Schedule_RecordName():  return Schedule_symbol  
def Schedule_RecordDelay(): return [Schedule_float_number]

def Schedule_symbol():   return _(r"\w+")
def Schedule_float_number():   return _(r'\d*\.\d*|\d+')
def Schedule_int_number():   return [Schedule_hex_number, Schedule_dec_number]
def Schedule_dec_number():   return _(r'\d+')
def Schedule_hex_number():   return _(r'0x[0-9A-Fa-f]+')

# Lexer Comments
def comment():          return [_("//.*"), _("/\*.*\*/")] # C comments style

def SchedulePrint(mySchedules):
    for x in range(len(mySchedules)):
        print (
            "Schedule_Name: " + mySchedules[x].Name
            )
        for y in range(len(mySchedules[x].ScheduleFrames)):
            print (
                "(%d)" % (y+1) +
                ", Frame: " + str( (mySchedules[x].ScheduleFrames[y]).Frame) +
                ", Delay: " + ( "%0.0f[msec]" % (mySchedules[x].ScheduleFrames[y]).Delay )
                )
     
    return

class LDF_ScheduleFrame_Class:
    def __init__(self,frame="",delay=0.0):
        self.Frame = frame
        self.Delay = delay
        
class LDF_Schedule_Class:
    def __init__(self):
        self.Name =""
        self.ScheduleFrames =[]

class LDF_ScheduleVisitor_Class(PTNodeVisitor):
    PTNodeVisitor.LDF_Schedules = []    
    PTNodeVisitor.LDF_SchedulesFrames = []
     
    def visit_Schedule_float_number(self, node, children):
        if self.debug:
            print (">>> DBG FLOAT_NUMBER : " + node.value)
        return float(node.value)
      
    def visit_Schedule_Record(self, node, children):
        if self.debug:
            for x in range(len(children)):        
                print (">>> DBG visit_Schedule_Record (" + str(x) + ") : " + str(children[x]))
        SchedulesFrame = LDF_ScheduleFrame_Class()
        SchedulesFrame.Frame = children[0]
        SchedulesFrame.Delay = children[1]
        PTNodeVisitor.LDF_SchedulesFrames.append(SchedulesFrame)
        return PTNodeVisitor.LDF_SchedulesFrames

    def visit_Schedule_EntryBlock(self, node, children):
        if self.debug:
            for x in range(len(children)):        
                print (">>> DBG visit_Schedule_EntryBlock (" + str(x) + ") : " + str(children[x]))
        Schedule = LDF_Schedule_Class()
        Schedule.Name = str(children[0])
        Schedule.ScheduleFrames = copy.deepcopy(PTNodeVisitor.LDF_SchedulesFrames)

        PTNodeVisitor.LDF_SchedulesFrames[:] = []

        PTNodeVisitor.LDF_Schedules.append(Schedule)

        return PTNodeVisitor.LDF_Schedules

