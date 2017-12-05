#    <OUTPUTFILENAME>
#    Created <DATE> from:
#        Messages = <INPUTFILENAME>
#        Template = <TEMPLATEFILENAME>
#        Language = <LANGUAGEFILENAME>
#
#                     AUTOGENERATED FILE, DO NOT EDIT
import struct
import ctypes
from collections import OrderedDict
from msgtools.lib.messaging import *
import msgtools.lib.messaging as msg

class <MSGNAME> :
    ID = <MSGID>
    SIZE = <MSGSIZE>
    MSG_OFFSET = Messaging.hdrSize
    # Enumerations
    <ENUMERATIONS>
    
    #@staticmethod
    #def Create():
    #    message_buffer = ctypes.create_string_buffer(<MSGNAME>.MSG_OFFSET + <MSGNAME>.SIZE)
    #
    #    Messaging.hdr.SetMessageID(message_buffer, <MSGNAME>.ID)
    #    Messaging.hdr.SetDataLength(message_buffer, <MSGNAME>.SIZE)
    #
    #    <INIT_CODE>
    #    return message_buffer

    def __init__(self, messageBuffer=None):
        doInit = 0
        if messageBuffer == None:
            doInit = 1
            messageBuffer = ctypes.create_string_buffer(<MSGNAME>.MSG_OFFSET + <MSGNAME>.SIZE)
        else:
            try:
                messageBuffer.raw
            except AttributeError:
                newbuf = ctypes.create_string_buffer(len(messageBuffer))
                for i in range(0, len(messageBuffer)):
                    newbuf[i] = messageBuffer[i]
                messageBuffer = newbuf
        # this is a trick to get us to store a copy of a pointer to a buffer, rather than making a copy of the buffer
        self.msg_buffer_wrapper = { "msg_buffer": messageBuffer }

        self.hdr = Messaging.hdr(messageBuffer)
        if doInit:
            self.hdr.SetMessageID(<MSGNAME>.ID)
            self.hdr.SetDataLength(<MSGNAME>.SIZE)
        
            <INIT_CODE>

    def rawBuffer(self):
        # this is a trick to get us to store a copy of a pointer to a buffer, rather than making a copy of the buffer
        return self.msg_buffer_wrapper["msg_buffer"]

    @staticmethod
    def MsgName():
        return "<MSGDESCRIPTOR>"
    # Accessors
    <ACCESSORS>

    # Reflection information
    fields = [ \
        <REFLECTION>\
    ]

Messaging.Register("<MSGDESCRIPTOR>", <MSGNAME>.ID, <MSGNAME>)
