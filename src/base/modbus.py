import modbus_tk.modbus_tcp as mt
import modbus_tk.defines as md
import logging,os
#from getConfiginfo import sinleCfg
#from DataManage import Display
#import l4_report_method
from datetime import datetime, timezone, timedelta
import time
import json


# @slave=1 : identifier of the slave. from 1 to 247.  0为广播所有的slave
# @function_code=READ_HOLDING_REGISTERS：功能码
# @starting_address=1：开始地址
# @quantity_of_x=3：寄存器/线圈的数量
# @output_value：一个整数或可迭代的值：1/[1,1,1,0,0,1]/xrange(12)
# @data_format
# @expected_length
#Hold_value = master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS, starting_address=40001, quantity_of_x=3, output_value=5)
#print(Hold_value)  # 取到的寄存器的值格式为元组(55, 12, 44)
#Hold_value = master.execute(slave=1, function_code=md.WRITE_MULTIPLE_REGISTERS , starting_address=40001, quantity_of_x=2, output_value=[3,7])
#Coils_value = master.execute(slave=1, function_code=md.READ_COILS, starting_address=40001,  quantity_of_x=3, output_value=5)

#print(Hold_value)  # 取到的寄存器的值格式为元组(55, 12, 44)
#print(Hold_value)  # 取到的寄存器的值格式为元组(1, 1, 1)

class modbus_request:
    logger = logging.getLogger("main.sub.mobus_request")
    
    cfg = {"modbus":{
        "ip":"127.0.0.1",
        "port":502,
        "slave":1,
        "timer":3
    }}
    master =None
    _slave = None
    #def __init__(self): # 1 空，2 ，3 可以释放 ，0 正在进行
    __add_map = {
        "1canload":{"addr":5010,"bit":-1},
        "2canload":{"addr":5011,"bit":-1},
        "1load":{"addr":10,"bit":-1},
        "2load":{"addr":11,"bit":1},
        "ucanget":{"addr":5020,"bit":-1},
        "uget":{"addr":20,"bit":-1},
        "ecanget":{"addr":5030,"bit":-1},
        "eget":{"addr":31,"bit":-1}
    }
    def reverseBits(n):
        bits = "{:0>8b}".format(n)
        return int(bits[::-1], 2)
    def getOnebit(num,n):
        bits = "{:0>8b}".format(n)
        return int(bits[n:n+1], 2)   
    def connect(self):
        print(self.cfg["modbus"])
        try:            
            self.master = mt.TcpMaster(self.cfg["modbus"]["ip"], self.cfg["modbus"]["port"])
            self.master.set_timeout(self.cfg["modbus"]["timer"])
            self._slave = self.cfg["modbus"]["slave"]
           
        except Exception as  e: 
            logging.error("connect error")
            logging.error(e)
    
    def getMultValue(self,slave,addr,qty):
        print(slave,addr,qty)
        try:
            Hold_value = self.master.execute(slave=slave, function_code=md.READ_HOLDING_REGISTERS, starting_address=addr, quantity_of_x=qty)
        except Exception as  e: 
            logging.error("get data error")
            logging.error(e)    
            return None
        return Hold_value
    
    def setMultValue(self,slave,addr,qty,vallist):
        
        try:
            Hold_value = self.master.execute(slave=slave, function_code=md.WRITE_SINGLE_REGISTER , starting_address=addr, quantity_of_x=qty,output_value=vallist)
        except Exception as  e: 
            logging.error("setMultValue error")
            logging.error(e)    
            return None
        return Hold_value
    
    def getOnePosStatus(self,opt):
        slave = self._slave
        addr = self.__add_map[opt]["addr"] 
        bit = self.__add_map[opt]["bit"]
        #print(slave,addr,1)
        value = self.getMultValue(slave,addr,1)
        return value
    '''    
    def getMutlPosStatus(self,opt):
        slave = self._slave
        addr = self.__add_map["Bstatus"]["addr"]
        bit = self.__add_map["Bstatus"]["bit"]
        value = self.getMultValue(slave,addr,4)
        print(dict(zip(["Bstatus","Dstatus","Estatus","Fstatus"],list(value))))
        return dict(zip(["Bstatus","Dstatus","Estatus","Fstatus"],value))
    '''    
    def setOnePosValue(self,pos,value):
        slave = self._slave
        addr = self.__add_map[pos]["addr"] 
        bit = self.__add_map[pos]["bit"]
        print(slave,addr,1)
        #value = self.setMultValue(slave,addr,1,list([value]))
        value = self.setMultValue(slave,addr,1,value)
        return value
        
    
if __name__ == "__main__":
    #print(hex((int('0x1245',16) & 0xff)))
    #print(hex(int('0x1245',16) >>8))
           
    #print(bin(12))
    #print(bin(reverseBits(12)))
    mk = modbus_request()
    mk.connect()
    cc = mk.getOnePosStatus("1canload")     
    mk.setOnePosValue("2canload",1)
    print(cc)
    print('主进程')
    
