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

import math
import copy
#import os
from arpeggio import *
from arpeggio import RegExMatch as _

# Grammar
#def simpleLanguage():       return Encoding_Block
def Encoding_Block():       return Kwd("Signal_encoding_types"), "{", OneOrMore(Encoding_SignalBlock), "}"
def Encoding_SignalBlock():  return Encoding_SignalName, "{", OneOrMore([Encoding_logical_value, Encoding_physical_value]), "}"

def Encoding_SignalName():      return Encoding_symbol
def Encoding_physical_value():  return Kwd("physical_value"),",", Encoding_PhMinVal,",", Encoding_PhMaxVal,",", Encoding_PhScaling,",", Encoding_PhOffSet, Optional(",",Encoding_PhUnit), ";"
def Encoding_logical_value():   return Kwd("logical_value"),",", Encoding_int_number,",", Encoding_value_quotes, ";"

def Encoding_PhMinVal():    return Encoding_int_number
def Encoding_PhMaxVal():    return Encoding_int_number
def Encoding_PhScaling():   return [Encoding_float_number]
def Encoding_PhOffSet():    return [Encoding_float_number]
def Encoding_PhUnit():      return Encoding_value_quotes

def Encoding_value_quotes():            return '"', Encoding_value_quoted_content, '"'
def Encoding_value_quoted_content():    return _(r'((\\")|[^"])*')

def Encoding_symbol():    return _(r"\w+")
def Encoding_int_number(): return [Encoding_hex_number, Encoding_dec_number]
def Encoding_dec_number():  return _(r'\d+')
def Encoding_hex_number(): return _(r'0x[0-9A-Fa-f]+')
def Encoding_float_number():   return _(r'[-+]?(\d*\.\d*|\d+)')

# Lexer Comments
def comment():          return [_("//.*"), _("/\*.*\*/")] # C comments style


def EncodingPrint(myEncodings):
    for x in range(len(myEncodings)):
        print ("\nEncoding Signal: " + myEncodings[x].Encoder)
        print ("---")
        for y in range(len(myEncodings[x].PhysicalValues)):
            print (
                ("%d" % (y+1)) + 
                ") MinValue: " + ("%d" % (myEncodings[x].PhysicalValues[y]).MinValue) +
                ", MaxValue: " + ("%d" % (myEncodings[x].PhysicalValues[y]).MaxValue) +
                ", Scale: " + ("%.3f" % (myEncodings[x].PhysicalValues[y]).Scale) +
                ", Offset: " + ("%.3f" % (myEncodings[x].PhysicalValues[y]).Offset) +
                ", Unit: " + ((myEncodings[x].PhysicalValues[y]).Unit)
                )
        for y in range(len(myEncodings[x].LogicalValues)):
            print (
                ("%d" % (y+1)) + 
                ") Value: " + ("%d" % (myEncodings[x].LogicalValues[y]).Value) +
                ", Description: " + ((myEncodings[x].LogicalValues[y]).Description) 
                )

class LDF_Encoding_Logical_Class:
    def __init__(self,Value=0,Description=""):
        self.Value = Value
        self.Description = Description
        
class LDF_Encoding_physical_Class:
    def __init__(self,MinValue=0,MaxValue=0,Scale=1.0,Offset=0.0,Unit=""):
        self.MinValue = MinValue
        self.MaxValue = MaxValue
        self.Scale = Scale
        self.Offset = Offset
        self.Unit = Unit
        
class LDF_Encoding_Class:
    def __init__(self):
        self.Encoder = ""
        self.PhysicalValues = []
        self.LogicalValues = []
    
    def get_ranges_tuple_list(self):
        RangeLUT=[]
        Logical = LDF_Encoding_Logical_Class() #redundant code
        for Logical in self.LogicalValues:
            RangeLUT.append( ([Logical.Value],Logical.Description) )
        Physical = LDF_Encoding_physical_Class
        for Physical in self.PhysicalValues:
            Physical_MIN = Physical.MinValue * Physical.Scale + Physical.Offset 
            Physical_MAX = Physical.MaxValue * Physical.Scale + Physical.Offset 
            RangeLUT.append( ([Physical.MinValue, Physical.MaxValue], [Physical_MIN, Physical_MAX], Physical.Unit) )
                
        return RangeLUT

    def ConvertToLinValue(self,InValue):
        if isinstance(InValue, str):
            # Check for Logical
            LogicalVal = LDF_Encoding_Logical_Class()
            for LogicalVal in self.LogicalValues:
                if LogicalVal.Description ==  InValue:
                    return LogicalVal.Value
            # If not found 
            return None
        
        elif isinstance(InValue, float) or isinstance(InValue, int):
            InValue = float(InValue) #Accept integer values and convert them to float 
            # Check for Physical
            PhysicalValue = LDF_Encoding_physical_Class()
            for PhysicalVal in self.PhysicalValues:
                Physical_MIN = PhysicalVal.MinValue * PhysicalVal.Scale + PhysicalVal.Offset 
                Physical_MAX = PhysicalVal.MaxValue * PhysicalVal.Scale + PhysicalVal.Offset 
                if InValue >=Physical_MIN and InValue <= Physical_MAX:
                    # Do conversion
                    return int(math.floor((InValue - PhysicalVal.Offset)/PhysicalVal.Scale)) # Operation Order checked with PeakLIN application                    
            # If not found 
            return None
        
        else:
            return None #Redundant code

    def ConvertToString(self,InValue):
        DecodedStr = ""
        LogicalVal = LDF_Encoding_Logical_Class()
        for LogicalVal in self.LogicalValues:
            if LogicalVal.Value ==  InValue:
                return LogicalVal.Description

        PhysicalValue = LDF_Encoding_physical_Class()
        for PhysicalVal in self.PhysicalValues:
            Physical_MIN = PhysicalVal.MinValue 
            Physical_MAX = PhysicalVal.MaxValue 
            if InValue >=Physical_MIN and InValue <= Physical_MAX:
                # Do conversion
                return "%f" % (InValue * PhysicalVal.Scale + PhysicalVal.Offset)  # Operation Order checked with PeakLIN application                    
            
        # If not found 
        return DecodedStr        

    def ConvertToLogicalPhysical(self,InValue):
        Decoded = None
        LogicalVal = LDF_Encoding_Logical_Class()
        for LogicalVal in self.LogicalValues:
            if LogicalVal.Value ==  InValue:
                return LogicalVal.Description

        PhysicalValue = LDF_Encoding_physical_Class()
        for PhysicalVal in self.PhysicalValues:
            Physical_MIN = PhysicalVal.MinValue 
            Physical_MAX = PhysicalVal.MaxValue 
            if InValue >=Physical_MIN and InValue <= Physical_MAX:
                # Do conversion
                return (InValue * PhysicalVal.Scale + PhysicalVal.Offset)  # Operation Order checked with PeakLIN application                    
            
        # If not found 
        return Decoded        
        
class LDF_EncodingVisitor_Class(PTNodeVisitor):
    PTNodeVisitor.LDF_Encodings = []

    PTNodeVisitor.LDF_physicalVals = []
    PTNodeVisitor.LDF_LogicalVals = []

    def visit_Encoding_float_number(self, node, children):
        if self.debug:
            print (">>> FLOAT_NUMBER : " + node.value)
        return float(node.value)  
    def visit_Encoding_dec_number(self, node, children):
        if self.debug:
            print (">>> DEC_NUMBER : " + node.value)
        return int((node.value),10)
    def visit_Encoding_hex_number(self, node, children):
        if self.debug:
            print (">>> HEX_NUMBER : " + node.value) 
        return int((node.value),16)
    def visit_Encoding_value_quoted_content(self, node, children):
        if self.debug:
            print (">>> QUOTED STRING : " + node.value) 
        return str((node.value))

    def visit_Encoding_PhUnit(self, node, children):
        if self.debug:
            for x in range(len(children)):        
                print (">>> DBG visit_Encoding_PhUnit (" + str(x) + ") : " + str(children[x])) 
        if self.debug:
            for x in range(len(node)):        
                print (">>> DBG visit_Encoding_PhUnit (" + str(x) + ") : " + str(node[x]))
        if len(children)>0:
            return children[0]
        else:
            return "" #if empty quoted values
    
    def visit_Encoding_logical_value(self, node, children):
        if self.debug:
            for x in range(len(children)):        
                print (">>> DBG visit_Encoding_logical_value (" + str(x) + ") : " + str(children[x]))

        Encoding_Logical_Entry = LDF_Encoding_Logical_Class()
        Encoding_Logical_Entry.Value = children[0]
        Encoding_Logical_Entry.Description = children[1]
        PTNodeVisitor.LDF_LogicalVals.append(Encoding_Logical_Entry)
        return PTNodeVisitor.LDF_LogicalVals

    def visit_Encoding_physical_value(self, node, children):
        if self.debug:
            for x in range(len(children)):        
                print (">>> DBG visit_Encoding_physical_value Count(" + str(x) + ") : " + str(children[x]))
        
        Encoding_Physical_Entry = LDF_Encoding_physical_Class()
        Encoding_Physical_Entry.MinValue = children[0]
        Encoding_Physical_Entry.MaxValue = children[1]
        Encoding_Physical_Entry.Scale = children[2]
        Encoding_Physical_Entry.Offset = children[3]
        if len(children)>=5:
            Encoding_Physical_Entry.Unit = children[4]
        else:
            Encoding_Physical_Entry.Unit = ""

        PTNodeVisitor.LDF_physicalVals.append(Encoding_Physical_Entry)
        return PTNodeVisitor.LDF_physicalVals
        
    def visit_Encoding_SignalBlock(self, node, children):
        if self.debug:
            print (">>> DBG visit_Encoding_SignalBlock Logical (" + str(len(PTNodeVisitor.LDF_LogicalVals)) + ")")
            print (">>> DBG visit_Encoding_SignalBlock Physical (" + str(len(PTNodeVisitor.LDF_physicalVals)) + ")")
            for x in range(len(children)):        
                print (">>> DBG visit_Encoding_SignalBlock (" + str(x) + ") : " + str(children[x]))  
        
        Encoder = LDF_Encoding_Class()
        Encoder.Encoder = (children[0])
        Encoder.PhysicalValues = copy.deepcopy(PTNodeVisitor.LDF_physicalVals)
        Encoder.LogicalValues = copy.deepcopy(PTNodeVisitor.LDF_LogicalVals)
    
        PTNodeVisitor.LDF_physicalVals[:] = []
        PTNodeVisitor.LDF_LogicalVals[:] = []
        
        PTNodeVisitor.LDF_Encodings.append(Encoder)
        
        return PTNodeVisitor.LDF_Encodings
    