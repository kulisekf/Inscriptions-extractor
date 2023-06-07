from workWithData import Data
from enums import BitcoinOP

class ScriptEvaluation:
    """
    This class is used to evaluate the Bitcoin Script. Individual methods are used to work with data and stack according to the identifying OP_CODE    
    
        :ivar stack list: stack with Script evaluation
    """

    def __init__(self: object, stack:list=[]) -> None:
        """
        Constructs necessary attributes for the object.           

            :param self object: class object
            :param stack list: stack with Script evaluation
        """
        self.stack = stack

    def OP_0(self: object, string: str) -> str:
        """
        This method push value 0 on the stack         

            :param self object: class object
            :param string str: String Script to be evaluated sequentially
            
            :returns: returns the rest of the string - data not used by this method
            :rtype: str 
        """
        self.stack.append(0)
        return string[2:] #vrátí zbytek witness bez Opcode dat

    def OP_1(self: object, string: str) -> str:
        """
        This method push value 1 on the stack         

            :param self object: class object
            :param string str: String Script to be evaluated sequentially
            
            :returns: returns the rest of the string - data not used by this method
            :rtype: str 
        """
        self.stack.append(1) 
        return string[2:] #vrátí zbytek witness bez Opcode dat
    
    def OP_2(self: object, string: str) -> str:
        """
        This method push value 2 on the stack         

            :param self object: class object
            :param string str: String Script to be evaluated sequentially
            
            :returns: returns the rest of the string - data not used by this method
            :rtype: str 
        """
        self.stack.append(2)
        return string[2:] #vrátí zbytek witness bez Opcode dat
    
    def OP_ADD(self: object, string: str) -> str:
        """
        this method pops the top 2 elements of the stack, adds them and pushes the result onto the stack        

            :param self object: class object
            :param string str: String Script to be evaluated sequentially
            
            :returns: returns the rest of the string - data not used by this method
            :rtype: str 
        """
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(a + b)
        return string[2:] #vrátí zbytek witness bez Opcode dat

    def Read_OP_Byte(self: object, string: str, OP_byte: str) -> str:
        """
        this method accepts a byte representing how many subsequent bytes contain data - it push that data onto the stack     

            :param self object: class object
            :param string str: String Script to be evaluated sequentially
            :param OP_byte str: int byte value - identifies how many subsequent bytes in the string contain data
            
            :returns: returns the rest of the string - data not used by this method
            :rtype: str 
        """
        self.stack.append(string[2:OP_byte*2+2]) #pushne hodnotu
        return string[2+OP_byte*2:] #vrátí zbytek witness bez Opcode a dat
    
    def OP_PUSHDATA(self: object, string: str, OP_byte: str) -> str:
        """
        this method accepts a byte representing how many subsequent bytes contain information, how many bytes contain data - push that data on the stack  

            :param self object: class object
            :param string str: String Script to be evaluated sequentially
            :param OP_byte str: int byte value - identifies how many subsequent bytes in the string contain data
            
            :returns: returns the rest of the string - data not used by this method
            :rtype: str 
        """
        byte_num = pow(2, OP_byte - 76) #zjistí, kolik následujících bajtů obsahuje informaci, kolik bajtů obsahuje data - 1, 2 nebo 4

        segment_length = int(Data.reverse(string[2:byte_num*2+2]), 16) #přečte bajty, které říkají, kolik bajtů obsahuje hodnotu - je třeba změnit endianitu

        self.stack.append(string[2 + byte_num * 2 :segment_length*2 + byte_num*2 + 2]) #pushne na stack data
        return string[2 + segment_length*2 + byte_num*2:] #vrátí zbytek witness bez přečtených dat
    
    def Execute_opcode(self: object, string: str) -> str:
        """
        this method reads a byte representing OP_CODE. Based on its value, execute the method corresponding to this OP_CODE

            :param self object: class object
            
            :returns: in return, it calls the method corresponding to the OP_CODE byte - this method return a string with data that it did not use
            :rtype: str 
        """
        OP_byteHex = string[0:2] #přečte bajt s Opcode
        OP_byte = int(OP_byteHex, 16)

        if OP_byte >= 1 and OP_byte <= 75:
            return self.Read_OP_Byte(string, OP_byte)
        elif OP_byte >= 76 and OP_byte <= 78:
            return self.OP_PUSHDATA(string, OP_byte)
        else:
            return eval("self." + BitcoinOP.convert_byte_to_op(OP_byteHex) + "('" + string + "')")