from modules import enums

class ScriptEvaluation:
    def __init__(self, stack:list=[]):
        self.stack = stack

    def OP_0(self, string):
        self.stack.append(0)
        return string[2:] #vrátí zbytek witness bez Opcode dat

    def OP_1(self, string):
        self.stack.append(1) 
        return string[2:] #vrátí zbytek witness bez Opcode dat
    
    def OP_2(self, string):
        self.stack.append(2)
        return string[2:] #vrátí zbytek witness bez Opcode dat
    
    def OP_ADD(self, string):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(a + b)
        return string[2:] #vrátí zbytek witness bez Opcode dat

    def Read_OP_Byte(self, string, OP_byte):
        self.stack.append(string[2:OP_byte*2+2]) #pushne hodnotu
        return string[2+OP_byte*2:] #vrátí zbytek witness bez Opcode a dat
    
    def OP_PUSHDATA(self, string, OP_byte):
        byte_num = pow(2, OP_byte - 76) #zjistí, kolik následujících bajtů obsahuje informaci, kolik bajtů obsahuje data - 1, 2 nebo 4

        segment_length = int(ScriptEvaluation.reverse(string[2:byte_num*2+2]), 16) #přečte bajty, které říkají, kolik bajtů obsahuje hodnotu - je třeba změnit endianitu

        self.stack.append(string[2 + byte_num * 2 :segment_length*2 + byte_num*2 + 2]) #pushne na stack data
        return string[2 + segment_length*2 + byte_num*2:] #vrátí zbytek witness bez přečtených dat
    
    def Execute_opcode(self, string):
        OP_byteHex = string[0:2] #přečte bajt s Opcode
        OP_byte = int(OP_byteHex, 16)

        if OP_byte >= 1 and OP_byte <= 75:
            return self.Read_OP_Byte(string, OP_byte)
        elif OP_byte >= 76 and OP_byte <= 78:
            return self.OP_PUSHDATA(string, OP_byte)
        else:
            return eval("self." + enums.BitcoinOP.convert_byte_to_op(OP_byteHex) + "('" + string + "')")
        

    def reverse(input:str)->str:
        L = len(input)
        if (L % 2) != 0:
            return None
        else:
            Res = ''
            L = L // 2
            for i in range(L):
                T = input[i*2] + input[i*2+1]
                Res = T + Res
                T = ''
            return Res