from modbus_tk import modbus
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

if __name__ == "__main__":
    from settings import modbus_cfg
else:
    from .settings import modbus_cfg

def check_ptr(slave_no,addr,checkaddr = True):
    if modbus_cfg is None or slave_no not in modbus_cfg:
        return False,"slave_no = {} ,cfg is None".format(slave_no)
    else:
        if "ip" not in modbus_cfg[slave_no] or modbus_cfg[slave_no]["ip"] is None or modbus_cfg[slave_no]["ip"] == "":
            return False,"ip  错误 请查看配置文件"
        if "port" not in modbus_cfg[slave_no] or modbus_cfg[slave_no]["port"] is None or modbus_cfg[slave_no]["port"] == "":
            return False,"port 错误 请查看配置文件"
        if "id" not in modbus_cfg[slave_no] or modbus_cfg[slave_no]["id"] is None or modbus_cfg[slave_no]["id"] == "":
            return False,"id 错误 请查看配置文件"
        if checkaddr == True:
            if "addrs" not in modbus_cfg[slave_no] or len(modbus_cfg[slave_no]["addrs"]) ==0:
                return False,"addrs 错误 请查看配置文件"
            elif isinstance(modbus_cfg[slave_no]["addrs"],list):
                for key,value in addr.items():
                    if key not in modbus_cfg[slave_no]["addrs"]:
                        return False,"{} 不在可允许地址列表，请查看配置文件".format(key)
            elif isinstance(modbus_cfg[slave_no]["addrs"],dict):
                for value in addr:
                    if value not in modbus_cfg[slave_no]["addrs"].values():
                        return False,"{} 不在可允许地址列表，请查看配置文件".format(value)
            else:
                return False,"addrs 错误 未知类型"


        return True,None

def set_data_sync(slave_no,data,checkaddr = True):
    flag,err= check_ptr(slave_no,data,checkaddr)
    if flag == False:
        return flag,err
    cfg = modbus_cfg[slave_no]
          
    master = mt.TcpMaster(modbus_cfg[slave_no]["ip"], modbus_cfg[slave_no]["port"])
    master.set_timeout(modbus_cfg[slave_no]["time_out"])         
    
    try:
        for key,value in data.items():
            Hold_value = master.execute(slave=cfg["id"], function_code=md.WRITE_SINGLE_REGISTER , starting_address=key, quantity_of_x=1,output_value=value)
    except Exception as  e: 
        logging.error("setMultValue error")
        logging.error(e)
        #print(e.get_exception_code())
        #raise e             
        return False,"设置失败"
    return True,None


def get_data_sync(slave_no:str,data:list,checkaddr = True):
    flag,err= check_ptr(slave_no,data,checkaddr)
    '''
    if isinstance(modbus_cfg[slave_no]["addrs"],dict):
        data = data.values()
    '''
    if flag == False:
        return flag,err
    cfg = modbus_cfg[slave_no]
    
             
    master = mt.TcpMaster(cfg["ip"], cfg["port"])
    master.set_timeout(cfg["time_out"])         

    res_data ={}

    try:
        for key in data:
        #print((master.execute(slave=1, function_code=md.READ_HOLDING_REGISTERS , starting_address=5010, quantity_of_x=1)))          
            Hold_value = master.execute(slave=cfg["id"], function_code=md.READ_HOLDING_REGISTERS , starting_address=key, quantity_of_x=1)
            res_data[key] = Hold_value[0]

    except Exception as  e: 
        logging.error("get_data_sync")
        logging.error(e)       
        return False,"读取失败"
    return True,res_data

cnt = 1
import  time
def get_string_sync(slave_no:str,data:list):
    flag,err= check_ptr(slave_no,data)
    '''
    if isinstance(modbus_cfg[slave_no]["addrs"],dict):
        data = data.values()
    '''
    if flag == False:
        return flag,err
    cfg = modbus_cfg[slave_no]
    test = 1


    global cnt
    start = time.time()
    timeArray = time.localtime(start)
    timedate = time.strftime("%Y-%m-%d",timeArray)
    #cnt = cnt +1
    batch = timedate+'{0:05d}'.format(cnt)
    if test == 1:
        return True,batch
    elif test == 2:
        return False,"unready"
    else:
        return False,"error"


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
        "1canload":{"addr":10,"bit":-1},
        "2canload":{"addr":11,"bit":-1},
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
            #print(e.get_exception_code())            
            #raise e             
            return None
        return Hold_value
    
    def setMultValue(self,slave,addr,qty,vallist):
        
        try:
            Hold_value = self.master.execute(slave=slave, function_code=md.WRITE_SINGLE_REGISTER , starting_address=addr, quantity_of_x=qty,output_value=vallist)
        except Exception as  e: 
            logging.error("setMultValue error")
            logging.error(e)
            #print(e.get_exception_code())
            #raise e             
            return None
        return Hold_value
    

    def getOnePosStatus(self,opt):
        slave = self._slave
        addr = self.__add_map[opt]["addr"] 
        #print(slave,addr,1)
        value = self.getMultValue(slave,addr,1)
        return value
        

        
    def setOnePosValue(self,pos,value):
        slave = self._slave
        addr = self.__add_map[pos]["addr"] 
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
    #dd = mk.setOnePosValue("2canload",1)
    print(cc)
    Hold_value = mk.master.execute(slave=1, function_code=md.READ_INPUT_REGISTERS, starting_address=00, quantity_of_x=27)
    
    print(Hold_value)
    dd = str(bytearray(Hold_value))
    print(dd)