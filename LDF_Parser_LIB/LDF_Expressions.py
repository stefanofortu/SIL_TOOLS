'''
Created on 16-dic-2020

@author: andrea.pasotti
'''
from __future__ import unicode_literals

from arpeggio import *
from arpeggio import RegExMatch as _

# Grammar
def Expression_LIN_Speed():     return Kwd("LIN_speed"), "=", Expression_LIN_Speed_kbps, ";"
def Expression_LIN_Speed_kbps():     return Expression_float_number , Kwd("kbps")

def Expression_float_number():   return _(r'\d*\.\d*|\d+')

class LDF_ExpressionVisitor_Class(PTNodeVisitor):
    PTNodeVisitor.LDF_Speed_kbps = 0
    
    def visit_Expression_float_number(self, node, children):
        if self.debug:
            print (">>> DBG FLOAT_NUMBER : " + node.value)
        return float(node.value)

    def visit_Expression_LIN_Speed_kbps(self, node, children):
        if self.debug:
            for x in range(len(children)):        
                print (">>> DBG Expression_LIN_Speed_kbps (" + str(x) + ") : " + str(children[x]))
        PTNodeVisitor.LDF_Speed_kbps = children[0]

        return PTNodeVisitor.LDF_Speed_kbps   
