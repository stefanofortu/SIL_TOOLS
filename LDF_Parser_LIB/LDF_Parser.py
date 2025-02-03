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

from LDF_Parser_LIB.LDF_Nodes_Parser import Nodes_Block, LDF_NodesVisitor_Class, LDF_Nodes_Class, NodesPrint
from LDF_Parser_LIB.LDF_Frames_Parser import Frames_Block, LDF_FramesVisitor_Class, LDF_Frame_Class, FramesPrint
from LDF_Parser_LIB.LDF_Signals_Parser import Signals_Block, LDF_SignalsVisitor_Class, LDF_Signal_Class, SignalsPrint
from LDF_Parser_LIB.LDF_Schedule_Parser import Schedule_Block, LDF_ScheduleVisitor_Class, LDF_Schedule_Class, SchedulePrint
from LDF_Parser_LIB.LDF_Encoding_Parser import Encoding_Block, LDF_EncodingVisitor_Class, LDF_Encoding_Class, EncodingPrint
from LDF_Parser_LIB.LDF_SignalsRepr_Parser import SignalRepr_Block, LDF_SignalReprVisitor_Class, LDF_SignalRepr_Class, SignalReprPrint
from LDF_Parser_LIB.LDF_Attributes_Parser import Attributes_Block, LDF_AttributesVisitor_Class, LDF_Attributes_Class, AttributesPrint, LDF_ConfigurableFrame_Class

from LDF_Parser_LIB.LDF_Encoding_Parser import LDF_Encoding_physical_Class
from LDF_Parser_LIB.LDF_Frames_Parser import LDF_FrameSignal_Class
from LDF_Parser_LIB.LDF_Schedule_Parser import LDF_ScheduleFrame_Class
#from builtins import None

def RecursiveListDelete(InList):
    if isinstance(InList,list):
        while len(InList)>0:
            if isinstance(InList[-1],list):
                RecursiveListDelete(self, InList)
            else:
                del InList[-1]

from LDF_Parser_LIB.LDF_Expressions import Expression_LIN_Speed, LDF_ExpressionVisitor_Class

# Dump Structure
import pickle # To store Class Instance to a file
import json # To store Class Instance to a file

# Grammar
def LDF_file_Grammar():       return ZeroOrMore(LDF_Block), EOF
def LDF_Block():   
    return [ 
        Frames_Block, 
        Nodes_Block,
        Signals_Block,
        Schedule_Block,
        Encoding_Block,
        SignalRepr_Block,
        Attributes_Block,
        Expression_LIN_Speed,
        GenericEntryWtihException ]
def _LDF_Block():   # Use this schema instead of LDF_Block to debug new Expressions
    return [ Expression_LIN_Speed, GenericEntry ]
def GenericEntryWtihException():
    return [SintaxException1, GenericEntry]
def GenericEntry():     return [GenericBlock, GenericExpression ]
def GenericBlock():     return BlockName, Optional(":",GenericBlockParams), "{", OneOrMore(GenericEntry), "}"
#def GenericExpression():      return GenericExpressionName, Optional([":","="], GenericExpressionValue), ";"
def GenericExpression():      return GenericExpressionName, Optional( GenericExpressionValue ), ";"
def GenericExpressionName():   return symbol()
def GenericExpressionValue():   return _(r'([^;\n])+')

# Sintax Exception must be put before Generic
# WARNING:
# The following sintax violates the "GenericEntry schema" and must be checked before GenericEntry  
def SintaxException1():  return  Generic_symbol, "{", Generic_symbol,",", Generic_int_number, "}", "delay", Generic_int_number, "ms", ";"

def BlockName():        return symbol()
def GenericBlockParams(): return GenericBlockParam, ZeroOrMore(",",GenericBlockParam)
def GenericBlockParam(): return [Generic_symbol,Generic_int_number,Generic_float_number]

def symbol():   return _(r"\w+")
def Generic_number():   return _(r'\d*\.\d*|\d+')

def Generic_symbol():       return _(r"\w+")
def Generic_float_number(): return _(r'\d*\.\d*|\d+')
def Generic_int_number():   return [Generic_hex_number, Generic_dec_number]
def Generic_dec_number():   return _(r'\d+')
def Generic_hex_number():   return _(r'0x[0-9A-Fa-f]+')

# Lexer Comments
def comment():          return [_(r'//.*'), mlinecomment] # C comments style
#def mlinecomment():     return _("/\*.*\*/")
#def mlinecomment():     return _(r'/\*([^*]|\*+[^/])*\*+/')
def mlinecomment():     return _(r'/\*(.|\n)*?\*/')

####################################
####################################

###
# LDF File encoding
###
def get_encoding(s, encodings=('utf8','ISO-8859-2', 'latin1', 'ascii')):
    for encoding in encodings:
        try:
            s.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            pass
    return 'Unknown'

'''
def check_encoding(FileName, encoding='utf-8'):
    FH = open(FileName,"rb")
    FileEncoding = get_encoding(FH.read())
    FH.close()
    #print("Encoding = " + Encoding)
    return (FileEncoding == encoding)
'''
    
###
# LDF RunTime Values  Class/functions (_FrameValues)
###
    
def LDF_FrameValue_Str2List(FrameValStr):
    Value64bit = int(FrameValStr,16)
    FrameLEN = int(len(FrameValStr)/2)
    FrameBYTES = Value64bit.to_bytes(FrameLEN, byteorder='little')
    FrameValList = [int(o) for o in FrameBYTES]
    return FrameValList

def LDF_FrameValue_List2Str(FrameValList):
    Value64bit = 0
    for x in range(len(FrameValList)):
        Value64bit += FrameValList[x]*(2**(8*x))
    FrameValStr =  ("%%0%dX" % (len(FrameValList)*2) ) % ( Value64bit )
    return FrameValStr

class FramesValue_Class():
    def __init__(self):
        self.FrameName = ""
        self.InitValue = Value_Class()
        self.ActualValue = Value_Class()

class Value_Class():
    def __init__(self, actualval=""):
        self._Value = actualval
        
    def get_List(self):
        return LDF_FrameValue_Str2List(self._Value)

    def get_int(self):
        return int(self._Value,16)
    
    def get_str(self):
        return self._Value
     
    def set_val(self,indata):
        if isinstance(indata, str):
            self._Value = indata
        elif isinstance(indata, int):
            self._Value =  ("%%0%dX" % (len(self._Value)) ) % ( indata ) # Integer Can't force data len 
        elif isinstance(indata, list):
            self._Value = LDF_FrameValue_List2Str(indata)
        else:
            return
            
        
class LDF_Struct_Class():
    def __init__(self):
        self.LDF_Nodes = LDF_Nodes_Class()
        self.LDF_Frames = []      
        self.LDF_Signals = []
        self.LDF_Encodings = []
        self.LDF_Schedules = []
        self.LDF_SignalReprs = []
        self.LDF_Attributes = []
        
        ###
        # TODO Retrieve it parsing LDF 
        self.LDF_Diagnostic_frames =[]
        
        Frm = LDF_Frame_Class()
        Frm.ID = 0x3C
        Frm.Name = "MasterReq"
        #Frm.Node = "" # Empty Because of Diag Frame
        #Frm.FrameSignals = [] # Leave temporarily empty 
        self.LDF_Diagnostic_frames.append(Frm)

        Frm = LDF_Frame_Class()
        Frm.ID = 0x3D
        Frm.Name = "SlaveResp"
        #Frm.Node = "" # Empty Because of Diag Frame
        #Frm.FrameSignals = [] # Leave temporarily empty 
        self.LDF_Diagnostic_frames.append(Frm)
        ###

        ###
        self.LIN_Speed = 0
        self._FrameValues=[]

    ###
    # LDF RunTime Values  Methods (_FrameValues)
    ###
        
    def InitFrameValues(self):
        '''
        LDF Initialize _FrameValues to store Frames Actual Values (during Scheduler)
        '''
        for Frm in self.LDF_Frames:
            Frame = LDF_Frame_Class() #redundant
            Frame = Frm;
        
            FrameSignals = [o.Signal for o in Frame.FrameSignals]

            FrameValue = FramesValue_Class()
            FrameValue.FrameName = Frame.Name
            (FrameValue.InitValue).set_val(0xFF)
            (FrameValue.ActualValue).set_val(0xFF)
            self._FrameValues.append(FrameValue)
            
            for SignalName in FrameSignals:
                ActSignal = LDF_Signal_Class()
                ActSignal = self.getSignal(SignalName)
                self.UpdateSignalValue(SignalName,ActSignal.InitVal)
        
        #Add Master Request/ Master Response
        ###################
        FrameValue = FramesValue_Class()
        FrameValue.FrameName = "MasterReq"
        (FrameValue.InitValue).set_val(0xFF)
        (FrameValue.ActualValue).set_val(0xFF)
        self._FrameValues.append(FrameValue)       

        FrameValue = FramesValue_Class()
        FrameValue.FrameName = "MasterResp"
        (FrameValue.InitValue).set_val(0xFF)
        (FrameValue.ActualValue).set_val(0xFF)
        self._FrameValues.append(FrameValue)
        ###################      

    def UpdateSignalValue(self, InSignalName, InValue):
        if not ( isinstance(InValue, int) or isinstance(InValue, float) or isinstance(InValue, str)): return None
        # Load Encoder
        Encoder = LDF_Encoding_Class()
        Encoder = self.getSignalEncoder(InSignalName)
        if Encoder== None: return None 
        EncodedValue = Encoder.ConvertToLinValue(InValue)
        
        return self.UpdateSignalValueEncoded(InSignalName, EncodedValue)            
                       
    def UpdateSignalValueEncoded(self, InSignalName, Value):
        if not isinstance(Value, int): return None
        
        Frm = self.getSignalFrame(InSignalName)
        ActualValue = (self.getFrameValue(Frm.Name)).ActualValue if Frm!= None else None
        if ActualValue == None: return None
        ActualValueInt = ActualValue.get_int()
          
        (SignalMask, FrameMask) = self.getSignalBitMask(InSignalName)
        if (SignalMask, FrameMask) == (None, None): return None
        (SignalBitOffset, FrameLEN) = self.getSignalBitOffset(InSignalName)
        if (SignalBitOffset, FrameLEN) == (None, None): return None

        ActualValueInt &= FrameMask
        ActualValueInt |= ((Value << SignalBitOffset) & SignalMask)
            
        self.UpdateFrameValue(Frm.Name, ActualValueInt)
        return Frm
                
    def UpdateFrameValue(self, InFrame, data):
        if isinstance(InFrame, str):
            FrameName = InFrame
        elif isinstance(InFrame, int):
            FrameID = InFrame
            # Search to frame-name from Frame ID
            FrameName = "" # TODO Non yet implemented
        #Frame = self.getFrame(FrameName)
        FramesValue = self.getFrameValue(FrameName)
        (FramesValue.ActualValue).set_val(data)

    def ResetFrameValues(self, Value=0x00):
        # the example allows to communicate with a PLIN-SLAVE
        res = True

        for x in range(len(self.LDF_Frames)):
            Frame = LDF_Frame_Class()
            Frame = self.LDF_Frames[x]
            
            if (self.isFramePublisher(Frame)):
                data =  [Value] * Frame.LEN
                self.UpdateFrameValue(Frame.Name, data)
                print("Buffered Frame (" + Frame.Name + ")=" + ((self.getFrameValue(Frame.Name)).ActualValue).get_str() ) #debug only
        
        return res

    def getFrameValue(self, InFrame):
        if isinstance(InFrame, str):
            FrameName = InFrame
        elif isinstance(InFrame, int):
            FrameID = InFrame
            # Search to frame-name from Frame ID
            Frm = self.getFrame(FrameID)
            FrameName = (self.getFrame(FrameID)).Name # TODO Non yet implemented
        
        FramesValue = FramesValue_Class()
        FramesValueNameList = [o.FrameName for o in self._FrameValues]
        if FrameName in FramesValueNameList:
            FramesValue = self._FrameValues[FramesValueNameList.index(FrameName)]
            return FramesValue
        else:
            return None #return empty frame Value

    ###
    # Structure CrossReference Methods
    ###
             
    #####################################         
    #####################################         
    def getSignal(self, SignalName):
        '''
        PUT Description Here
        '''  
        Signal = LDF_Signal_Class()
        SignalNameList = [o.Name for o in self.LDF_Signals]
        if SignalName in SignalNameList:
            Signal = self.LDF_Signals[SignalNameList.index(SignalName)]
            return Signal
        else:
            return None
        
    def getFrame(self, FrameDesc):
        '''
        PUT Description Here
        '''
        Frame = LDF_Frame_Class()
        if isinstance(FrameDesc, str):
            FrameName = FrameDesc
            FrameNameList = [o.Name for o in self.LDF_Frames]
            DiagFrameNameList = [o.Name for o in self.LDF_Diagnostic_frames]
            if FrameName in FrameNameList:
                Frame = self.LDF_Frames[FrameNameList.index(FrameName)]
                return Frame
            elif FrameName in DiagFrameNameList:
                Frame = self.LDF_Diagnostic_frames[DiagFrameNameList.index(FrameName)]
                return Frame                
            else:
                return None
            
        elif isinstance(FrameDesc, int):
            FrameID = FrameDesc
            FrameIDList = [o.ID for o in self.LDF_Frames]
            DiagFrameIDList = [o.ID for o in self.LDF_Diagnostic_frames]
            if FrameID in FrameIDList:
                Frame = self.LDF_Frames[FrameIDList.index(FrameID)]
                return Frame
            elif FrameID in DiagFrameIDList:
                Frame = self.LDF_Diagnostic_frames[DiagFrameIDList.index(FrameID)]
                return Frame                
            else:
                return None
        else:
            return None
    
    #####################################         
    #####################################         

    def Frame_Name2ID(self, FrameName):
        '''
        PUT Description Here
        '''
        if not isinstance(FrameName, str):
            return None
        Frame = LDF_Frame_Class()
        Frame = self.getFrame(FrameName)
        if Frame == None:
            return None
        else:
            return Frame.ID
   
    def Frame_ID2Name(self, FrameID):
        '''
        PUT Description Here
        '''    
        if not isinstance(FrameID, int):
            return None
        Frame = LDF_Frame_Class()
        Frame = self.getFrame(FrameID)
        if Frame == None:
            return None
        else:
            return Frame.Name

    def isSignalPublisher(self, Signalin):
        '''
        PUT Description Here
        '''     
        if isinstance(Signalin, str):        
            Signal = LDF_Signal_Class()
            Signal = self.getSignal(Signalin) #retrieve it from Signal name
            if Signal == None: # Signal name not found 
                return False
            else:
                if Signal.Publisher == self.LDF_Nodes.Master:
                    return True
                else:
                    return False                
        elif isinstance(Signalin, LDF_Signal_Class): 
            Signal = Signalin
            if Signal.Publisher == self.LDF_Nodes.Master:
                return True
            else:
                return False                
        else:    
            return False

    def isSignalSubscriber(self, Signalin):
        '''
        PUT Description Here
        '''  
        if isinstance(Signalin, str):        
            Signal = LDF_Signal_Class()
            Signal = self.getSignal(Signalin) #retrieve it from Signal name
            if Signal == None: # Signal name not found 
                return False
            else:
                if Signal.Publisher != self.LDF_Nodes.Master:
                    return True
                else:
                    return False                
        elif isinstance(Signalin, LDF_Signal_Class): 
            Signal = Signalin
            if Signal.Publisher != self.LDF_Nodes.Master:
                return True
            else:
                return False                
        else:    
            return False
            
    def isFramePublisher(self, FrameIn):
        '''
        PUT Description Here
        '''    
        if isinstance(FrameIn, str):        
            Frame = LDF_Frame_Class()
            Frame = self.getFrame(FrameIn) #retrieve from Frame name
        elif isinstance(FrameIn, LDF_Frame_Class):
            Frame = FrameIn
        else:
            Frame = None
            
        if Frame == None:
            return False
        else:
            if Frame.Node == self.LDF_Nodes.Master:
                return True
            else:
                return False
    
    def getSignalFrame(self, SignalName):
        '''
        PUT Description Here
        '''    
        for Frm in self.LDF_Frames:
            Frame = LDF_Frame_Class()
            Frame = Frm
            Sig = LDF_FrameSignal_Class # redundant code
            FrameSignalsNames = [Sig.Signal for Sig in Frame.FrameSignals]
            if SignalName in FrameSignalsNames:
                return Frame
        return None 
    
    def getSignalEncoderName(self, SignalName):
        '''
        PUT Description Here
        '''    
        EncoderNameLUT=[]
        SignalNameLUT=[]

        for Rep in self.LDF_SignalReprs:
            Reprs = LDF_SignalRepr_Class()
            Reprs = Rep
            #FrameNameList.append(Frame.Name)
            EncoderNameList = [Reprs.Encoder for o in Reprs.EncodedSignals]
            SignalsNameList = [o for o in Reprs.EncodedSignals]

            EncoderNameLUT.extend(EncoderNameList)
            SignalNameLUT.extend(SignalsNameList)
            
        if SignalName in SignalNameLUT:
            EncoderName = EncoderNameLUT[SignalNameLUT.index(SignalName)]
            return (EncoderName)
        else:
            return "Undefined"
    
    def getSignalEncoder(self, SignalName):
        '''
        PUT Description Here
        '''    
        EncoderName = self.getSignalEncoderName(SignalName)
        
        Encoder = LDF_Encoding_Class()
        if EncoderName == "Undefined":
            Encoder.Encoder = "Default"
            Encoder.LogicalValues = []
            phy_val = LDF_Encoding_physical_Class()
            phy_val.MaxValue = (2 ** (self.getSignal(SignalName)).BitLen)-1
            Encoder.PhysicalValues.append(phy_val)
            return Encoder
        else:
            EncoderNameList = [o.Encoder for o in self.LDF_Encodings]
            if EncoderName in EncoderNameList:
                Encoder = self.LDF_Encodings[EncoderNameList.index(EncoderName)]
                return Encoder
            else:
                return None
        
    def getSignalBitOffset(self, SignalName):
        '''
        PUT Description Here
        '''    
        #FrameNameList = [o.Name for o in self.LDF_Frames]
        FrameLENLUT=[]
        SignalNameLUT=[]
        SignalBitOffsetLUT=[]
        #FrameNameList=[]
        for Frm in self.LDF_Frames:
            Frame = LDF_Frame_Class()
            Frame = Frm
            #FrameNameList.append(Frame.Name)
            FrameFrameLENList = [Frame.LEN for o in Frame.FrameSignals]
            FrameSignalNameList = [o.Signal for o in Frame.FrameSignals]
            FrameSignalOffsetList = [o.BitOffset for o in Frame.FrameSignals]
            SignalNameLUT.extend(FrameSignalNameList)
            SignalBitOffsetLUT.extend(FrameSignalOffsetList)
            FrameLENLUT.extend(FrameFrameLENList)
            
        if SignalName in SignalNameLUT:
            SignalBitOffset = SignalBitOffsetLUT[SignalNameLUT.index(SignalName)]
            FrameLEN = FrameLENLUT[SignalNameLUT.index(SignalName)]
            return (SignalBitOffset, FrameLEN)
        else:
            return (None, None)
    
    def getSignalBitMask(self, SignalName):
        '''
        PUT Description Here
        '''    
        Signal = LDF_Signal_Class()
        Signal = self.getSignal(SignalName)
        (BitOffset, FrameLEN) = self.getSignalBitOffset(SignalName)
        
        UnsignedBIT = math.log2(sys.maxsize * 2 + 2)
        if UnsignedBIT < 64:
            raise("MAX UNSIGNED BIT %d must be >= 64" % UnsignedBIT )
        if BitOffset == None:
            return (None, None)
        
        SignalMask = (((2**(Signal.BitLen))-1) << BitOffset)
        FrameMask = ((2**(8*FrameLEN))-1) ^ SignalMask
        return (SignalMask, FrameMask)

    ###
    # Structure Get general Information
    ###
    def GetSignalNameList(self,type="Both"):
        '''
        PUT Description Here
        '''    
        Signal_LUT=[]
        for x in range(len(self.LDF_Signals)):
            sig = LDF_Signal_Class()
            sig = self.LDF_Signals[x]
            
            if type=="Pub": 
                if ( self.isSignalPublisher(sig) ): # Check if Publisher and in Selected Schedule 
                    Signal_LUT.append(sig.Name)
            elif type=="Sub":
                if ( self.isSignalSubscriber(sig) ): # Check if Publisher and in Selected Schedule 
                    Signal_LUT.append(sig.Name)                 
            else: #Both
                Signal_LUT.append(sig.Name)
        
        return Signal_LUT

    def GetFrameNameList(self,type="Both"):
        '''
        PUT Description Here
        '''    
        Frame_LUT=[]
        for x in range(len(self.LDF_Frames)):
            Frm = LDF_Frame_Class()
            Frm = self.LDF_Frames[x]
            
            if type=="Pub": 
                if ( self.isFramePublisher(Frm) ): # Check if Publisher and in Selected Schedule 
                    Frame_LUT.append(Frm.Name)
            elif type=="Sub":
                if ( self.isSignalSubscriber(Frm) ): # Check if Publisher and in Selected Schedule 
                    Frame_LUT.append(Frm.Name)                 
            else: #Both
                Frame_LUT.append(Frm.Name)
                        
        return Frame_LUT

    def GetFrameList(self,type="Both"):
        '''
        PUT Description Here
        '''    
        Frame_LUT=[]
        for x in range(len(self.LDF_Frames)):
            Frm = LDF_Frame_Class()
            Frm = self.LDF_Frames[x]
            
            if type=="Pub": 
                if ( self.isFramePublisher(Frm) ): # Check if Publisher and in Selected Schedule 
                    Frame_LUT.append(Frm)
            elif type=="Sub":
                if ( self.isSignalSubscriber(Frm) ): # Check if Publisher and in Selected Schedule 
                    Frame_LUT.append(Frm)                 
            else: #Both
                Frame_LUT.append(Frm)
                        
        return Frame_LUT

    def GetScheduleNameList(self):
        '''
        PUT Description Here
        '''    
        Schedule_LUT=[]
        for x in range(len(self.LDF_Schedules)):
            Sch = LDF_Schedule_Class()
            Sch = self.LDF_Schedules[x]
            Schedule_LUT.append(Sch.Name)
                        
        return Schedule_LUT
    
    ###
    ### Apply Filer on LDF_Struct
    ###
    def Filter_by_Scheduler(self,SchedulerSelection=-1):
        
        if SchedulerSelection < 0:
            return
        #----------------------------------------------------
        # UPDATE LDF_Schedules [LDF_Schedule_Class()]
        self.LDF_Schedules[:] = [self.LDF_Schedules[SchedulerSelection]]
        
        #----------------------------------------------------
        # UPDATE Frames [LDF_Frame_Class()]
        FrameNameList =  [o.Frame for o in (self.LDF_Schedules[0]).ScheduleFrames]
        #print(FrameNameList)
        
        self.LDF_Frames[:] =(val 
                                for val in self.LDF_Frames
                                if (val.Name in FrameNameList)
                            )
        #----------------------------------------------------

        #----------------------------------------------------
        # UPDATE Nodes [LDF_Nodes_Class()]
        #self.LDF_Nodes.Master = self.LDF_Nodes.Master
        NodeNameList = [o.Node for o in self.LDF_Frames]
        NodeNameList = list( dict.fromkeys(NodeNameList) ) # Remove duplicates 
        #print(NodeNameList)
        
        self.LDF_Nodes.Slaves[:] = (val 
                                        for val in NodeNameList
                                        if (val != self.LDF_Nodes.Master)
                                    )
        
        #----------------------------------------------------

        #----------------------------------------------------
        # UPDATE Signals [LDF_Signal_Class()]
        SigNameList =[]
        for FR in self.LDF_Frames:
            SigNameList.extend([val.Signal for val in FR.FrameSignals])
        #print(SigNameList)
        
        self.LDF_Signals[:] = (val 
                                for val in self.LDF_Signals 
                                if (val.Name in SigNameList)
                                )
        #----------------------------------------------------
        
        #----------------------------------------------------
        # DBG Signals Representation [LDF_SignalRepr_Class()]
        self.LDF_SignalReprs[:] = (val 
                                    for val in self.LDF_SignalReprs 
                                    if len(set(val.EncodedSignals).intersection(SigNameList))>0
                                    )
        # Clean Ups from other signals
        # TODO 
        #----------------------------------------------------

        SigEncoderList =  [o.Encoder for o in self.LDF_SignalReprs]

        #----------------------------------------------------
        # UPDATE Encodings [LDF_Encoding_Class()]
        self.LDF_Encodings[:] = (val 
                                             for val in self.LDF_Encodings 
                                             if ( (val.Encoder in SigEncoderList) or (val.Encoder in SigNameList))
                                             )
        #----------------------------------------------------

        #----------------------------------------------------
        # UPDATE Attributes [LDF_Attributes_Class()]
        self.LDF_Attributes[:] = (val 
                                    for val in self.LDF_Attributes 
                                    if (val.NodeName in NodeNameList)
                                )
        #----------------------------------------------------
                                             
        #----------------------------------------------------        

    def Filter_by_Node(self,SlaveNodeName):
        
        MasterNodeName = self.LDF_Nodes.Master
        
        #----------------------------------------------------
        # UPDATE Nodes
        self.LDF_Nodes.Slaves[:] = [SlaveNodeName]
        #----------------------------------------------------
    
        #----------------------------------------------------
        # UPDATE Attributes
        # x[:] = (val for val in x if val != 2)
        # slice assignment x[:] take care of removing old elements
        self.LDF_Attributes[:] = (val 
                                             for val in self.LDF_Attributes 
                                             if (val.NodeName == SlaveNodeName)
                                             )
        #----------------------------------------------------

        #----------------------------------------------------
        # UPDATE Signals
        self.LDF_Signals[:] = (val 
                                             for val in self.LDF_Signals 
                                             if (
                                                 (val.Publisher == SlaveNodeName) or
                                                 ( (val.Publisher == MasterNodeName) and (SlaveNodeName in val.Subscribers)) 
                                                 )
                                             )
        #----------------------------------------------------
        
        SigNameList =       [o.Name for o in self.LDF_Signals]

        #----------------------------------------------------
        # DBG Signals print
        self.LDF_SignalReprs[:] = (val 
                                             for val in self.LDF_SignalReprs 
                                             if len(set(val.EncodedSignals).intersection(SigNameList))>0
                                             )
        #----------------------------------------------------
                
        SigEncoderList =  [o.Encoder for o in self.LDF_SignalReprs]
        
        #----------------------------------------------------
        # UPDATE Encodings
        self.LDF_Encodings[:] = (val 
                                             for val in self.LDF_Encodings 
                                             if ( (val.Encoder in SigEncoderList) or (val.Encoder in SigNameList))
                                             )
        #----------------------------------------------------
        
        #----------------------------------------------------
        # UPDATE Frames
        self.LDF_Frames[:] = (val 
                                             for val in self.LDF_Frames 
                                             if (
                                                 (val.Node == SlaveNodeName) or
                                                 len(set([o.Signal for o in val.FrameSignals]).intersection(SigNameList))>0
                                                )
                                             )
        #----------------------------------------------------

        FrameNameList =  [o.Name for o in self.LDF_Frames] 
      
        #----------------------------------------------------
        # UPDATE LDF_Schedules
        self.LDF_Schedules[:] = (val 
                                             for val in self.LDF_Schedules 
                                             if len(set([o.Frame for o in val.ScheduleFrames]).intersection(FrameNameList))>0
                                             )
        #----------------------------------------------------
        
        #----------------------------------------------------
        # Clean up schedulers
        #--------------------------
        for Schedule in self.LDF_Schedules:
            FilteredScheduleSignals=[]
            extra_delay = 0
            for (Sig, Delay) in [(o.Frame, o.Delay) for o in Schedule.ScheduleFrames]:
                if Sig in FrameNameList:
                    FilteredScheduleSignals.append(LDF_ScheduleFrame_Class(Sig,Delay + extra_delay))
                    extra_delay = 0
                else:
                    extra_delay += Delay
            if extra_delay>0:
                FilteredScheduleSignals[-1].Delay += extra_delay
            
            Schedule.ScheduleFrames = FilteredScheduleSignals
        #--------------------------      
        return self
  
    ###
    # Methods to store Structure in Files
    ###
    def dump_object(self, FileName):
        ####
        ####  Store and Retrieve From Binary (piclke ) 
        ####
        FileHandler = open(FileName,"wb")
        pickle.dump(self, FileHandler) # Protocol 0 is for human readable
        FileHandler.close()
    
    def load_object(self, FileName):
        ####
        #### To Check ???
        ####
        FileHandler = open(FileName,"rb")
        Tmp_Struct = self.__init__()
        Tmp_Struct = pickle.load(FileHandler)
        FileHandler.close()
        #self.LDF_Attributes = Tmp_Struct.LDF_Attributes
        self.LDF_Nodes = Tmp_Struct.LDF_Nodes
        self.LDF_Frames = Tmp_Struct.LDF_Frames    
        self.LDF_Signals = Tmp_Struct.LDF_Signals
        self.LDF_Encodings = Tmp_Struct.LDF_Encodings
        self.LDF_Schedules = Tmp_Struct.LDF_Schedules
        self.LDF_SignalReprs = Tmp_Struct.LDF_SignalReprs
        self.LDF_Attributes = Tmp_Struct.LDF_Attributes
    
    def dump_json(self, FileName=None):
        ####  Store human readable json format (json ) 
        ####
        res = json.dumps(
            self, 
            default=lambda o: o.__dict__, 
            sort_keys=True, indent=4, ensure_ascii=False)
        try:
            with open(FileName,"w") as FileHandler:
                FileHandler.write(res)
        except:
            print("Warning: json dump fails")
        return res
        
class LDF_Parser_Class():
    def __init__(self, inputfile="",Encoding="utf_8", DEBUG=False):
        if isinstance(inputfile, str):
            self.LDF_FH = None
            self.LDF_Filename  = inputfile
        else:
            self.LDF_FH = inputfile
            self.LDF_Filename = None
        self.LDF_Encoding  = Encoding
        self.LDF_Struct = LDF_Struct_Class()
        self.LDF_ParseTree = []
        self.LDF_parser = ParserPython(LDF_file_Grammar, comment, debug=DEBUG)
        self.myNodesVisitor = LDF_NodesVisitor_Class(debug=DEBUG)
        self.myFramesVisitor = LDF_FramesVisitor_Class(debug=DEBUG)
        self.mySignalsVisitor = LDF_SignalsVisitor_Class(debug=DEBUG)
        self.myScheduleVisitor = LDF_ScheduleVisitor_Class(debug=DEBUG)
        self.myEncodingVisitor = LDF_EncodingVisitor_Class(debug=DEBUG)
        self.mySignalReprVisitor = LDF_SignalReprVisitor_Class(debug=DEBUG)
        self.myAttributesVisitor = LDF_AttributesVisitor_Class(debug=DEBUG)
        ##
        self.myExpressionVisitor = LDF_ExpressionVisitor_Class(debug=DEBUG)
    
    def check_encoding(self):
        FH = open(self.LDF_Filename,"rb")
        FileEncoding = get_encoding(FH.read())
        FH.close()
        print("LDF Input file Encoding = " + FileEncoding)
        return (FileEncoding == self.LDF_Encoding)        

    def get_encoding(self):
        FH = open(self.LDF_Filename,"rb")
        FileEncoding = get_encoding(FH.read())
        FH.close()
        print("LDF Input file Encoding = " + FileEncoding)
        return (FileEncoding)        
        
    def LDFparse(self, DEBUG=False):
        dbg_print = False 
        
        # Check for Encoding
        #if( not self.check_encoding()):
        #    raise("File Encoding doesn't match (" + self.LDF_Filename +"," + self.LDF_Encoding+")")
        
        # Check for Encoding and automatically switch to the proper encoder
        if self.LDF_FH == None:
            Actual_Encoding = self.get_encoding()
            if not Actual_Encoding == self.LDF_Encoding:
                print("WARNING: LDF encoding is '%s' instead of '%s'" % (Actual_Encoding, self.LDF_Encoding))
                self.LDF_Encoding = Actual_Encoding
            
            LDF_file = open(
                    self.LDF_Filename,"r", encoding=self.LDF_Encoding
                    ).read()
        else:
            LDF_file = self.LDF_FH.read()
        # Parser instantiation. LDF_Block is the definition of the root rule
        # and comment is a grammar rule for comments.
            
        del self.LDF_ParseTree
        self.LDF_ParseTree = self.LDF_parser.parse(LDF_file)
        
        ###
        ### Populate LDF_Struct
        ###
        
        #------------------------------------------------
        RecursiveListDelete(self.myNodesVisitor.LDF_Nodes.Slaves)
        ast = visit_parse_tree(self.LDF_ParseTree, self.myNodesVisitor)
        self.LDF_Struct.LDF_Nodes = self.myNodesVisitor.LDF_Nodes
        if dbg_print:
            print("---\nNODES:\n---") 
            NodesPrint(self.LDF_Struct.LDF_Nodes)
        #------------------------------------------------
    
        #------------------------------------------------
        RecursiveListDelete(self.myNodesVisitor.LDF_Frames)
        ast = visit_parse_tree(self.LDF_ParseTree, self.myFramesVisitor)
        self.LDF_Struct.LDF_Frames = self.myNodesVisitor.LDF_Frames
        if dbg_print:        
            print("---\nFRAMES:\n---") 
            FramesPrint(self.LDF_Struct.LDF_Frames)
        #------------------------------------------------

        #------------------------------------------------
        RecursiveListDelete(self.mySignalsVisitor.LDF_Signals)
        ast = visit_parse_tree(self.LDF_ParseTree, self.mySignalsVisitor)
        self.LDF_Struct.LDF_Signals = self.mySignalsVisitor.LDF_Signals
        if dbg_print:
            print("---\nSIGNALS:\n---") 
            SignalsPrint(self.LDF_Struct.LDF_Signals)
        #------------------------------------------------

        #------------------------------------------------
        RecursiveListDelete(self.myScheduleVisitor.LDF_Schedules)
        ast = visit_parse_tree(self.LDF_ParseTree, self.myScheduleVisitor)
        self.LDF_Struct.LDF_Schedules = self.myScheduleVisitor.LDF_Schedules
        if dbg_print:
            print("---\nSCHEDULES:\n---") 
            SchedulePrint(self.LDF_Struct.LDF_Schedules)
        #------------------------------------------------

        #------------------------------------------------
        RecursiveListDelete(self.myEncodingVisitor.LDF_Encodings)
        ast = visit_parse_tree(self.LDF_ParseTree, self.myEncodingVisitor)
        self.LDF_Struct.LDF_Encodings = self.myEncodingVisitor.LDF_Encodings
        if dbg_print:        
            print("---\nENCODING:\n---") 
            EncodingPrint(self.LDF_Struct.LDF_Encodings)
        #------------------------------------------------

        
        #------------------------------------------------
        RecursiveListDelete(self.mySignalReprVisitor.LDF_SignalReprs)
        ast = visit_parse_tree(self.LDF_ParseTree, self.mySignalReprVisitor)
        self.LDF_Struct.LDF_SignalReprs = self.mySignalReprVisitor.LDF_SignalReprs
        if dbg_print:
            print("---\nSIGNALS Representation:\n---") 
            SignalReprPrint(self.LDF_Struct.LDF_SignalReprs)
        #------------------------------------------------

        #------------------------------------------------
        RecursiveListDelete(self.myAttributesVisitor.LDF_Attributes)
        ast = visit_parse_tree(self.LDF_ParseTree, self.myAttributesVisitor)
        self.LDF_Struct.LDF_Attributes = self.myAttributesVisitor.LDF_Attributes
        if dbg_print:
            print("---\nATTRIBUTES:\n---") 
            AttributesPrint(self.LDF_Struct.LDF_Attributes)
        #------------------------------------------------

        #------------------------------------------------
        RecursiveListDelete(self.myExpressionVisitor.LDF_Speed_kbps)
        ast = visit_parse_tree(self.LDF_ParseTree, self.myExpressionVisitor)
        self.LDF_Struct.LIN_Speed = int(self.myExpressionVisitor.LDF_Speed_kbps * 1000);
        #------------------------------------------------