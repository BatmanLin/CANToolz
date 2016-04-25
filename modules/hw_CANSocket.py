from libs.can import *
from libs.module import *
import socket
import struct

class hw_CANSocket(CANModule):
    name = "CANSocket I/O"
    help = """
    
    This module to read/write with CANSocket

    
    Init parameters example:  

     'iface' : 'vcan0',       # device

    Module parameters: 
      action - 'read' or 'write'. Will write/read to/from bus
      'pipe' -  integer, 1 by default - from which pipe to read or write

        Example: {'action':'read','pipe':2}
   
    """

    _bus = 90

    socket = None
    device = None


    def do_init(self, init_params):  # Get device and open serial port
        self.device = init_params.get('iface', None)
        self._cmdList['t'] = ["Send CAN frame directly, like 01A:4:11223344", 1, " <frame> ", self.dev_write]
        self._active = True
        self._run = False

    def dev_write(self, data):

        return ""

    def do_start(self, params):
        if not self.device and not self._run:
            try:
                self.socket = socket.socket(socket.PF_CAN, socket.SOCK_RAW,  socket.CAN_RAW)
                self.socket.bind((self.device,))
                self._run = True
            except Exception as e:
                self._run = False
                self.dprint(0, "ERROR: " + str(e))

    def do_stop(self, params):
        if not self.device and self._run:
            try:
                self.socket.close()
                self._run = True
            except:
                self._run = False

    def do_effect(self, can_msg, args):  # read full packet from serial port
        if args.get('action') == 'read':
            can_msg = self.do_read(can_msg)
        elif args.get('action') == 'write':
            self.do_write(can_msg)
        else:
            self.dprint(1, 'Command ' + args['action'] + ' not implemented 8(')
        return can_msg

    def do_read(self, can_msg):
        if self._run and not can_msg.CANData:
            can_frame = self.socket.recv(16)
            self.dprint(2, "READ: " + self.get_hex(can_frame))
            #if len(can_frame) >:
            #    can_msg.CANData = True
            #    can_msg.CANFrame = CANMessage.init_raw_data(can_frame[0:4], can_frame[4], can_frame[5:])

        return can_msg

    def do_write(self, can_msg):
        if can_msg.CANData:
            cmd_byte = None

        return can_msg
