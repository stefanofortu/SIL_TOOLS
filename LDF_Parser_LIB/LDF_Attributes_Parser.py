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
from arpeggio import *
from arpeggio import RegExMatch as _

# Grammar
def Attributes_Block():     return Kwd("Node_attributes"), "{", OneOrMore(Attributes_NodeBlock), "}"
def Attributes_NodeBlock(): return NodeName, "{", OneOrMore(Attributes_Entry), "}"
def Attributes_Entry():     return [
        Attributes_NAD_Entry,
        Attributes_ProductID_Entry,
        Attributes_ConfFramesBlock,
        Attributes_RespErr_Entry,
        Attributes_GenericEntry ]
def NodeName():  return Attributes_symbol()
##########################################

# Generic used to avoid to parse everything 
def Attributes_GenericEntry():     return [ Attributes_GenericBlock, Attributes_GenericExpression ]
def Attributes_GenericBlock():      return Attributes_BlockName, "{", OneOrMore(Attributes_GenericEntry), "}"
def Attributes_BlockName():         return Attributes_symbol()
def Attributes_GenericExpression(): return Attributes_GenericExpressionName, Optional("=", Attributes_GenericExpressionValue), ";"
def Attributes_GenericExpressionName(): return Attributes_symbol()
def Attributes_GenericExpressionValue():   return _(r'([^;\n])+')
##########################################

def Attributes_NAD_Entry(): return Kwd("configured_NAD"), "=", Attributes_NADValue, ";"
def Attributes_NADValue():             return Attributes_int_number()
##########################################

def Attributes_RespErr_Entry(): return Kwd("response_error"), "=", Attributes_RespErr, ";"
def Attributes_RespErr():       return Attributes_symbol()
##########################################

# product_id=0x0000, 0x0000, 0x00;
def Attributes_ProductID_Entry(): return Kwd("product_id"), "=", Attributes_SupplyerID, ",", Attributes_FunctionID, ",", Attributes_VariantID, ";"
def Attributes_SupplyerID():    return Attributes_int_number
def Attributes_FunctionID():    return Attributes_int_number
def Attributes_VariantID():    return Attributes_int_number
##########################################

def Attributes_ConfFramesBlock():   return Kwd("configurable_frames"), "{", OneOrMore(Attributes_MessageIDEntry), "}"
def Attributes_MessageIDEntry():    return Attributes_MessageIDName, "=", Attributes_MessageID, ";"
def Attributes_MessageIDName():     return Attributes_symbol()
def Attributes_MessageID():         return Attributes_int_number()
##########################################

def Attributes_symbol():        return _(r"\w+")
def Attributes_int_number():    return [Attributes_hex_number, Attributes_dec_number]
def Attributes_dec_number():    return _(r'\d+')
def Attributes_hex_number():    return _(r'0x[0-9A-Fa-f]+')
##########################################


def AttributesPrint(LDF_Attributes):
    for x in range(len(LDF_Attributes)):
        print("Node: "+ LDF_Attributes[x].NodeName )
        print("response_error:  "+ ("%s" % LDF_Attributes[x].response_error) )
        print("NAD:  "+ ("0x%02X" % LDF_Attributes[x].NAD) )
        print("SupplyerID:  "+ ("0x%04X" % LDF_Attributes[x].SupplyerID) )    
        print("FunctionID:  "+ ("0x%04X" % LDF_Attributes[x].FunctionID) )
        print("VariantID:  "+ ("0x%02X" % LDF_Attributes[x].VariantID) )
        print("ConfigurableFrames: ")
        for y in range(len(LDF_Attributes[x].ConfigurableFrames)):
            print ( "\t" + LDF_Attributes[x].ConfigurableFrames[y].FrameName + " = " +("0x%04X" % LDF_Attributes[x].ConfigurableFrames[y].MessageID) )
        
class LDF_ConfigurableFrame_Class:
    def __init__(self):
        self.FrameName = ""
        self.MessageID = 0x0000
        
class LDF_Attributes_Class:
    def __init__(self):
        self.NodeName = ""
        self.response_error = ""
        self.NAD = 0xFF
        self.SupplyerID = 0x0000
        self.FunctionID = 0x0000
        self.VariantID = 0x00
        self.ConfigurableFrames = []

class LDF_AttributesVisitor_Class(PTNodeVisitor):
    PTNodeVisitor.LDF_Attributes = []
    PTNodeVisitor.response_error = ""
    PTNodeVisitor.NAD = 0
    PTNodeVisitor.SupplyerID = 0
    PTNodeVisitor.FunctionID = 0
    PTNodeVisitor.VariantID = 0
    
    PTNodeVisitor.LDF_ConfigurableFrames = [] # Questa lista non ha bisogno della prima struttura

    def visit_Attributes_dec_number(self, node, children):
        if self.debug:
            print (">>> DEC_NUMBER : " + node.value)
        return int((node.value),10)
    def visit_Attributes_hex_number(self, node, children):
        if self.debug:
            print (">>> HEX_NUMBER : " + node.value) 
        return int((node.value),16)
        
    def visit_Attributes_NodeBlock(self, node, children):
        if self.debug:
            print (">>> DBG visit_Attributes_NodeBlock,   ", str(node.value))
            for x in range(len(children)):        
                print (">>> DBG visit_Attributes_NodeBlock (" + str(x) + ") : " + str(children[x]))
        
        Attributes = LDF_Attributes_Class()
        Attributes.NodeName = str(children[0])
        Attributes.response_error = PTNodeVisitor.response_error
        Attributes.NAD = PTNodeVisitor.NAD
        Attributes.SupplyerID = PTNodeVisitor.SupplyerID
        Attributes.FunctionID = PTNodeVisitor.FunctionID
        Attributes.VariantID = PTNodeVisitor.VariantID 
        Attributes.ConfigurableFrames = copy.deepcopy(PTNodeVisitor.LDF_ConfigurableFrames)
        
        PTNodeVisitor.LDF_ConfigurableFrames[:] = []

        PTNodeVisitor.LDF_Attributes.append(Attributes)
        
        return PTNodeVisitor.LDF_Attributes
    
    def visit_Attributes_NADValue(self, node, children):
        if self.debug:        
            for x in range(len(children)):        
                print (">>> DBG visit_Attributes_NADValue (" + str(x) + ") : " + str(children[x]))
        PTNodeVisitor.NAD = children[0]
        return children[0]

    def visit_Attributes_RespErr_Entry(self, node, children):
        if self.debug:        
            for x in range(len(children)):        
                print (">>> DBG visit_Attributes_NADValue (" + str(x) + ") : " + str(children[x]))
        if len(children) >= 1:
            PTNodeVisitor.response_error = children[0]
            return children[0]
        else:
            return ""

    def visit_Attributes_SupplyerID(self, node, children):
        if self.debug:        
            for x in range(len(children)):        
                print (">>> DBG visit_Attributes_SupplyerID (" + str(x) + ") : " + str(children[x]))
        PTNodeVisitor.SupplyerID = children[0]
        return children[0];

    def visit_Attributes_FunctionID(self, node, children):
        if self.debug:        
            for x in range(len(children)):        
                print (">>> DBG visit_Attributes_FunctionID (" + str(x) + ") : " + str(children[x]))
        PTNodeVisitor.FunctionID = children[0]
        return children[0]

    def visit_Attributes_VariantID(self, node, children):
        if self.debug:        
            for x in range(len(children)):        
                print (">>> DBG visit_Attributes_VariantID (" + str(x) + ") : " + str(children[x]))
        PTNodeVisitor.VariantID = children[0]
        return children[0]
        
    def visit_Attributes_MessageIDEntry(self, node, children):
        if self.debug:        
            for x in range(len(children)):        
                print (">>> DBG visit_Attributes_MessageIDEntry (" + str(x) + ") : " + str(children[x]))
        MessageIDEntry = LDF_ConfigurableFrame_Class()
        MessageIDEntry.FrameName = children[0]
        MessageIDEntry.MessageID = children[1]
        PTNodeVisitor.LDF_ConfigurableFrames.append(MessageIDEntry)
        return PTNodeVisitor.LDF_ConfigurableFrames
