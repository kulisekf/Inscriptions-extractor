from io import BufferedReader
import hashlib

##přečte určitý počet bajtů, změní little-endian notaci na notmální
def read_bytes(file:BufferedReader,n:int,byte_order:str = 'L')->str:
    """
    This function reads the specified number of bytes and also changes the notation from little-endian to classic by default

        :param BufferedReader file: File to read data (bytes)
        :param int n: Number of bytes to read
        :param str byte_order: Specifies endianity - default "L" (little-endian)

        :returns: read bytes in big-endian (classical) notation format

        :rtype: str
    """
    data = file.read(n)
    if byte_order == 'L':
        data = data[::-1]
    data = data.hex().upper()
    return data

##bajt dat může značit více věcí - zde se rozhoduje, zda samotný bajt je výsledná požadovaná hodnota, či zda značí kolik následujících bajtů hodnotu obsahuje a až následně načte tuto hodnotu
def read_varint(file:BufferedReader)->str:
    """
    This function reads one byte of data and decides whether this byte contains the searched data, or whether it contains information on how many subsequent bytes contain the searched data, which it then reads

        :param BufferedReader file: File to read data (bytes)

        :returns: value stored in one or more (2, 4, 8) bytes of data

        :rtype: str
    """
    b = file.read(1)
    bInt = int(b.hex(),16)
    data = ''
    if bInt < 253:
        c = 0
        data = b.hex().upper()
    if bInt == 253: c = 2
    if bInt == 254: c = 4
    if bInt == 255: c = 8
    for j in range(0,c):
        b = file.read(1)
        b = b.hex().upper()
        data = b + data
    return data

##funguje stejně, jako předchozí. S tím rozdílem, že je třeba uchovat a returnnout všechna data - použita pro výpočet transaction hashe
def read_varint_transaction(file:BufferedReader)->str:
    """
    This function works in the same way as the read_variant() function, with the only difference that it needs to store and return all the data it works with - it is used, for example, to calculate the transaction hash
        
        :param BufferedReader file: File to read data (bytes)

        :returns: all the loaded data that the function worked with

        :rtype: str
    """
    b = file.read(1)
    tmpB = b.hex().upper()
    bInt = int(b.hex(),16)
    tmpHex = ''
    if bInt < 253:
        c = 0
        tmpHex = b.hex().upper()
        tmpB = ''
    if bInt == 253: c = 2
    if bInt == 254: c = 4
    if bInt == 255: c = 8
    for j in range(0,c):
        b = file.read(1)
        b = b.hex().upper()
        tmpHex = b + tmpHex
    return tmpHex, tmpB

##z little-endian stringu udělá big-endian
def reverse(input:str)->str:
    """
    This function turns a little-endian string into big-endian        
        
        :param str input: Data sequence to change endianity

        :returns: Data with changed endianness

        :rtype: str
    """
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
    
#vypočítá hash vstupních dat
def hash_of_data(data:str)->str:
    """
    This function calculates a 2x sha256 hash of the input data     
        
        :param str data: input data whose hash is to be calculated

        :returns: 2x sha256 hash of input data

        :rtype: str
    """
    ##vypocita hash bloku (jeho hlavicky - veliká 80 bajtů)
    data = bytes.fromhex(data)
    data = hashlib.new('sha256', data).digest()
    data = hashlib.new('sha256', data).digest()
    data = data[::-1]        
    data = data.hex().upper()
    return data

def save_file(suffix:str, data:bytes, result_dir:str)->None:
    """
    This function saves the file containing the inscription
        
        :param suffix str: Suffix of the file in which the data will be stored
        :param data str: Inscription data to save to file
        :param result_dir str: The path to the folder where the inscription file should be saved (absolute/relative - preferred) - entered when starting the program in the console

        :returns: None
    """
    with open(result_dir + '/inscription.' + suffix, 'wb') as file:
            file.write(data)