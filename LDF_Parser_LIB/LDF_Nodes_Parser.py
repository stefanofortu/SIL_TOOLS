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
#def simpleLanguage():   return Nodes_Block
def Nodes_Block():      return Kwd("Nodes"), "{", Nodes_Master, Optional(Nodes_Slaves), "}"
def Nodes_Master():     return Kwd("Master"), ":", Nodes_MasterName, ZeroOrMore(",", Nodes_GenericExpression), ";"
def Nodes_Slaves():     return Kwd("Slaves"), ":", Nodes_SlaveName, ZeroOrMore(",", Nodes_SlaveName), ";"
def Nodes_MasterName(): return Nodes_symbol
def Nodes_SlaveName():  return Nodes_symbol

def Nodes_GenericExpression(): return _(r'([^,;\n])+')
def Nodes_symbol():            return _(r"\w+")

# Lexer Comments
#def comment():          return [_("//.*"), _("/\*.*\*/")] # C comments style

def NodesPrint(my_nodes):
    print("Master: "+str(my_nodes.Master))
    print("Slaves: "+str(my_nodes.Slaves))

class LDF_Nodes_Class:
    def __init__(self):
        self.Master =""
        self.Slaves =[]
    
class LDF_NodesVisitor_Class(PTNodeVisitor):
    PTNodeVisitor.LDF_Nodes = LDF_Nodes_Class()
    #PTNodeVisitor.LDF_Nodes = Nodes_Class()
    
    def visit_Nodes_SlaveName(self, node, children):
        if self.debug:
            print ("DBG Slave name : " + node.value)
        PTNodeVisitor.LDF_Nodes.Slaves.append(node.value)
        return node.value
    
    def visit_Nodes_MasterName(self, node, children):
        if self.debug:        
            print ("DBG Master name : " + node.value)
        PTNodeVisitor.LDF_Nodes.Master = node.value
        return node.value

